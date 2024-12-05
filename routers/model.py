import traceback
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class MyHTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


async def my_exception_handler(request: Request, exc: MyHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, 
                 "message": exc.message, 
                 "result": None}
    )
def reply_success(message, result):
    return  {
                "status_code": 200,
                "message": message,
                "result": result
                }

def reply_server_error(message):
    return {
            "status_code": 500,
            "message": str(message) + "Trace back: " + str(traceback.format_exc()),
            "result": None
            }

def reply_bad_request(message):
    return {
            "status_code": 400,
            "message": message,
            "result": None
            }