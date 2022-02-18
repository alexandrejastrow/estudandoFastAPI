import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

tempo = {"conta": 0,"tempo": 0}
class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            tempo['conta'] += 1
            tempo['tempo'] += duration
            response.headers["X-Response-Time"] = str(duration)
            print(tempo)
            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=TimedRoute)


@app.get("/")
async def not_timed():
    return {"message": "Not timed"}


@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}


app.include_router(router)


#
#while(true){fetch('http://localhost:8000/timed',{method:'get'}).then()}