from setuptools import setup, find_packages

setup(
    name="upyuns3client",
    version="0.1.2",
    url="https://github.com/evansuner/upyuns3client",
    author="Evan",
    author_email="zhidong.s@outlook.com",
    description="UpYun Storage SDK for Python S3 Support",
    long_description=open("README.md", mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(),
    keywords=["upyun", "python", "sdk", "s3"],
    install_requires=[
        "boto3==1.28.30",
        "python-dotenv==1.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
