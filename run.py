import os
import uvicorn
from app.main import asgi_app

if __name__ == "__main__":
    #uvicorn.run("app.main:asgi_app", host="127.0.0.1", port=5000, reload=True)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:asgi_app", host="0.0.0.0", port=port)

