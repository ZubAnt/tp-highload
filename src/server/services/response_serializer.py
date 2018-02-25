from models.response import Response
from models.status_codes import StatusCodes


class ResponseSerializer(object):

    @staticmethod
    def dump(response: Response) -> str:
        if response.status_code == StatusCodes.OK:
            return ResponseSerializer._success_response(response)
        else:
            return ResponseSerializer._error_response(response)

    @staticmethod
    def _success_response(response: Response) -> str:
        return f"HTTP/{response.protocol} {response.status_code.value}\r\n" \
               f"Content-Type: {response.content_type}\r\n" \
               f"Content-Length: {response.content_length}\r\n" \
               f"Date: {response.date.strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n" \
               f"Server: Server\r\n\r\n"

    @staticmethod
    def _error_response(response: Response) -> str:
        return f"HTTP/{response.protocol} {response.status_code.value}\r\n" \
               f"Server: Server\r\n\r\n"
