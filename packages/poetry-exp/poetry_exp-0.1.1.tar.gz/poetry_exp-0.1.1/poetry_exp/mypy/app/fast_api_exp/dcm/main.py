from fastapi import FastAPI
import uvicorn

from app.routes import users, login, hypervisor_managers

app = FastAPI()

deta_project_key = "d0rayprx_zqvkEnvbaVask8GoSX3SaDxAEi1H1Wkj"

@app.get("/", tags=["About"])
async def about():
    #create_db_file()

    return {
        "Project": "Data Center Management Server API",
        "version": "1.0",
        "author": "Aafak Mohammad",
        "email": "aafak.mitsmca09@gmail.com"
    }


app.include_router(router=users.router, tags=["Users"])
app.include_router(router=login.router, tags=["Login"])
app.include_router(router=hypervisor_managers.router, tags=["Hypervisor Managers"])


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8001)