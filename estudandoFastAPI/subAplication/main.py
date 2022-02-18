from fastapi import FastAPI, Request


app = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path_in_servers=False
)

@app.get("/app")
async def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


subApp = FastAPI()
app.mount('/subapi', subApp)


@subApp.get('/subapp')
async def read_sub_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


