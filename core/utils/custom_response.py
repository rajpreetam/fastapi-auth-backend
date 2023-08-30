from fastapi.responses import JSONResponse
from typing import Any


class CustomResponse:
    def __init__(self, success: bool, status_code: int, data: Any, message: str):
        self.success = success
        self.status_code = status_code
        self.data = data
        self.message = message

    def json_response(self):
        return JSONResponse({
            'success': self.success,
            'status_code': self.status_code,
            'data': self.data,
            'message': self.message
        }, status_code=self.status_code)
