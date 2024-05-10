import zmq
import io
import tempfile
import time
import subprocess

from PIL import Image as im
from PIL.Image import Image

from signal import signal, SIGINT, SIG_DFL

from text_to_image.serialization.image import base64_decode


def main():
    # maybe use argparser or something for host, port, etc

    host = "localhost"
    port = "8672"

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")

    quote = """
“Buy a man eat fish, he day,
 teach fish man, to a lifetime.”
"""

    # socket.send_string(quote)
    socket.send_json({"text": quote})

    response = socket.recv_json()

    print("recieved response: ", response)

    if response["status"] == "ok":
        img = response["image"]

        img_bytes = base64_decode(img)
        b = io.BytesIO(img_bytes)

        i = im.open(b)
        i.show()


        # with tempfile.NamedTemporaryFile() as f:
        #     f.write(img_bytes)
        #     subprocess.run(["explorer.exe", f.name])
        #     time.sleep(10)


if __name__ == "__main__":
    main()
