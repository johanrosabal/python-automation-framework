import pytest

from applications.web.demo.config.decorators import demo
from core.config.logger_config import setup_logger
from applications.web.demo.pages.DownloadsPage import DownloadsPage
from core.ui.common.BaseTest import BaseTest, downloads
from core.utils import helpers
from core.utils.decorator import test

logger = setup_logger('TestDownloads')


@pytest.mark.web
@demo
class TestDownloads(BaseTest):
    download = DownloadsPage.get_instance()

    @test(test_case_id="HRM-0001", test_description="Verify Download File")
    def test_downloads(self):
        filename = "samplefile.pdf"

        # Load Page
        self.download.go_to("https://demo.automationtesting.in/FileDownload.html")
        # Get File Location
        self.download.click_download()
        # Validate File Exist on Download Folder
        assert helpers.wait_for_file_to_download(filename, timeout=10, interval=1), "File Not on Download Folder"
