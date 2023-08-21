from app.unittest_exp.src import backups
import unittest
from unittest.mock import patch
from app.unittest_exp.src.publisher import KafkaPublisher


class TestBackups(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch.object(KafkaPublisher, 'publish_events', return_value="SUCCESS_MOCKED")
    def test_create_backup(self, mock_publisher):
        backups.create_backup({"name": "bkp1"})

    # def test_create_backup2(self):
    #     backups.create_backup({"name": "bkp1"})


if __name__== '__main__':
    unittest.main()
