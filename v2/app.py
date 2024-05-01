from fastapi import FastAPI
from v2.router import router as router_v2
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router_v2)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
