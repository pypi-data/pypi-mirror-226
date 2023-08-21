import asyncio
import unittest
from unittest.mock import MagicMock, patch
from app.unittest_exp.asyncio_mock_await_func import start_worker


class TestStartWorker(unittest.IsolatedAsyncioTestCase):
    @patch("app.unittest_exp.asyncio_mock_await_func.execute_task1")
    async def test_start_worker(self, async_execute_task1_mock):
        # Mock the async execute_task1 function
        async def mock_execute_task1(data):
            await asyncio.sleep(0)  # Simulate immediate completion
            return len(data)

        # Replace the original async_data_processing with the mock version
        async_execute_task1_mock.return_value = MagicMock(wraps=mock_execute_task1)
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