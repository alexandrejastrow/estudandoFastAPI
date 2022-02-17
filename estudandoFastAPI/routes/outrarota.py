from fastapi import APIRouter
from fastapi.responses import (
    ORJSONResponse, 
    HTMLResponse, 
    RedirectResponse, 
    StreamingResponse,
    FileResponse,
    JSONResponse
    )
from pydantic import BaseModel
from pytest import Item


from static import index

novaRota = APIRouter()

responses = {
    404: {"description": "Item not found", 'content':{
        'application/json':{
            'example':{
                'item_id': 'iditem',
                'value': '5525'
            }
        }
    }},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@novaRota.get("/ola", response_class=ORJSONResponse)
async def read_rota():
    return [{"item": "foo"}]

@novaRota.get("/ola2", response_class=HTMLResponse)
async def read_rota2():
    return HTMLResponse(content=index.index, status_code=200)


@novaRota.get("/ola3")
async def read_rota3():

    with open("/home/jastrow/Projects/estudando/estudando/static/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@novaRota.get("/ola4", response_class=RedirectResponse, status_code=302)
async def read_rota4():
    return "https://www.linkedin.com/in/alexandre-jastrow-da-cruz-266a99150/"


file_path = "/home/jastrow/Projects/estudando/estudando/static/02 - Preparação e Primeiros Clientes.mp4"

def interfile():   
    with open(file_path, "rb") as f:
        yield f.read()


@novaRota.get("/ola5")
async def read_rota5():
    return StreamingResponse(interfile(), media_type="video/mp4")


@novaRota.get("/ola6")
async def read_rota6():
    return FileResponse(file_path)


class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

@novaRota.get('/ola7/{item_id}', 
response_model=Item, responses={404: {"model": Message}})
async def novoModel(item_id: str):
    if item_id == 'foo':
        return {"id": "foo", "value": "there goes my hero"}
    
    return JSONResponse(status_code=404, content={'message': 'deu ruim'})


@novaRota.get('/ola8/{item_id}', 
response_model=Item, responses={200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }})
async def novoModel2(item_id: str, img: bool | None = None):
    
    if img:
        return FileResponse('estudando/routes/facu.png', media_type='image/png')
    
    return JSONResponse(status_code=404, content={'message': item_id})


@novaRota.get(
    '/ola9/{item_id}',
    response_model=Item,
    responses={
        404: {
            'model': Message,
             'description': 'the item nao achou'
             },
        200: {
            'description': 'item achado pelo ID',
            'content':{
                'application/json':{
                    'example': {
                        'id': 'bar',
                         'value':'the bar tender'
                         }
                }
            }
        },
        201: {
            'model': Item,
            'description': 'criando item',
             'content':{
                 'application/json':{
                     'example':{
                         'id': 'bar',
                         'value': 'deu'
                     }
                 }
             }
        }
    }
    
    )
async def modelo3(item_id:str):
    if item_id == 'foo':
        return {'id': 'foo', 'value': 'there goes my hero'}
    elif item_id =='bar':
        return JSONResponse(status_code=201, content={'id': 'bar', 'value': 'bar'})
    return JSONResponse(status_code=404, content={'message': 'item not found'})

@novaRota.get(
    "/ola10/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("estudando/routes/facu.png", media_type="image/png")
    elif item_id == '222':
        return JSONResponse(status_code=404, content={'message': 'item not found'})
    else:
        return {"id": "foo", "value": "there goes my hero"}