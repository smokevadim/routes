from starlette.requests import Request
from starlette.responses import JSONResponse


async def catch_error(request: Request, call_next):
    """Middleware to catch errors and response details to client"""

    try:
        return await call_next(request)
    except Exception as e:
        body = {'detail': e.args[0]}
        return JSONResponse(body, status_code=500)
