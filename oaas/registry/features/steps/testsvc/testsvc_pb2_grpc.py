# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import features.steps.testsvc.testsvc_pb2 as testsvc__pb2


class ProcessNameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_process_name = channel.unary_unary(
            "/ProcessName/get_process_name",
            request_serializer=testsvc__pb2.ProcessNameIn.SerializeToString,
            response_deserializer=testsvc__pb2.ProcessNameOut.FromString,
        )


class ProcessNameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_process_name(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    @staticmethod
    def add_to_server(servicer, server):
        rpc_method_handlers = {
            "get_process_name": grpc.unary_unary_rpc_method_handler(
                servicer.get_process_name,
                request_deserializer=testsvc__pb2.ProcessNameIn.FromString,
                response_serializer=testsvc__pb2.ProcessNameOut.SerializeToString,
            ),
        }
        generic_handler = grpc.method_handlers_generic_handler(
            "ProcessName", rpc_method_handlers
        )
        server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ProcessName(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_process_name(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ProcessName/get_process_name",
            testsvc__pb2.ProcessNameIn.SerializeToString,
            testsvc__pb2.ProcessNameOut.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
