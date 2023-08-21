"""
https://realpython.com/fastapi-python-web-apis/#what-is-fastapi

FastAPI is a modern, high-performance web framework for building APIs
with Python based on standard type hints. It has the following key features:

Fast to run: It offers very high performance, on par with NodeJS and Go, thanks to Starlette and pydantic.
Fast to code: It allows for significant increases in development speed.
Reduced number of bugs: It reduces the possibility for human-induced errors.
Intuitive: It offers great editor support, with completion everywhere and less time debugging.
Straightforward: It’s designed to be uncomplicated to use and learn,
 so you can spend less time reading documentation.
Short: It minimizes code duplication.
Robust: It provides production-ready code with automatic interactive documentation.
Standards-based: It’s based on the open standards for APIs, OpenAPI and JSON Schema.
The framework is designed to optimize your developer experience so that you can write simple code to build production-ready APIs with best practices by default.
"""


from fastapi import FastAPI
import uvicorn

app = FastAPI()  # An instance of the class FastAPI.
# This will be the main point of interaction to create your API.
# This app is the one you referred to in the command to run the live server with


@app.get("/")
async def root():
    return {"message": "Hello world"}
    #  You can return a dictionary, list, or singular values as strings,
    #  integers, and so on. You can also return pydantic models

# The @app.get("/") tells FastAPI that the function right below is in charge of
# handling requests that go to the path / using a get operation.
# This is a decorator related to a path operation, or a path operation decorator.


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=9002, log_level="debug")  # OR use uvicorn.exe first_exp:app --reload

"""
pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 uvicorn

Above code defines your application, but it won’t run on itself if you call it with python directly.
To run it, you need a server program. In the steps above, you already installed Uvicorn. That will be your server.

Run the live server using Uvicorn: Before run install fastapi and uvicorn
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/fast_api_exp
$ uvicorn.exe first_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\fast_api_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [34628] using statreload
INFO:     Started server process [110172]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


# Browse: http://127.0.0.1:8000/
{"message":"Hello world"}


 FastAPI takes care of serializing the Python dict into a JSON object and setting the appropriate Content-Type.

Check the Interactive API Documentation
Now open http://127.0.0.1:8000/docs in your browser.

You will see the automatic interactive API documentation provided by Swagger UI:


The web-based user interface documenting your API is provided and integrated by default.
 You don’t have to do anything else to take advantage of it with FastAPI.

Check the Alternative Interactive API Documentation
Now, go to http://127.0.0.1:8000/redoc in your browser.

You’ll see the alternative automatic documentation provided by ReDoc:


As FastAPI is based on standards like OpenAPI, there are many alternative ways to show the API documentation.
FastAPI provides these two alternatives by default.

Install:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/github-repos/atlas/dm-virt-api (dev)
$ pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 fastapi
Collecting fastapi
  Downloading https://files.pythonhosted.org/packages/df/44/ee1976b03404318590bbe4b0ef27007ce2c42b15757aa0c72bc99a4ebae7/fastapi-0.68.1-py3-none-any.whl (52kB)
Collecting pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2
  Downloading https://files.pythonhosted.org/packages/ff/74/54e030641601112309f6d2af620774e9080f99c7a15742fc6a0b170c4076/pydantic-1.8.2-py3-none-any.whl (126kB)
Collecting starlette==0.14.2
  Downloading https://files.pythonhosted.org/packages/15/34/db1890f442a1cd3a2c761f4109a0eb4e63503218d70a8c8e97faa09a5500/starlette-0.14.2-py3-none-any.whl (60kB)
Collecting dataclasses>=0.6; python_version < "3.7"
  Downloading https://files.pythonhosted.org/packages/fe/ca/75fac5856ab5cfa51bbbcefa250182e50441074fdc3f803f6e76451fab43/dataclasses-0.8-py3-none-any.whl
Collecting typing-extensions>=3.7.4.3
  Downloading https://files.pythonhosted.org/packages/74/60/18783336cc7fcdd95dae91d73477830aa53f5d3181ae4fe20491d7fc3199/typing_extensions-3.10.0.2-py3-none-any.whl
Installing collected packages: dataclasses, typing-extensions, pydantic, starlette, fastapi
  Found existing installation: typing-extensions 3.7.4.1
    Uninstalling typing-extensions-3.7.4.1:
      Successfully uninstalled typing-extensions-3.7.4.1
Successfully installed dataclasses-0.8 fastapi-0.68.1 pydantic-1.8.2 starlette-0.14.2 typing-extensions-3.10.0.2
WARNING: You are using pip version 19.3.1; however, version 21.2.4 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/github-repos/atlas/dm-virt-api (dev)
$ pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 uvicorn
Collecting uvicorn
  Downloading https://files.pythonhosted.org/packages/6f/d0/2c2f4e88d63a8f8891419ca02e029e3a7200ab8f64a3628517cf35ff0379/uvicorn-0.15.0-py3-none-any.whl (54kB)
Collecting h11>=0.8
  Downloading https://files.pythonhosted.org/packages/60/0f/7a0eeea938eaf61074f29fed9717f2010e8d0e0905d36b38d3275a1e4622/h11-0.12.0-py3-none-any.whl (54kB)
Collecting asgiref>=3.4.0
  Downloading https://files.pythonhosted.org/packages/fe/66/577f32b54c50dcd8dec38447258e82ed327ecb86820d67ae7b3dea784f13/asgiref-3.4.1-py3-none-any.whl
Requirement already satisfied: click>=7.0 in c:\python3\lib\site-packages (from uvicorn) (7.0)
Requirement already satisfied: typing-extensions; python_version < "3.8" in c:\python3\lib\site-packages (from uvicorn) (3.10.0.2)
Installing collected packages: h11, asgiref, uvicorn
  Found existing installation: asgiref 3.2.3
    Uninstalling asgiref-3.2.3:
      Successfully uninstalled asgiref-3.2.3
Successfully installed asgiref-3.4.1 h11-0.12.0 uvicorn-0.15.0
WARNING: You are using pip version 19.3.1; however, version 21.2.4 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.


"""