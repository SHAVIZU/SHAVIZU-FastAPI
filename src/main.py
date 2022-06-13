from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from src.apps import api_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
