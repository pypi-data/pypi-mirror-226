"""
What is "Dependency Injection"   (Similar to decorator)
"Dependency Injection" means, in programming, that there is a way for your code
 (in this case, your path operation functions) to declare things that it requires
  to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever
 is needed to provide your code with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

Have shared logic (the same code logic again and again).
Share database connections.
Enforce security, authentication, role requirements, etc.
And many other things...


And it has the same shape and structure that all your path operation functions have.
"""


import uvicorn
from fastapi import FastAPI, APIRouter, Depends

PRODUCTS = []
for i in range(1, 101):
    PRODUCTS.append(
        {
            "id": i,
            "name": "Product-" + str(i),
            "price": i * 10
        })

router = APIRouter()


class QueryParams:
    def __init__(self, query: str = None, skip: int = 0, limit: int = 10):
        self.query = query
        self.skip = skip
        self.limit = limit


@router.get("/products")
async def get_products(query_params: QueryParams = Depends(QueryParams)):
    if query_params:
        return PRODUCTS[query_params.skip: query_params.limit]
    else:
        return PRODUCTS


if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router, prefix="/api/v1", tags=["dependency injection"])

    uvicorn.run(app, host='localhost', port=5002, log_level="info")


"""
http://localhost:5002/api/v1/products?skip=5
http://localhost:5002/api/v1/products?limit=5
http://localhost:5002/api/v1/products?skip=5&limit=15

"""