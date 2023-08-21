aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise
$ python -m virtualenv fastapi_venv
created virtual environment CPython3.6.5.final.0-32 in 6745ms
  creator CPython3Windows(dest=C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\fastapi_venv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\aafakmoh\AppData\Local\pypa\virtualenv)
    added seed packages: pip==21.3.1, setuptools==59.6.0, wheel==0.37.1
  activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/fastapi_venv
$ source Scripts/activate
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/fastapi_venv
$

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp
$ mkdir dcm
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp
$ cd dcm/
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$


aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install fastapi --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting fastapi
  Downloading fastapi-0.82.0-py3-none-any.whl (55 kB)
Collecting pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2
  Downloading pydantic-1.9.2-py3-none-any.whl (143 kB)
Collecting starlette==0.19.1
  Downloading starlette-0.19.1-py3-none-any.whl (63 kB)
Collecting anyio<5,>=3.4.0
  Downloading anyio-3.6.1-py3-none-any.whl (80 kB)
Collecting typing-extensions>=3.10.0
  Downloading typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Collecting contextlib2>=21.6.0
  Downloading contextlib2-21.6.0-py2.py3-none-any.whl (13 kB)
Collecting dataclasses>=0.6
  Using cached dataclasses-0.8-py3-none-any.whl (19 kB)
Collecting idna>=2.8
  Downloading idna-3.3-py3-none-any.whl (61 kB)
Collecting contextvars
  Downloading contextvars-2.4.tar.gz (9.6 kB)
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Collecting sniffio>=1.1
  Downloading sniffio-1.2.0-py3-none-any.whl (10 kB)
Collecting immutables>=0.9
  Downloading immutables-0.18-cp36-cp36m-win32.whl (54 kB)
Building wheels for collected packages: contextvars
  Building wheel for contextvars (setup.py): started
  Building wheel for contextvars (setup.py): finished with status 'done'
  Created wheel for contextvars: filename=contextvars-2.4-py3-none-any.whl size=7681 sha256=02995e6adba475a28a73fb6112938012812af9797b929dedc30e9add0949678c
  Stored in directory: c:\users\aafakmoh\appdata\local\pip\cache\wheels\41\11\53\911724983aa48deb94792432e14e518447212dd6c5477d49d3
Successfully built contextvars
Installing collected packages: typing-extensions, immutables, contextvars, sniffio, idna, dataclasses, contextlib2, anyio, starlette, pydantic, fastapi
Successfully installed anyio-3.6.1 contextlib2-21.6.0 contextvars-2.4 dataclasses-0.8 fastapi-0.82.0 idna-3.3 immutables-0.18 pydantic-1.9.2 sniffio-1.2.0 starlette-0.19.1 typing-extensions-4.1.1
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install uvicorn --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting uvicorn
  Downloading uvicorn-0.16.0-py3-none-any.whl (54 kB)
Requirement already satisfied: typing-extensions in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from uvicorn) (4.1.1)
Collecting h11>=0.8
  Downloading h11-0.13.0-py3-none-any.whl (58 kB)
Collecting click>=7.0
  Downloading click-8.0.4-py3-none-any.whl (97 kB)
Collecting asgiref>=3.4.0
  Using cached asgiref-3.4.1-py3-none-any.whl (25 kB)
Collecting importlib-metadata
  Downloading importlib_metadata-4.8.3-py3-none-any.whl (17 kB)
Collecting colorama
  Downloading colorama-0.4.5-py2.py3-none-any.whl (16 kB)
Requirement already satisfied: dataclasses in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from h11>=0.8->uvicorn) (0.8)
Collecting zipp>=0.5
  Downloading zipp-3.6.0-py3-none-any.whl (5.3 kB)
Installing collected packages: zipp, importlib-metadata, colorama, h11, click, asgiref, uvicorn
Successfully installed asgiref-3.4.1 click-8.0.4 colorama-0.4.5 h11-0.13.0 importlib-metadata-4.8.3 uvicorn-0.16.0 zipp-3.6.0
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install sqlalchemy --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting sqlalchemy
  Downloading SQLAlchemy-1.4.41-cp36-cp36m-win32.whl (1.6 MB)
Requirement already satisfied: importlib-metadata in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from sqlalchemy) (4.8.3)
Collecting greenlet!=0.4.17
  Downloading greenlet-1.1.3-cp36-cp36m-win32.whl (98 kB)
Requirement already satisfied: typing-extensions>=3.6.4 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from importlib-metadata->sqlalchemy) (4.1.1)
Requirement already satisfied: zipp>=0.5 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from importlib-metadata->sqlalchemy) (3.6.0)
Installing collected packages: greenlet, sqlalchemy
Successfully installed greenlet-1.1.3 sqlalchemy-1.4.41
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install passlib --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting passlib
  Downloading passlib-1.7.4-py2.py3-none-any.whl (525 kB)
Installing collected packages: passlib
Successfully installed passlib-1.7.4
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install bcrypt --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting bcrypt
  Downloading bcrypt-4.0.0-cp36-abi3-win32.whl (159 kB)
Installing collected packages: bcrypt
Successfully installed bcrypt-4.0.0
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install python-jose --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting python-jose
  Using cached python_jose-3.3.0-py2.py3-none-any.whl (33 kB)
Collecting ecdsa!=0.15
  Downloading ecdsa-0.18.0-py2.py3-none-any.whl (142 kB)
Collecting pyasn1
  Using cached pyasn1-0.4.8-py2.py3-none-any.whl (77 kB)
Collecting rsa
  Downloading rsa-4.9-py3-none-any.whl (34 kB)
Collecting six>=1.9.0
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, pyasn1, rsa, ecdsa, python-jose
Successfully installed ecdsa-0.18.0 pyasn1-0.4.8 python-jose-3.3.0 rsa-4.9 six-1.16.0
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install alembic --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting alembic
  Downloading alembic-1.7.7-py3-none-any.whl (210 kB)
Requirement already satisfied: importlib-metadata in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from alembic) (4.8.3)
Requirement already satisfied: SQLAlchemy>=1.3.0 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from alembic) (1.4.41)
Collecting importlib-resources
  Using cached importlib_resources-5.4.0-py3-none-any.whl (28 kB)
Collecting Mako
  Downloading Mako-1.1.6-py2.py3-none-any.whl (75 kB)
Requirement already satisfied: greenlet!=0.4.17 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from SQLAlchemy>=1.3.0->alembic) (1.1.3)
Requirement already satisfied: zipp>=0.5 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from importlib-metadata->alembic) (3.6.0)
Requirement already satisfied: typing-extensions>=3.6.4 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from importlib-metadata->alembic) (4.1.1)
Collecting MarkupSafe>=0.9.2
  Downloading MarkupSafe-2.0.1-cp36-cp36m-win32.whl (14 kB)
Installing collected packages: MarkupSafe, Mako, importlib-resources, alembic
Successfully installed Mako-1.1.6 MarkupSafe-2.0.1 alembic-1.7.7 importlib-resources-5.4.0
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 install python-multipart --proxy=http://web-proxy.in.hpecorp.net:8080
Collecting python-multipart
  Downloading python-multipart-0.0.5.tar.gz (32 kB)
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Requirement already satisfied: six>=1.4.0 in c:\users\aafakmoh\onedrive - hewlett packard enterprise\fastapi_venv\lib\site-packages (from python-multipart) (1.16.0)
Building wheels for collected packages: python-multipart
  Building wheel for python-multipart (setup.py): started
  Building wheel for python-multipart (setup.py): finished with status 'done'
  Created wheel for python-multipart: filename=python_multipart-0.0.5-py3-none-any.whl size=31678 sha256=2786d09e9c5287b51fc7f7dda1e456de7771c9b0b9f3060a5e4b441d80e817c6
  Stored in directory: c:\users\aafakmoh\appdata\local\pip\cache\wheels\42\f2\ed\1e45bd5dd2eeb2c2a23e78e00e98ec2151195c4d66d732c0f9
Successfully built python-multipart
Installing collected packages: python-multipart
Successfully installed python-multipart-0.0.5
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm


aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ pip3 freeze > requirements.txt
(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ cat requirements.txt
alembic==1.7.7
anyio==3.6.1
asgiref==3.4.1
bcrypt==4.0.0
click==8.0.4
colorama==0.4.5
contextlib2==21.6.0
contextvars==2.4
dataclasses==0.8
ecdsa==0.18.0
fastapi==0.82.0
greenlet==1.1.3
h11==0.13.0
idna==3.3
immutables==0.18
importlib-metadata==4.8.3
importlib-resources==5.4.0
Mako==1.1.6
MarkupSafe==2.0.1
passlib==1.7.4
pyasn1==0.4.8
pydantic==1.9.2
python-jose==3.3.0
python-multipart==0.0.5
rsa==4.9
six==1.16.0
sniffio==1.2.0
SQLAlchemy==1.4.41
starlette==0.19.1
typing_extensions==4.1.1
uvicorn==0.16.0
zipp==3.6.0

(fastapi_venv)
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$


aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/dcm
$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\fast_api_exp\\dcm']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12232] using statreload
INFO:     Started server process [3436]
INFO:     Waiting for application startup.
INFO:     Application startup complete.




IN powershell:

PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\dcm> ls


    Directory: C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\dcm


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
da---l         9/8/2022  12:07 PM                app
da---l         9/8/2022   2:56 PM                __pycache__
-a---l         9/8/2022   3:53 PM          20480 dcm.db
-a----         9/8/2022   3:57 PM            651 main.py
-a----         9/8/2022   3:56 PM            554 requirements.txt
-a---l        9/16/2021   2:03 PM              0 __init__.py


PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\dcm> deta new
Successfully created a new micro
{
        "name": "dcm",
        "id": "2486b24d-379e-4894-aac9-350798818a1b",
        "project": "d0rayprx",
        "runtime": "python3.9",
        "endpoint": "https://89tixy.deta.dev",
        "region": "ap-south-1",
        "visor": "disabled",
        "http_auth": "disabled"
}
Adding dependencies...
Collecting alembic==1.7.7
  Downloading https://files.pythonhosted.org/packages/b3/e2/8d48220731b7279911c43e95cd182961a703b939de6822b00de3ea0d3159/alembic-1.7.7-py3-none-any.whl (210kB)
Collecting anyio==3.6.1
  Downloading https://files.pythonhosted.org/packages/c3/22/4cba7e1b4f45ffbefd2ca817a6800ba1c671c26f288d7705f20289872012/anyio-3.6.1-py3-none-any.whl (80kB)
Collecting asgiref==3.4.1
  Downloading https://files.pythonhosted.org/packages/fe/66/577f32b54c50dcd8dec38447258e82ed327ecb86820d67ae7b3dea784f13/asgiref-3.4.1-py3-none-any.whl
Collecting bcrypt==4.0.0
  Downloading https://files.pythonhosted.org/packages/c5/77/14bbcd08ad265577ad6ea8e8980b9c0ad668cecfd241ae169b6747c4491b/bcrypt-4.0.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (594kB)
Collecting click==8.0.4
  Downloading https://files.pythonhosted.org/packages/4a/a8/0b2ced25639fb20cc1c9784de90a8c25f9504a7f18cd8b5397bd61696d7d/click-8.0.4-py3-none-any.whl (97kB)
Collecting colorama==0.4.5
  Downloading https://files.pythonhosted.org/packages/77/8b/7550e87b2d308a1b711725dfaddc19c695f8c5fa413c640b2be01662f4e6/colorama-0.4.5-py2.py3-none-any.whl
Collecting contextlib2==21.6.0
  Downloading https://files.pythonhosted.org/packages/76/56/6d6872f79d14c0cb02f1646cbb4592eef935857c0951a105874b7b62a0c3/contextlib2-21.6.0-py2.py3-none-any.whl
Collecting contextvars==2.4
  Downloading https://files.pythonhosted.org/packages/83/96/55b82d9f13763be9d672622e1b8106c85acb83edd7cc2fa5bc67cd9877e9/contextvars-2.4.tar.gz
ERROR: Could not find a version that satisfies the requirement dataclasses==0.8 (from versions: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
ERROR: No matching distribution found for dataclasses==0.8
You should consider upgrading via the 'pip install --upgrade pip' command.


Error: failed to update dependecies: error on one or more dependencies, no dependencies were added, see output for details




PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\dcm> deta deploy
Deploying...
Successfully deployed changes
Updating dependencies...
Collecting fastapi
  Downloading https://files.pythonhosted.org/packages/56/c7/e36aa8a7a04a2536b559abd7ced3a69fbabb324b27911b7a4c50276167cf/fastapi-0.82.0-py3-none-any.whl (55kB)
Collecting uvicorn
  Downloading https://files.pythonhosted.org/packages/64/82/3fdff66fca901b30e42c88e0c37ada35e181074e0c4fd8d7d7525107329d/uvicorn-0.18.3-py3-none-any.whl (57kB)
Collecting SQLAlchemy
  Downloading https://files.pythonhosted.org/packages/ce/b7/1b65516236b36b55624768f7923c9a8d55ca4ba239b795ea84cb82086718/SQLAlchemy-1.4.41-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.6MB)
Collecting passlib
  Downloading https://files.pythonhosted.org/packages/3b/a4/ab6b7589382ca3df236e03faa71deac88cae040af60c071a78d254a62172/passlib-1.7.4-py2.py3-none-any.whl (525kB)
Collecting bcrypt
  Downloading https://files.pythonhosted.org/packages/c5/77/14bbcd08ad265577ad6ea8e8980b9c0ad668cecfd241ae169b6747c4491b/bcrypt-4.0.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (594kB)
Collecting alembic
  Downloading https://files.pythonhosted.org/packages/b3/c8/69600a8138a56794713ecdb8b75b14fbe32a410bc444683f27dbab93c0ca/alembic-1.8.1-py3-none-any.whl (209kB)
Collecting python-jose
  Downloading https://files.pythonhosted.org/packages/bd/2d/e94b2f7bab6773c70efc70a61d66e312e1febccd9e0db6b9e0adf58cbad1/python_jose-3.3.0-py2.py3-none-any.whl
Collecting python-multipart
  Downloading https://files.pythonhosted.org/packages/46/40/a933ac570bf7aad12a298fc53458115cc74053474a72fbb8201d7dc06d3d/python-multipart-0.0.5.tar.gz
Collecting pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2
  Downloading https://files.pythonhosted.org/packages/4c/5f/11db15638a3f5b29c7ae6f24b43c1e7985f09b0fe983621d7ef1ff722020/pydantic-1.10.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.2MB)
Collecting starlette==0.19.1
  Downloading https://files.pythonhosted.org/packages/f1/9d/1fa96008b302dd3e398f89f3fc5afb19fb0b0f341fefa05c65b3a38d64cf/starlette-0.19.1-py3-none-any.whl (63kB)
Collecting h11>=0.8
  Downloading https://files.pythonhosted.org/packages/19/d2/32a15a4955be1b8114a1c570999eefd31279c7f9aa2d2a43d492a79b53c5/h11-0.13.0-py3-none-any.whl (58kB)
Collecting click>=7.0
  Downloading https://files.pythonhosted.org/packages/c2/f1/df59e28c642d583f7dacffb1e0965d0e00b218e0186d7858ac5233dce840/click-8.1.3-py3-none-any.whl (96kB)
Collecting greenlet!=0.4.17; python_version >= "3" and (platform_machine == "aarch64" or (platform_machine == "ppc64le" or (platform_machine == "x86_64" or (platform_machine == "amd64" or (platform_machine == "AMD64" or (platform_machine == "win32" or platform_machine == "WIN32"))))))
  Downloading https://files.pythonhosted.org/packages/2d/7b/a6783972e0d5e3fe94514055a8ea23219ad7a78ec5b0b1675facced24c26/greenlet-1.1.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (154kB)
Collecting Mako
  Downloading https://files.pythonhosted.org/packages/90/12/eb62db8bc346bc41a7ec8fbccd525e91d2747f9acfa6fbfd978948640a85/Mako-1.2.2-py3-none-any.whl (78kB)
Collecting ecdsa!=0.15
  Downloading https://files.pythonhosted.org/packages/09/d4/4f05f5d16a4863b30ba96c23b23e942da8889abfa1cdbabf2a0df12a4532/ecdsa-0.18.0-py2.py3-none-any.whl (142kB)
Collecting rsa
  Downloading https://files.pythonhosted.org/packages/49/97/fa78e3d2f65c02c8e1268b9aba606569fe97f6c8f7c2d74394553347c145/rsa-4.9-py3-none-any.whl
Collecting pyasn1
  Downloading https://files.pythonhosted.org/packages/62/1e/a94a8d635fa3ce4cfc7f506003548d0a2447ae76fd5ca53932970fe3053f/pyasn1-0.4.8-py2.py3-none-any.whl (77kB)
Collecting six>=1.4.0
  Downloading https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl
Collecting typing-extensions>=4.1.0
  Downloading https://files.pythonhosted.org/packages/ed/d6/2afc375a8d55b8be879d6b4986d4f69f01115e795e36827fd3a40166028b/typing_extensions-4.3.0-py3-none-any.whl
Collecting anyio<5,>=3.4.0
  Downloading https://files.pythonhosted.org/packages/c3/22/4cba7e1b4f45ffbefd2ca817a6800ba1c671c26f288d7705f20289872012/anyio-3.6.1-py3-none-any.whl (80kB)
Collecting MarkupSafe>=0.9.2
  Downloading https://files.pythonhosted.org/packages/df/06/c515c5bc43b90462e753bc768e6798193c6520c9c7eb2054c7466779a9db/MarkupSafe-2.1.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Collecting sniffio>=1.1
  Downloading https://files.pythonhosted.org/packages/c3/a0/5dba8ed157b0136607c7f2151db695885606968d1fae123dc3391e0cfdbf/sniffio-1.3.0-py3-none-any.whl
Collecting idna>=2.8
  Downloading https://files.pythonhosted.org/packages/04/a2/d918dcd22354d8958fe113e1a3630137e0fc8b44859ade3063982eacd2a4/idna-3.3-py3-none-any.whl (61kB)
Installing collected packages: typing-extensions, pydantic, sniffio, idna, anyio, starlette, fastapi, h11, click, uvicorn, greenlet, SQLAlchemy, passlib, bcrypt, MarkupSafe, Mako, alembic, six, ecdsa, pyasn1, rsa, python-jose, python-multipart
    Running setup.py install for python-multipart: started
    Running setup.py install for python-multipart: finished with status 'done'
Successfully installed Mako-1.2.2 MarkupSafe-2.1.1 SQLAlchemy-1.4.41 alembic-1.8.1 anyio-3.6.1 bcrypt-4.0.0 click-8.1.3 ecdsa-0.18.0 fastapi-0.82.0 greenlet-1.1.3 h11-0.13.0 idna-3.3 passlib-1.7.4 pyasn1-0.4.8 pydantic-1.10.2 python-jose-3.3.0 python-multipart-0.0.5 rsa-4.9 six-1.16.0 sniffio-1.3.0 starlette-0.19.1 typing-extensions-4.3.0 uvicorn-0.18.3
You should consider upgrading via the 'pip install --upgrade pip' command.

PS C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\fast_api_exp\dcm>