import os
from unittest import TestCase
from unittest.mock import patch
import logging

from .blog_backup import main

@patch.dict(
    os.environ,
    {
        "BACKUP_S3_ENDPOINT": "",
        "BACKUP_S3_KEY_ID": "",
        "BACKUP_S3_ACCESS_KEY": "",
        "BACKUP_BUCKET_NAME": "",
        "BACKUP_KEY_PREFIX": "",
    },
    clear=True)
class TestBlogBackup(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
    
    def test_main(self):
        main()