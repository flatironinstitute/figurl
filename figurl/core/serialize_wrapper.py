from functools import wraps 
import base64
import numpy as np

def serialize_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        output = f(*args, **kwargs)
        return _serialize(output)
    return wrapper

def _serialize(x, *, compress_npy=False, label: str='', allow_float64: bool=False):
    if isinstance(x, np.integer):
        return int(x)
    elif isinstance(x, np.floating):
        return float(x)
    elif type(x) == dict:
        ret = dict()
        for key, val in x.items():
            if not isinstance(key, str):
                raise Exception(f'serialize: keys must be string not {str(type(key))}: {label}')
            ret[key] = _serialize(val, compress_npy=compress_npy, label=f'{label}.{key}', allow_float64=allow_float64)
        return ret
    elif (type(x) == list) or (type(x) == tuple):
        return [_serialize(val, compress_npy=compress_npy, label=f'{label}[{ii}]', allow_float64=allow_float64) for ii, val in enumerate(x)]
    elif isinstance(x, np.ndarray):
        # todo: worry about byte order here
        if str(x.dtype) not in ['uint8', 'int16', 'uint16', 'int32', 'uint32', 'float32', 'float64']:
            raise Exception(f'Unable to serialize numpy array with dtype {str(x.dtype)}: {label}')
        if str(x.dtype) == 'float64':
            if not allow_float64:
                raise Exception('Unable to serialize numpy array with dtype float64. It is usually best to convert to float32, but if you need 64-bit, then use allow_float64=True.')
        ret = {
            '_type': 'ndarray',
            'shape': _serialize(x.shape, allow_float64=allow_float64),
            'dtype': str(x.dtype)
        }
        if compress_npy:
            import zlib
            ret['data_gzip_b64'] = base64.b64encode(zlib.compress(x.ravel().tobytes(), level=9)).decode()
        else:
            ret['data_b64'] = base64.b64encode(x.ravel()).decode()
        return ret
    else:
        if _is_jsonable(x):
            # this will capture int, float, str, bool
            return x
    raise Exception(f'Item is not json safe: {type(x)}')

def _deserialize(x):
    if type(x) == dict:
        if x.get('_type', None) == 'ndarray':
            shape = x['shape']
            dtype = x['dtype']
            if 'data_b64' in x.keys():
                data_b64 = x['data_b64']
            elif 'data_gzip_b64' in x.keys():
                import zlib
                data_b64 = zlib.decompress(x['data_gzip_b64'])
            else:
                raise Exception('Missing field: data_b64 or data_gzip_b64')
            data = base64.b64decode(data_b64)
            x = np.reshape(np.frombuffer(data, dtype=dtype), shape)
            return x
        else:
            ret = dict()
            for key, val in x.items():
                ret[key] = _deserialize(val)
            return ret
    elif (type(x) == list) or (type(x) == tuple):
        return [_deserialize(val) for val in x]
    else:
        return x

def _is_jsonable(x) -> bool:
    import json
    try:
        json.dumps(x)
        return True
    except:
        return False