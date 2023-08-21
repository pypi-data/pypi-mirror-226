from fastapi import FastAPI
import uvicorn
import uuid

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Project": "Data Center Management API",
        "version": "1.0",
        "author": "Aafak Mohammad",
        "email": "aafak.mitsmca09@gmail.com"
    }


@app.get("/virtual-machines")
def read_item():
    return [{"id": str(uuid.uuid4()), "name": "windows_vm"}, {"id": str(uuid.uuid4()), "name": "linux_vm"}]


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=9002)


"""


"""