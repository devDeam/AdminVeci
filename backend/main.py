from fastapi import FastAPI
from api.tenants import router as tenants_router
from api.auth import router as auth_router

app = FastAPI()
@app.get('/')
async def Home():
    return {"message": "API FUNCIONANDO"}

app.include_router(tenants_router)
app.include_router(auth_router)
