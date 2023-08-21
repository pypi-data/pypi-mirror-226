Python Poetry is a dependency management and packaging tool that aims to simplify the process
of managing dependencies and packaging Python projects. It offers several advantages
over traditional tools like pip and virtualenv. Here are some key advantages of Python Poetry:

pyproject.toml:
Poetry provides a centralized way to manage project dependencies. It creates a pyproject.toml
file where you can list all your project's dependencies, including direct and transitive dependencies.
Poetry also resolves and locks dependency versions, ensuring consistency across environments.

Lock File: Poetry generates a poetry.lock file that locks the exact versions of all dependencies
used in your project. This ensures that everyone working on the project is using the
same versions of dependencies.

Packaging and Publishing: Poetry simplifies the process of packaging your Python project 
into a distributable format, such as a Wheel or a source distribution (sdist). It also provides
commands to publish packages to the Python Package Index (PyPI) or other repositories.

Faster Installations: Since the lock file specifies the exact versions of dependencies,
installing them becomes faster because the resolver doesn't need to calculate and select
versions each time. It simply refers to the lock file for the exact versions to install.
Tools like pip dynamically resolve dependencies each time you run pip install -r requirements.txt.
This can lead to different versions being installed in different environments, especially
if new versions have been released since you first created the file.

Virtual Environments: Poetry automatically creates and manages virtual environments for your projects.
This isolates project dependencies from the system Python environment, minimizing conflicts
and ensuring a consistent environment for your project.

Installation: Install Poetry using pip: pip install poetry

Creating a New Project: Navigate to the directory where you want to create your project and run:

aafak@aafak-virtual-machine:~$ poetry new poetry_exp
Created package poetry_exp in poetry_exp
aafak@aafak-virtual-machine:~$ ls
addons            atlas_repos     cd_cluster_installation  Downloads         ls      Pictures    Templates
admin.conf        bring_postgres  curl                     env_vars          member  poetry_exp  Videos
alert_rec.py      cadence         Desktop                  index.html        Music   Public
atlas-dev-images  cadence_exp     Documents                kube-flannel.yml  mypy    python311

aafak@aafak-virtual-machine:~$ cd poetry_exp/
aafak@aafak-virtual-machine:~/poetry_exp$ ls
poetry_exp  pyproject.toml  README.md  tests

aafak@aafak-virtual-machine:~/poetry_exp$ cat pyproject.toml
[tool.poetry]
name = "poetry-exp"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "poetry_exp"}]

[tool.poetry.dependencies]
python = "^3.11"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

aafak@aafak-virtual-machine:~/poetry_exp$ cd tests/
aafak@aafak-virtual-machine:~/poetry_exp/tests$ ls
__init__.py
aafak@aafak-virtual-machine:~/poetry_exp/tests$ cd ../poetry_exp/
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ ls
__init__.py
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$

Adding Dependencies: Add flask as a depedency
   Edit the pyproject.toml file to add your project dependencies under the [tool.poetry.dependencies] section.


aafak@aafak-virtual-machine:~/poetry_exp$ cat pyproject.toml
[tool.poetry]
name = "poetry-exp"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "poetry_exp"}]

[tool.poetry.dependencies]
python = "^3.11"
flask = "2.3.2"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Installing Dependencies: Run:, will create the poetry.lock file

aafak@aafak-virtual-machine:~/poetry_exp$ poetry install
Creating virtualenv poetry-exp-15UI45M7-py3.11 in /home/aafak/.cache/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (0.7s)

Failed to unlock the collection!
aafak@aafak-virtual-machine:~/poetry_exp$ export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
aafak@aafak-virtual-machine:~/poetry_exp$ poetry install
Updating dependencies
Resolving dependencies... Downloading https://files.pythonhosted.org/packages/0d/f1/5f39e771cd730d347539bb74c6d496737b9d5f0aResolving dependencies... Downloading https://files.pythonhosted.org/packages/68/5f/447e04e828f47465eeab35b5d408b7ebaaaee207Resolving dependencies... (3.1s)

Package operations: 7 installs, 0 updates, 0 removals

  • Installing markupsafe (2.1.3)
  • Installing blinker (1.6.2)
  • Installing click (8.1.7)
  • Installing itsdangerous (2.1.2)
  • Installing jinja2 (3.1.2)
  • Installing werkzeug (2.3.7)
  • Installing flask (2.3.2)

Writing lock file

Installing the current project: poetry-exp (0.1.0)
aafak@aafak-virtual-machine:~/poetry_exp$ ls
poetry_exp  poetry.lock  pyproject.toml  README.md  tests
aafak@aafak-virtual-machine:~/poetry_exp$

Now create your app:

aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ cat flask_app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def handle_alert():
    print("Handling alert....")
    return "Ok"

if __name__ == '__main__':
    server = app.run('172.17.29.165', 5001)
    print('Starting the server')
    server.serve_forever()
	
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$

Using Poetry:

Poetry automatically manages virtual environments for your projects. To activate the virtual environment and run your application, 
follow these steps:
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ poetry shell
Spawning shell within /home/aafak/.cache/pypoetry/virtualenvs/poetry-exp-15UI45M7-py3.11
. /home/aafak/.cache/pypoetry/virtualenvs/poetry-exp-15UI45M7-py3.11/bin/activate
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ . /home/aafak/.cache/pypoetry/virtualenvs/poetry-exp-15UI45M7-py3.11/bin/activate
(poetry-exp-py3.11) aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ python flask_app.py
 * Serving Flask app 'flask_app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://172.17.29.165:5001
Press CTRL+C to quit


Add more dependencies and the run poetry update

(poetry-exp-py3.11) aafak@aafak-virtual-machine:~/poetry_exp$ exit
exit
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ ls
flask_app.py  __init__.py
aafak@aafak-virtual-machine:~/poetry_exp/poetry_exp$ cd ..
aafak@aafak-virtual-machine:~/poetry_exp$ ls
poetry_exp  poetry.lock  pyproject.toml  README.md  tests
aafak@aafak-virtual-machine:~/poetry_exp$ cat pyproject.toml
[tool.poetry]
name = "poetry-exp"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "poetry_exp"}]

[tool.poetry.dependencies]
python = "^3.11"
flask = "2.3.2"
pyvmomi = "8.0.1.0.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
aafak@aafak-virtual-machine:~/poetry_exp$ poetry update
Updating dependencies
Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... Downloading https://files.pythonhosted.org/packages/33/36/dcdbaae24b7ccd2685bb5d975553235269edd249Resolving dependencies... (4.2s)

Package operations: 2 installs, 0 updates, 0 removals

  • Installing six (1.16.0)
  • Installing pyvmomi (8.0.1.0.2)

Writing lock file
aafak@aafak-virtual-machine:~/poetry_exp$




aafak@aafak-virtual-machine:~/poetry_exp$ poetry build
Building poetry-exp (0.1.0)
  - Building sdist
  - Built poetry_exp-0.1.0.tar.gz
  - Building wheel
  - Built poetry_exp-0.1.0-py3-none-any.whl
aafak@aafak-virtual-machine:~/poetry_exp$

aafak@aafak-virtual-machine:~/poetry_exp$ ls
dist  poetry_exp  poetry.lock  pyproject.toml  README.md  tests
aafak@aafak-virtual-machine:~/poetry_exp$ poetry publish

Publishing poetry-exp (0.1.0) to PyPI
 - Uploading poetry_exp-0.1.0-py3-none-any.whl FAILED

HTTP Error 403: Invalid or non-existent authentication information. See https://pypi.org/help/#invalid-auth for more information. | b'<html>\n <head>\n  <title>403 Invalid or non-existent authentication information. See https://pypi.org/help/#invalid-auth for more information.\n \n <body>\n  <h1>403 Invalid or non-existent authentication information. See https://pypi.org/help/#invalid-auth for more information.\n  Access was denied to this resource.<br/><br/>\nInvalid or non-existent authentication information. See https://pypi.org/help/#invalid-auth for more information.\n\n\n \n'
aafak@aafak-virtual-machine:~/poetry_exp$

aafak@aafak-virtual-machine:~/poetry_exp$ poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcCJDQzMDBiZTEyLTExNDAtNGYwMi05Njg4LTIxNTk3ZDQ2Y2M3MwACKlszLCIwZDQwMDFiMC1hY2VlLTRiMzYtYjBhZi0wMzY2MzUyZjVlMTIiXQAABiBRA019QfEkkLV3r6PORYXGcuHF5SoOUn4ZHY38zx7_Dw
Usin

aafak@aafak-virtual-machine:~/poetry_exp$ poetry publish

Publishing poetry-exp (0.1.0) to PyPI
 - Uploading poetry_exp-0.1.0-py3-none-any.whl 100%
 - Uploading poetry_exp-0.1.0.tar.gz 100%
aafak@aafak-virtual-machine:~/poetry_exp$


aafak@aafak-virtual-machine:~/peotry_demo/mypy$ poetry build
Building mypy (0.1.0)
  - Building sdist
  - Built mypy-0.1.0.tar.gz
  - Building wheel
  - Built mypy-0.1.0-py3-none-any.whl
aafak@aafak-virtual-machine:~/peotry_demo/mypy$ poetry publish



aafak@aafak-virtual-machine:~/peotry_demo/mypy$ poetry build
Building mypy (0.1.0)
  - Building sdist
  - Built mypy-0.1.0.tar.gz
  - Building wheel
  - Built mypy-0.1.0-py3-none-any.whl
aafak@aafak-virtual-machine:~/peotry_demo/mypy$ poetry publish