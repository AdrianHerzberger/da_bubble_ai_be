import uvicorn
from app.main import asgi_app

if __name__ == "__main__":
    uvicorn.run("app.main:asgi_app", host="127.0.0.1", port=5001, reload=True)

