from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ai_agent_ecommerce.api.routes import router

app = FastAPI()
app.include_router(router)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def root():
    return {"message": "AI E-commerce Agent Running"}
