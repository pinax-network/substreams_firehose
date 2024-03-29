"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ....sf.substreams.v1 import substreams_pb2 as sf_dot_substreams_dot_v1_dot_substreams__pb2

class StreamStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Blocks = channel.unary_stream('/sf.substreams.v1.Stream/Blocks', request_serializer=sf_dot_substreams_dot_v1_dot_substreams__pb2.Request.SerializeToString, response_deserializer=sf_dot_substreams_dot_v1_dot_substreams__pb2.Response.FromString)

class StreamServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Blocks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_StreamServicer_to_server(servicer, server):
    rpc_method_handlers = {'Blocks': grpc.unary_stream_rpc_method_handler(servicer.Blocks, request_deserializer=sf_dot_substreams_dot_v1_dot_substreams__pb2.Request.FromString, response_serializer=sf_dot_substreams_dot_v1_dot_substreams__pb2.Response.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sf.substreams.v1.Stream', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Stream(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Blocks(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/sf.substreams.v1.Stream/Blocks', sf_dot_substreams_dot_v1_dot_substreams__pb2.Request.SerializeToString, sf_dot_substreams_dot_v1_dot_substreams__pb2.Response.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)