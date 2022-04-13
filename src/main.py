from fastapi import FastAPI

import uvicorn

from src.apps import product


app = FastAPI()

app.include_router(product.router)


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
