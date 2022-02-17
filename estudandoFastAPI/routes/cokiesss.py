
from fastapi import Depends, Response, APIRouter, status
from fastapi.responses import JSONResponse


rou = APIRouter()

class CheckQuery:

    def __init__(self, context: str) -> None:
        self.context = context
    
    def __call__(self, q: str = "") -> any:
        if q:
            return self.context in q
        return False

checker = CheckQuery('bar')


@rou.get('/query-check')
async def read_query(fixed_content_include: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_include}

@rou.get('/ola-cookie')
def create_cookie(res: Response):

    cont = {"message":"qualquer coisa que tem um cookie"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    res = JSONResponse(content=cont, headers=headers)
    res.set_cookie(key="fake-session", value='fake-cookie-session-value')
    res.set_cookie(key="fake-session2", value='fake-cookie-session-value2')
    res.status_code = status.HTTP_201_CREATED
    return res