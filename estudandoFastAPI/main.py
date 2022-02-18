from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="templates")

templates = Jinja2Templates(directory="templates")


fake_users_db = {
    "eu": {
        "username": "eu",
        "full_name": "John Doe",
        "email": "eu@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": False,
    },
    "John": {
        "username": "eu2",
        "full_name": "eu2 Chains",
        "email": "eu2@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": True,
    },
    "Doe": {
        "username": "eu",
        "full_name": "John Doe",
        "email": "eu@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": False,
    },
    "Chains": {
        "username": "eu2",
        "full_name": "eu2 Chains",
        "email": "eu2@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": True,
    },
}


@app.get("/item/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id, "users": fake_users_db})