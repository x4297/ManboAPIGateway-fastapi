from fastapi import FastAPI
import uvicorn

from routers import router
from settings import CommonConfig


app = FastAPI(openapi_url="/openapi.json" if CommonConfig.debug else None)
app.mount("/", router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=CommonConfig.host, port=CommonConfig.port, workers=CommonConfig.workers)
