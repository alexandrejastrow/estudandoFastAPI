from fastapi import Depends, FastAPI, BackgroundTasks, Request

#from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from infra import crud, models, schemas
from infra.database import get_db, engine
from routes.routes import Routers
from routes.rotaYaml import yamlRoute
from routes.outrarota import novaRota
from routes.cokiesss import rou



from random import randint, randbytes
from time import sleep
from infos import metadata



models.Base.metadata.create_all(bind=engine)



app = FastAPI(
    dependencies=[Depends(get_db)],
    title=metadata.Title,
    description=metadata.Description,
    version=metadata.__version__,
    terms_of_service=metadata.Terms_if_service,
    contact=metadata.Contact,
    license_info=metadata.Licenses,
    tags_metadata=[
        metadata.User_tag,
        metadata.Items_tag
    ],
    openapi_url="/api/v1/openapi.json",
    docs_url="/documentation", 
    redoc_url=None
)


app.include_router(rou)
app.include_router(yamlRoute)
app.include_router(novaRota)
app.include_router(
    Routers,
    prefix='/api',
    dependencies=[Depends(get_db)]
)

#app.mount("/static", StaticFiles(directory="static"), name="static")


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        a = randbytes(24)
        sleep(randint(1, 15))
        log.write(message + ",  " + str(a.hex()) + '\n')


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/", tags=['items'])
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)

    return {"message": "Message sent"}


############## include_in_schema=False tira da documentação
@app.get("/items/", response_model=list[schemas.Item], tags=['items'], include_in_schema=False, operation_id="essa eh uma rota de id")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


from fastapi.routing import APIRoute

#testessss#######################
@app.get("/", operation_id="definindo alguma coisa de id unico", )
async def read_main():
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return {"msg": "Hello World"}


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            
            route.operation_id = route.name 

use_route_names_as_operation_ids(app)



@app.get('/it01/{item_it}')
async def read_rot(item_id: str, req: Request):
    cli_host = req.client.host
    return {"client_host": cli_host, "item_id": item_id}

#################################################################

from dataclasses import dataclass, field
from typing import List

@dataclass
class It:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)


@app.post('/it-class', response_model=It)
async def cria_it():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "tags": ["breater"],
    }




import uvicorn

if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=8, reload=True)

#