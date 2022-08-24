from concurrent.futures import ThreadPoolExecutor
from email import message
import logging
import threading
import time
from typing import Iterable
from google.protobuf.json_format import MessageToJson
import grpc
import stream_pb2_grpc
import stream_pb2

run = {
    "1":{
        "get": True
    }
} 
class Stream(stream_pb2_grpc.PostControllerServicer):
    def Stream(self, request, Stream):
        stream = 1
        run["1"]["get"] = True
        while(run["1"]["get"]):
            time.sleep(2)
            logging.info(f"stream ...")
            yield stream_pb2.CallInfo(session_id="1", result=stream)
            stream += 1
        yield stream_pb2.CallInfo(session_id="1", result=stream)
        logging.info(f"stream stop")

    def Cancel(self, request, context):
        run[request.session_id]["get"] = False
        logging.info(str(request.session_id))
        logging.info(str("cancel"))

        yield stream_pb2.Cancel(session_id="1")


def serve(address: str) -> None:
    server = grpc.server(ThreadPoolExecutor())
    stream_pb2_grpc.add_PostControllerServicer_to_server(Stream(), server)
    server.add_insecure_port(address)
    server.start()
    logging.info("Server serving at %s", address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve("[::]:50052")
