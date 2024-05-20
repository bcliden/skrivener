# Skrivener

## Overview

<p align="right">
<img alt="An example generated image: 'Traditionally, art has been for the select few. We have been brainwashed to believe that Michaelangelo had to pat you on the head at birth. Well, we show people that anybody can paint a picture that they're proud of -- Bob Ross'" src="https://github.com/bcliden/skrivener/assets/27828594/874787c1-7992-45f3-8946-10e64b2197bc"  height="250px" align="right"/>
</p>

Skrivener is a service that accepts text and typesets it into an image. This service communicates over ZeroMQ protocol using JSON formatted messages.

Features:
- Accepts up to 250 characters of UTF-8 text
- Returns PNG formatted image
- Pleasant color pairings
  - can be customized
- Unsurprising interfaces
    - JSON messages
    - Base64 encoding

## Installation

1. Clone this repository
2. Enter or initialize a Python virtual environment*
3. Install this repo with `$ pip install .`
4. Run this project
   - either execute `$ skrivener` (this command is placed in your $PATH by PIP)
   - or execute `$ python -m skrivener`

Skrivener reads some environment variables on initialization.
The provided defaults are:
- `host=*`
- `port=8672`
- `loglevel=info`

You can change these in the `.env.example` file provided, make your own `.env`, or set these environment variables another way.

\* for more on this see [the Python Packaging Authority's introduction](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

## Communication Contract

Send and recieve data using a ZeroMQ REP socket:
```py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind(f"tcp://{HOST}:{PORT}")

# send response dict using send_json()
socket.send_json({ "text": "Hello from CS361" })

# recieve reply dict using recv_json()
reply = socket.recv_json()
```

### Request Format
The accepted parameters for generating an image are:
- text:
   - required: Yes
   - type: `string`
   - constraints: 1-250 characters
- colors:
   - required: No
      - default: a color pairing will be selected from [the default palettes](https://github.com/bcliden/skrivener/blob/main/src/text_to_image/color.py#L11)
   - type: `object`
   - constraints
       - both keys are required
       - value formats must be [valid hex color codes](https://en.wikipedia.org/wiki/Web_colors#Hex_triplet)
           - optional "#" prefix, 3 or 6 digits, characters [0-9, a-f, A-F] only
   - keys:
       - "bg": `string`
       - "text": `string`

#### Examples

```json
{
  "text": "Traditionally, art has been for the select few. We have been brainwashed to believe that Michaelangelo had to pat you on the head at birth. Well, we show people that anybody can paint a picture that they're proud of -- Bob Ross"
}
```

or, specifying the colors:
```json
{
  "text": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.",
  "colors": {
    "text": "#fff",
    "bg": "#000"
  }
}
```

### Response Format

All Skrivener responses have one common key:
- status
    - required: Yes
    - type: `string` 

#### Ok

- status
   - required: Yes
   - type: literal string `ok` 
- image:
   - required: Yes
   - type: `string`
   - info
     - this is a base64 encoded PNG file (for instructions on usage, see below)

##### Example

```json
{
    "status": "ok",
    "image":  "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIA (...)"
}
```

#### Error

- status
   - required: Yes
   - type: literal string `error` 
- message
   - required: Yes
   - type: `string`
   - info
     - provides context for what went wrong 
    
##### Example
In this example, we sent one malformed color (#0fg).

```json
{
    "status": "error",
    "message": "unknown color specifier: '#0fg'"
}
```

Because Skrivener uses Pydantic for data validation, any formatting or validation errors should be human readable.

### Sequence Diagram

![2024-05-20 14_18_37-Untitled _ Visual Paradigm Online — Mozilla Firefox](https://github.com/bcliden/skrivener/assets/27828594/51ef3ea6-3a05-4a87-b5fa-b520c8f32229)

## How To
### Using the encoded image response

To decode the Base64 string in Python, use [the base64 module](https://docs.python.org/3/library/base64.html):
```py
import base64

image_encoded = "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIA (...)"
image_bytes: bytes = base64.b64decode(image_encoded)
```

Then, you may write that image out to disk using `open`
```py
with open("/your/file/here.png", "wb") as file:
    file.write(image_bytes)
```
or read using Pillow
```py
bytes_buffer = io.BytesIO(image_bytes)
image = im.open(bytes_buffer)
# do anything with image!
image.show() # will open in your system viewer
```

Also see the test client script in the repo at [/tests/client.py](/tests/client.py#L52-L58)

## Attributions

Skrivener uses
- [Pillow](https://github.com/python-pillow/Pillow) for image manipulation
- [Pydantic](https://github.com/pydantic/pydantic) for data validation
- [pyzmq](https://github.com/zeromq/pyzmq) for ZeroMQ communication
- [Poetsen One](https://fonts.google.com/specimen/Poetsen+One) font, designed by Rodrigo Fuenzalida, Pablo Impallari 
