import os
import tempfile


def serve_figure(*, input_file: str, port: int):
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f'tar -xvf {input_file} -C {tmpdir}')

        figure_dir = tmpdir
        if os.path.exists(os.path.join(figure_dir, 'index.html')):
            pass
        else:
            # find the singular directory in the tmpdir
            dirs = []
            for x in os.listdir(figure_dir):
                if os.path.isdir(os.path.join(figure_dir, x)):
                    dirs.append(x)
            if len(dirs) == 0:
                raise Exception(f'No top-level directories in {input_file}')
            if len(dirs) > 1:
                raise Exception(f'More than one top-level directory in {input_file}')
            figure_dir = os.path.join(figure_dir, dirs[0])
        
        # use one of the following methods but don't use "npx serve" because that has problems with rel paths and iframes
        os.system(f'cd {figure_dir} && python -m http.server {port}')
        # os.system(f'cd {tmpdir} && npx http-server -p {port}')