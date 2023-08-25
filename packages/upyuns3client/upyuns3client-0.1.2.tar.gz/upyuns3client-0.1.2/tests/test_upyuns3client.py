import os
import unittest
import uuid

from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from upyuns3client.upyuns3client import UpYunS3Client

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")
BUCKET = os.getenv("BUCKET")


def root_path():
    return "/py_sdk-%s/" % uuid.uuid4().hex


class TestUpYun(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = UpYunS3Client(ACCESS_KEY, SECRET_KEY)
        cls.root = root_path()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.delete_folder(BUCKET, cls.root)
        print("test completed")
        print("=====================================")

    def test_create_folder(self):
        try:
            self.client.create_folder(BUCKET, self.root)
            print("test_create_folder: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_list_buckets(self):
        try:
            res = self.client.list_buckets()
            print(res)
            print("test_list_buckets: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_list_folders(self):
        try:
            res = self.client.list_folders(BUCKET)
            print(res)
            print("test_list_folders: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_list_files(self):
        try:
            res = self.client.list_files(BUCKET, self.root)
            print(res)
            print("test_list_files: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_upload_file(self):
        try:
            self.client.upload_file(BUCKET, "./test.png", self.root + "test.png")
            self.client.upload_file(
                BUCKET, "./requirements.txt", self.root + "requirements.txt"
            )
            print("test_upload_file: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    # def test_delete_file(self):
    #     try:
    #         res = self.client.delete_file(BUCKET, self.root + "test.png")
    #         print(res)
    #         print("test_delete_file: OK")
    #     except Exception as e:
    #         raise
    #     finally:
    #         print("=====================================")

    # def test_get_file_info(self):
    #     try:
    #         res = self.client.get_file_info(BUCKET, self.root + "requirements.txt")
    #         print(res)
    #         print("test_get_file_info: OK")
    #     except Exception as e:
    #         raise
    #     finally:
    #         print("=====================================")

    # def test_get_random_file(self):
    #     try:
    #         res = self.client.get_random_file(BUCKET, self.root)
    #         print(res)
    #         print("test_get_random_file: OK")
    #     except Exception as e:
    #         raise
    #     finally:
    #         print("=====================================")

    def download_file(self):
        try:
            self.client.download_file(BUCKET, self.root, "./requirements1.txt")
            print("test_download_file: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_generate_presigned_url(self):
        try:
            res = self.client.generate_presigned_url(
                BUCKET, self.root + "requirements.txt", expiration=60
            )
            print(res)
            print("test_generate_presigned_url: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")

    def test_delete_folder(self):
        try:
            self.client.delete_folder(BUCKET, self.root)
            print("test_delete_folder: OK")
        except Exception as e:
            raise
        finally:
            print("=====================================")


if __name__ == "__main__":
    unittest.main()
