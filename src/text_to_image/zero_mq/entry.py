from signal import signal, SIGINT, SIG_DFL
from typing import Optional

import zmq

from text_to_image.zero_mq.config import Config
from text_to_image.image import typography
from text_to_image.zero_mq.models import Request, SuccessReply, ErrorReply


def main() -> None:
    c = Config()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{c.host}:{c.port}")

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    while True:
        #  Wait for next request from client
        recieved: str = socket.recv_string()
        reply: Optional[SuccessReply | ErrorReply] = None

        try:
            # accept json message
            request = Request.model_validate_json(recieved)
            image = typography.set_text(request.text)

            reply = SuccessReply(image=image)

        except Exception as e:
            # is it so bad to just dump the exception out?
            reply = ErrorReply(message=str(e))

        finally:
            # we always need to send something back.

            if reply is None:
                # shouldn't really be able to get here, but...
                reply = ErrorReply(message="Something went wrong.")

            message = reply.model_dump_json()
            socket.send_string(message)


if __name__ == "__main__":
    main()
