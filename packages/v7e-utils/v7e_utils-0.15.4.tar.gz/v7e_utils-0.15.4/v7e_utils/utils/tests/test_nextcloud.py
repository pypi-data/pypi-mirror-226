from v7e_utils.utils.nextclould import Nextcloud
from v7e_utils.utils.config import NextCloudItem
from django.test import TestCase


class UtilsNextcloudTestCase(TestCase):
    def test_mkdir(self):
        parameters = NextCloudItem()
        print(parameters)
        next = Nextcloud(
            config_parameters=parameters
        )
        result = next.mkdir(path="Reports/PDFs/expedientes/88888888")

        self.assertTrue(result)
