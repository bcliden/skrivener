import zmq
from pathlib import Path

from PIL import Image as im
from PIL.Image import Image

from signal import signal, SIGINT, SIG_DFL

from text_to_image.serialization.image import base64_decode


"""
Tests to write...
- invalid hex colors values
- valid hex colors
    - # prefixed
    - non-# prefixed
    - mixed prefices
- missing one color/property
"""

def main():
    # maybe use argparser or something for host, port, etc

    host = "localhost"
    port = "8672"

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")

    #     quote = """
    # “Buy a man eat fish, he day,
    #  teach fish man, to a lifetime.”
    # """

    quote = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old."

    socket.send_json({ "text": quote })
    # socket.send_json({"text": quote, "color": {"bg": "FFF", "text": "#111"}})

    response = socket.recv_json()

    # print("recieved response: ", response)

    assert response["status"] != "error"

    if response["status"] == "ok":
        img = response["image"]

        img_bytes = base64_decode(img)

        parent_folder = Path(__file__).parent.resolve()
        with open(parent_folder / "last_recieved_test_image.png", "wb") as f:
            f.write(img_bytes)

        # b = io.BytesIO(img_bytes)
        # i = im.open(b)
        # i.show()


if __name__ == "__main__":
    main()
