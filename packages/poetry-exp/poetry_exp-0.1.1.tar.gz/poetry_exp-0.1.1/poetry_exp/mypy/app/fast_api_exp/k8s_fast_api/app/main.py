from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users():
    return [{'id': 1, 'name': 'User1'}, {'id':2, 'name': "User2"}]
