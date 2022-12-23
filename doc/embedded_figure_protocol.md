# Embedded figure protocol (v1)

The figURL is of the form

```html
https://figurl.org/f?v=<view_uri>&d=<data_uri>&label=<label>&s=<url_state_string>&zone=<zone>
```

The figure is embedded in an iframe in one of two ways

Method 1:
```tsx
<iframe src={`${srcUrl}?parentOrigin=${parentOrigin}>&figureId=${figureId}&s=<url_state_string>`}>
```

where

```typescript
const srcUrl = '<obtained-from-view-uri>'
const parentOrigin = window.location.protocol + '//' + window.location.host
const figureId = '<random-figure-id>'
```

Method 2:
```html
<iframe srcdoc="<html_source>">
```

where the html source is obtained from downloading the content at the view URI.

For method 2, a message is immediately posted to the iframe as follows:

```typescript
const msg = {
    type: 'initiateFigure',
    parentOrigin: '**',
    figureId: '<figure_id>',
    s?: <url_state>
}
iframe.postMessage(msg, '*')
```

The child posts messages to the parent as follows:

```typescript
const request: FigurlRequest = ... // defined below
const msgToParent = {
    type: 'figurlRequest',
    figureId: '<figure_id>',
    requestId: '<random_request_id>',
    request: request
}
window.parent.postMessage(msgToParent, '<parent_origin>')
```

The parent sends messages to the child as follows:

```typescript
const msgToChild: FigurlResponseMessage | FileDownloadProgressMessage | SetCurrentUserMessage = ... // defined below

// For method 1, origin is origin of <src_url>
// For method 2, origin is *
iframe.postMessage(msgToChild, origin)
```

```typescript
// request message to parent

type FigurlRequest =
    GetFigureDataRequest |
    GetFileDataRequest |
    GetFileDataUrlRequest |
    StoreFileRequest |
    StoreGithubFileRequest |
    SetUrlStateRequest

type GetFigureDataRequest = {
    type: 'getFigureData'
}

type GetFileDataRequest = {
    type: 'getFileData'
    uri: string
    responseType?: string // 'text', 'json', 'json-deserialized': default is 'json-deserialized'
}

type GetFileDataUrlRequest = {
    type: 'getFileDataUrl'
    uri: string
}

type StoreFileRequest = {
    type: 'storeFile'
    fileData: string
}

type StoreGithubFileRequest = {
    type: 'storeGithubFile'
    fileData: string
    uri: string
}

type SetUrlStateRequest = {
    type: 'setUrlState'
    state: {[key: string]: any}
}
```

```typescript
// response message to child

type FigurlResponseMessage = {
    type: 'figurlResponse',
    requestId: string,
    response: FigurlResponse
}

type FigurlResponse =
    GetFigureDataResponse |
    GetFileDataResponse |
    GetFileDataUrlResponse |
    StoreFileResponse |
    StoreGithubFileResponse |
    SetUrlStateResponse

type GetFigureDataResponse = {
    type: 'getFigureData'
    figureData: any
}

type GetFileDataResponse = {
    type: 'getFileData'
    fileData?: any
    errorMessage?: string
}

type GetFileDataUrlResponse = {
    type: 'getFileDataUrl'
    fileDataUrl?: string
    errorMessage?: string
}

type StoreFileResponse = {
    type: 'storeFile'
    uri?: string
    error?: string
}

type StoreGithubFileResponse = {
    type: 'storeGithubFile'
    success: boolean
    error?: string
}

type SetUrlStateResponse = {
    type: 'setUrlState'
}
```

```typescript
// other messages to child

type FileDownloadProgressMessage = {
    type: 'fileDownloadProgress'
    uri: string
    loaded: number
    total: number
}

type SetCurrentUserMessage = {
    type: 'setCurrentUser',
    userId: string
}
```