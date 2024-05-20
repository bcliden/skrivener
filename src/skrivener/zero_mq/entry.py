import logging
import sys

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from signal import signal, SIGINT, SIG_DFL
from typing import Optional

import zmq

from skrivener.zero_mq.config import Config
from skrivener.image import typography
from skrivener.zero_mq.models import Request, SuccessReply, ErrorReply

logger = logging.getLogger(__name__)


def get_type(sock: zmq.Socket) -> str:
    socket_type = sock.get(zmq.TYPE)
    if socket_type == zmq.REQ:
        return "REQ"
    elif socket_type == zmq.REP:
        return "REP"
    else:
        return "unknown"


def main() -> None:
    cfg = Config()

    logging.basicConfig(
        level=cfg.loglevel.upper(),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            # write out to log file
            RotatingFileHandler(
                filename="text_to_img-zmq.log",
                maxBytes=1024 * 100,                # max file size: 100kB
                backupCount=1                       # how many previous ones to keep?
            ),
            # and to the process stderr
            StreamHandler(sys.stderr),
        ],
    )

    logger.info("using config: %s", cfg)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{cfg.host}:{cfg.port}")

    logger.info(
        "bound to %s socket on tcp://%s:%s",
        get_type(socket),
        cfg.host,
        cfg.port,
    )

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    while True:
        #  Wait for next request from client
        recieved: str = socket.recv_string()
        logger.info("Recieved string on socket of size len=%d", len(recieved))
        logger.debug("Recieved: %s", str)

        reply: Optional[SuccessReply | ErrorReply] = None
        try:
            # accept json message
            request = Request.model_validate_json(recieved)
            logger.debug("successfully parsed json: %s", request)

            image = typography.set_text(request.text, request.color)
            logger.info("successfully generated text image")

            reply = SuccessReply(image=image)

        except Exception as e:
            logger.exception("something broke in the core loop:")

            # is it so bad to just dump the exception out in the reply?
            reply = ErrorReply(message=str(e))

        finally:
            # we always need to send something back.

            if reply is None:
                # shouldn't really be able to get here, but...
                logger.error("reply is none after everything (bad!)", exc_info=True)
                reply = ErrorReply(message="Something went wrong.")

            logger.debug("serializing reply: %s", reply)
            message = reply.model_dump_json()

            logger.info("responding with json payload of len=%d", len(message))
            socket.send_string(message)


if __name__ == "__main__":
    main()
