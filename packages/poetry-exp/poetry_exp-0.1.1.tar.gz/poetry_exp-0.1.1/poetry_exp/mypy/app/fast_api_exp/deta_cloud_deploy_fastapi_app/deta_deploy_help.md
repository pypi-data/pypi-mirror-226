https://fastapi.tiangolo.com/deployment/deta/#__tabbed_1_2

Install deta cli from powershell:
PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise>iwr https://get.deta.dev/cli.ps1 -useb | iex

Create new Account in deta:
https://web.deta.sh/home/aafakcb32/default/micros
psw: @CB32

Login deta:
PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise> deta login

PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\deta_cloud_deploy_fastapi_app> deta new
Successfully created a new micro
{
        "name": "deta_cloud_deploy_fastapi_app",
        "id": "d2dfde42-dd66-4502-9cdb-933f88e6bca9",
        "project": "d0rayprx",
        "runtime": "python3.9",
        "endpoint": "https://y35njl.deta.dev",
        "region": "ap-south-1",
        "visor": "disabled",
        "http_auth": "disabled"
}
Adding dependencies...
Collecting fastapi
  Downloading https://files.pythonhosted.org/packages/56/c7/e36aa8a7a04a2536b559abd7ced3a69fbabb324b27911b7a4c50276167cf/fastapi-0.82.0-py3-none-any.whl (55kB)
Collecting uvicorn
  Downloading https://files.pythonhosted.org/packages/64/82/3fdff66fca901b30e42c88e0c37ada35e181074e0c4fd8d7d7525107329d/uvicorn-0.18.3-py3-none-any.whl (57kB)
Collecting starlette==0.19.1
  Downloading https://files.pythonhosted.org/packages/f1/9d/1fa96008b302dd3e398f89f3fc5afb19fb0b0f341fefa05c65b3a38d64cf/starlette-0.19.1-py3-none-any.whl (63kB)
Collecting pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2
  Downloading https://files.pythonhosted.org/packages/4c/5f/11db15638a3f5b29c7ae6f24b43c1e7985f09b0fe983621d7ef1ff722020/pydantic-1.10.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.2MB)
Collecting click>=7.0
  Downloading https://files.pythonhosted.org/packages/c2/f1/df59e28c642d583f7dacffb1e0965d0e00b218e0186d7858ac5233dce840/click-8.1.3-py3-none-any.whl (96kB)
Collecting h11>=0.8
  Downloading https://files.pythonhosted.org/packages/19/d2/32a15a4955be1b8114a1c570999eefd31279c7f9aa2d2a43d492a79b53c5/h11-0.13.0-py3-none-any.whl (58kB)
Collecting typing-extensions>=3.10.0; python_version < "3.10"
  Downloading https://files.pythonhosted.org/packages/ed/d6/2afc375a8d55b8be879d6b4986d4f69f01115e795e36827fd3a40166028b/typing_extensions-4.3.0-py3-none-any.whl
Collecting anyio<5,>=3.4.0
  Downloading https://files.pythonhosted.org/packages/c3/22/4cba7e1b4f45ffbefd2ca817a6800ba1c671c26f288d7705f20289872012/anyio-3.6.1-py3-none-any.whl (80kB)
Collecting idna>=2.8
  Downloading https://files.pythonhosted.org/packages/04/a2/d918dcd22354d8958fe113e1a3630137e0fc8b44859ade3063982eacd2a4/idna-3.3-py3-none-any.whl (61kB)
Collecting sniffio>=1.1
  Downloading https://files.pythonhosted.org/packages/c3/a0/5dba8ed157b0136607c7f2151db695885606968d1fae123dc3391e0cfdbf/sniffio-1.3.0-py3-none-any.whl
Installing collected packages: typing-extensions, idna, sniffio, anyio, starlette, pydantic, fastapi, click, h11, uvicorn
Successfully installed anyio-3.6.1 click-8.1.3 fastapi-0.82.0 h11-0.13.0 idna-3.3 pydantic-1.10.2 sniffio-1.3.0 starlette-0.19.1 typing-extensions-4.3.0 uvicorn-0.18.3
You should consider upgrading via the 'pip install --upgrade pip' command.

PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\deta_cloud_deploy_fastapi_app>


Now Browse:
https://y35njl.deta.dev
https://y35njl.deta.dev/docs
https://y35njl.deta.dev/items/1