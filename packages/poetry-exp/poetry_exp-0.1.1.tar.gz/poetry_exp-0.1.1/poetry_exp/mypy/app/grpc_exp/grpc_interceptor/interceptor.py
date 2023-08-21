# (C) Copyright 2022 Hewlett Packard Enterprise Development Company, L.P.

import grpc


GRPC_SERVICES = ["Backup"]

UNARY = "unary"
SERVER_STREAMING = "server_stream"
CLIENT_STREAMING = "client_stream"
BIDI_STREAMING = "bidi_stream"  # Bidirectional streaming



def split_method_call(handler_call_details):
    """
        Infers the grpc service and method name from the handler_call_details.
    """
    # e.g. /package.ServiceName/MethodName
    parts = handler_call_details.method.split("/")
    if len(parts) < 3:
        return "", "", False

    grpc_service_name, grpc_method_name = parts[1:3]
    return grpc_service_name, grpc_method_name, True


def wrap_iterator_inc_counter(
    iterator, counter, grpc_type, grpc_service_name, grpc_method_name
):
    """Wraps an iterator and collect metrics."""

    for item in iterator:
        counter.labels(
            grpc_type=grpc_type, grpc_service=grpc_service_name,
            grpc_method=grpc_method_name
        ).inc()
        yield item


def get_method_type(request_streaming, response_streaming):
    """
    Infers the method type from if the request or the response is streaming.
    """
    if request_streaming and response_streaming:
        return BIDI_STREAMING
    elif request_streaming and not response_streaming:
        return CLIENT_STREAMING
    elif not request_streaming and response_streaming:
        return SERVER_STREAMING
    return UNARY


class GrpcInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        """Intercepts the server function calls."""

        grpc_service_name, grpc_method_name, _ = \
            split_method_call(handler_call_details)

        def metrics_wrapper(behavior, request_streaming, response_streaming):
            async def new_behavior(request_or_iterator, servicer_context):
                try:
                    grpc_type = get_method_type(
                        request_streaming, response_streaming
                    )
                    try:
                        print(
                            f'grpc_service_name:{grpc_service_name},'
                            f' grpc_method_name:{grpc_method_name},'
                            f' request_streaming: {request_streaming},'
                            f' response_streaming:{response_streaming}')

                        if grpc_service_name not in GRPC_SERVICES:
                            # Bypass the interceptor
                            return behavior(
                                request_or_iterator, servicer_context
                            )

                        if request_streaming:
                            print("Received request is streaming.")

                        else:
                           print(f"Updating prometheus"
                                     f" metric grpc_server_started_total with"
                                     f" grpc_type: {grpc_type},"
                                     f" service_name: {grpc_service_name},"
                                     f" grpc_method_name: {grpc_method_name}")

                        # Invoke the original rpc behavior.
                        print(f"request_or_iterator: {request_or_iterator}")
                        response_or_iterator = behavior(
                            request_or_iterator, servicer_context
                        )
                        print(f"response_or_iterator:"
                                  f" {response_or_iterator}")

                        if response_streaming:
                            print("Response is streaming.")

                        else:
                            grpc_code = self._compute_status_code(
                                servicer_context)
                            print(f"Updating prometheus"
                                     f" metric grpc_server_handled_total with"
                                     f" grpc_type: {grpc_type},"
                                     f" grpc_code:{grpc_code}, "
                                     f" service_name: {grpc_service_name},"
                                     f" grpc_method_name: {grpc_method_name}")

                        return response_or_iterator

                    except grpc.RpcError as ex:
                        grpc_code = self._compute_error_code(ex).name
                        print(f"RPC execution failed, code:"
                                  f" {grpc_code}, error: {ex}")

                        raise ex

                except Exception as ex:
                    grpc_code = self._compute_error_code(ex).name
                    print(f"RPC common execution failed, code:"
                              f" {grpc_code}, error: {ex}")
                    print(f"Error in prometheus interceptor,"
                                  f" error:{ex}")
                    raise ex

            return new_behavior

        handler = await continuation(handler_call_details)
        optional_any = self._wrap_rpc_behavior(
            handler, metrics_wrapper
        )
        return optional_any

    def _wrap_rpc_behavior(self, handler, fn):
        """Returns a new rpc handler that wraps the given function"""
        if handler is None:
            return None

        if handler.request_streaming and handler.response_streaming:
            behavior_fn = handler.stream_stream
            handler_factory = grpc.stream_stream_rpc_method_handler
        elif handler.request_streaming and not handler.response_streaming:
            behavior_fn = handler.stream_unary
            handler_factory = grpc.stream_unary_rpc_method_handler
        elif not handler.request_streaming and handler.response_streaming:
            behavior_fn = handler.unary_stream
            handler_factory = grpc.unary_stream_rpc_method_handler
        else:
            behavior_fn = handler.unary_unary
            handler_factory = grpc.unary_unary_rpc_method_handler

        behaviour = fn(
            behavior_fn, handler.request_streaming, handler.response_streaming
        )

        return handler_factory(
            behaviour,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer
        )

    def _compute_status_code(self, servicer_context):
        #print(dir(servicer_context))
        status_code = ""
        # if len(grpc.StatusCode._member_names_) > servicer_context.code():
        #     status_code = \
        #         grpc.StatusCode._member_names_[servicer_context.code()]
        return status_code

    def _compute_error_code(self, grpc_exception):
        if isinstance(grpc_exception, grpc.Call):
            return grpc_exception.code()
        return grpc.StatusCode.UNKNOWN
