# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2023/07/21 10:03:53
@Author  :   Evan
@Version :   1.0
@Desc    :   None
"""


import random
from pathlib import Path

import boto3
from botocore.client import Config


class UpYunS3Client:
    def __init__(self, access_key: str, secret_key: str) -> None:
        self.ak = access_key
        self.sk = secret_key
        self.endpoint = "https://s3.api.upyun.com"
        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.ak,
            aws_secret_access_key=self.sk,
            config=Config(signature_version="s3v4"),
        )

    def list_buckets(self) -> list:
        # 列出所有的bucket：
        buckets = []
        response = self.s3.list_buckets()
        for bucket in response["Buckets"]:
            buckets.append(bucket["Name"])
        return buckets

    def list_folders(self, bucket: str) -> list:
        # 列出指定bucket下的所有文件夹：
        folders = []
        response = self.s3.list_objects_v2(Bucket=bucket, Delimiter="/")
        for prefix in response.get("CommonPrefixes", []):
            folders.append(prefix.get("Prefix"))

        return folders

    def list_files(self, bucket: str, folder: str) -> list:
        # 列出指定bucket下的指定文件夹下的所有文件：
        files = []
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=folder)
        for obj in response.get("Contents", []):
            files.append(obj.get("Key"))
        return files[1:]

    def delete_file(self, bucket: str, file: str) -> dict:
        # 删除指定bucket下的指定文件：
        response = self.s3.delete_object(Bucket=bucket, Key=file)
        return response

    def delete_folder(self, bucket: str, folder: str) -> None:
        # 删除指定bucket下的指定文件夹以及其下文件
        objects_to_delete = []
        if folder[-1] == "/":
            folder = folder[:-1]
        if folder[0] == "/":
            folder = folder[1:]
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=folder)

        for obj in response.get("Contents", []):
            objects_to_delete.append({"Key": obj["Key"]})

        if objects_to_delete:
            self.s3.delete_objects(Bucket=bucket, Delete={"Objects": objects_to_delete})

    def create_folder(self, bucket: str, folder_name: str) -> None:
        # 创建文件夹
        try:
            if folder_name[-1] != "/":
                folder_name += "/"

            self.s3.upload_file("./test.png", bucket, f"{folder_name}test.png")
            self.s3.delete_object(Bucket=bucket, Key=f"{folder_name}test.png")
        except Exception as e:
            raise e

    def upload_file(self, bucket: str, file_path: str, object_name: str = None) -> None:
        # 上传文件, 如果object_name为None，则默认使用file_path的文件名 并且上传到根目录
        if object_name is None:
            filename = Path(file_path).name
            object_name = filename
        try:
            self.s3.upload_file(file_path, bucket, object_name)
        except Exception as e:
            raise e

    def get_file_info(self, bucket: str, object_name: str) -> dict:
        # 获取文件信息
        try:
            response = self.s3.head_object(Bucket=bucket, Key=object_name)
            return response
        except Exception as e:
            raise e

    def get_random_file(self, bucket: str, folder: str) -> str:
        # 获取随机文件
        files = self.list_files(bucket, folder)
        file = random.choice(files)
        return file

    def download_file(self, bucket: str, object_name: str, file_path: str = None):
        # 下载文件
        if file_path is None:
            file_path = Path(object_name).name
        try:
            self.s3.download_file(bucket, object_name, file_path)
        except Exception as e:
            raise e

    def generate_presigned_url(
        self, bucket: str, object_name: str, expiration: int = 3600
    ) -> str:
        """生成具有时效性的签名url 这个URL的有效期是有限的，最长可以设置为7天（604800秒）"""

        # 生成预签名URL
        try:
            response = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": object_name},
                ExpiresIn=expiration,
                HttpMethod="GET",
            )
            return response
        except Exception as e:
            raise e


if __name__ == "__main__":
    ak = "xxxxx"
    sk = "xxxxx"
    client = UpYunS3Client(ak, sk)
    client.generate_presigned_url(
        bucket="test-bucket", object_name="test.png", expiration=3600
    )
