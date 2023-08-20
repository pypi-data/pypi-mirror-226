# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import integration_incident_pb2 as admin_dot_v1_dot_integration__incident__pb2


class IncidentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ConnectIncidentAccount = channel.unary_unary(
                '/admin.v1.IncidentService/ConnectIncidentAccount',
                request_serializer=admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountRequest.SerializeToString,
                response_deserializer=admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountResponse.FromString,
                )
        self.GetIncidentAccounts = channel.unary_unary(
                '/admin.v1.IncidentService/GetIncidentAccounts',
                request_serializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsRequest.SerializeToString,
                response_deserializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsResponse.FromString,
                )
        self.GetIncidentAccountById = channel.unary_unary(
                '/admin.v1.IncidentService/GetIncidentAccountById',
                request_serializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdRequest.SerializeToString,
                response_deserializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdResponse.FromString,
                )
        self.DeleteIncidentAccountById = channel.unary_unary(
                '/admin.v1.IncidentService/DeleteIncidentAccountById',
                request_serializer=admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdRequest.SerializeToString,
                response_deserializer=admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdResponse.FromString,
                )


class IncidentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ConnectIncidentAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIncidentAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIncidentAccountById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteIncidentAccountById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IncidentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ConnectIncidentAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectIncidentAccount,
                    request_deserializer=admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountRequest.FromString,
                    response_serializer=admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountResponse.SerializeToString,
            ),
            'GetIncidentAccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIncidentAccounts,
                    request_deserializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsRequest.FromString,
                    response_serializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsResponse.SerializeToString,
            ),
            'GetIncidentAccountById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIncidentAccountById,
                    request_deserializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdRequest.FromString,
                    response_serializer=admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdResponse.SerializeToString,
            ),
            'DeleteIncidentAccountById': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteIncidentAccountById,
                    request_deserializer=admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdRequest.FromString,
                    response_serializer=admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'admin.v1.IncidentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IncidentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ConnectIncidentAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admin.v1.IncidentService/ConnectIncidentAccount',
            admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountRequest.SerializeToString,
            admin_dot_v1_dot_integration__incident__pb2.ConnectIncidentAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIncidentAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admin.v1.IncidentService/GetIncidentAccounts',
            admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsRequest.SerializeToString,
            admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIncidentAccountById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admin.v1.IncidentService/GetIncidentAccountById',
            admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdRequest.SerializeToString,
            admin_dot_v1_dot_integration__incident__pb2.GetIncidentAccountByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteIncidentAccountById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admin.v1.IncidentService/DeleteIncidentAccountById',
            admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdRequest.SerializeToString,
            admin_dot_v1_dot_integration__incident__pb2.DeleteIncidentAccountByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
