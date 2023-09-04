from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.utils.schemas.custom_response_schema import CustomResponseModel
from core.utils.custom_exceptions import InternalServerError
from core.utils.custom_response import CustomResponse
from accounts.routers import router as auth_router

app = FastAPI()


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return JSONResponse({
        'success': exc.success,
        'status_code': exc.status_code,
        'data': exc.data,
        'message': exc.message
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse({
        'success': False,
        'status_code': exc.status_code,
        'data': None,
        'message': exc.detail
    }, status_code=exc.status_code)


origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get('/', response_model=CustomResponseModel, status_code=200)
async def root():
    response = CustomResponse(True, 200, None, 'Success')
    try:
        return response
    except Exception as e:
        print(e)
        raise InternalServerError
