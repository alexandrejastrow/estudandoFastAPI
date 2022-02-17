from fastapi import Request,HTTPException, APIRouter, status, Response
from pydantic import ValidationError, BaseModel
from typing import List
import yaml
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    name: str
    tags: List[str]

yamlRoute = APIRouter()

@yamlRoute.post(
    "/itemss/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.schema()}},
            "required": True,
        },
    },
)
async def create_items(request: Request):
    raw_body = await request.body()

    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.parse_obj(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    it = {"name": item.name, "tag": f'{item.tags}'}

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=it)

@yamlRoute.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)

@yamlRoute.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")