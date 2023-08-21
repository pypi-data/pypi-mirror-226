import asyncio
import unittest
from unittest.mock import MagicMock, patch
from app.unittest_exp.asyncio_mock_await_func2 import start_worker

class ActivityStubMock:
    async def pre(self):
        print("Executing pre.mock..")
        await asyncio.sleep(1)

    async def post(self):
        print("Executing post mock...")
        await asyncio.sleep(1)


class TestStartWorker(unittest.IsolatedAsyncioTestCase):
    @patch("app.unittest_exp.asyncio_mock_await_func2.create_activity_stub")
    async def test_start_worker(self, mock_create_activity_stub):
        # Mock the async execute_task1 function

        # Replace the original async_data_processing with the mock version
        mock_create_activity_stub.return_value = MagicMock(wraps=ActivityStubMock())
        data = {"a": 1}
        await start_worker(data)
        print("executed")


if __name__ == '__main__':

    unittest.main()


"""

aafak@aafak-virtual-machine:~/mypy$ export PYTHONPATH=$PYTHONPATH:/home/aafak/mypy/
aafak@aafak-virtual-machine:~/mypy$ cd app/unittest_exp/
aafak@aafak-virtual-machine:~/mypy/app/unittest_exp$ python3 test_asyncio_mock_await_func.py
starting worker....
executed
.
----------------------------------------------------------------------
Ran 1 test in 0.095s

OK
aafak@aafak-virtual-machine:~/mypy/app/unittest_exp$

"""