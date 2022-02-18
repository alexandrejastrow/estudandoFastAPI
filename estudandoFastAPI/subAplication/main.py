from fastapi import FastAPI


app = FastAPI()

@app.get("/app")
async def read_main():
    return {"message":"ola mundo"}


subApp = FastAPI()

@subApp.get('/subapp')
async def read_sub_main():
    return {"message":"ola mundo do dub main"}

app.mount('/subapi', subApp)

