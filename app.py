from app_factory import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":

    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
