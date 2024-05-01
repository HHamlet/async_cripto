from fastapi import FastAPI
from v1.router import router as router_api
import uvicorn

app = FastAPI()
app.include_router(router_api)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
