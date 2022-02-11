from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nlp",
    version="0.1",
    description="nlp server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Viv",
    author_email="ymviv@qq.com",
    packages=find_packages(".", exclude=("tests",)),
    python_requires=">=3.7",
    install_requires=[
        "grpcio==1.27.2",
        "jieba==0.42.1",
        "protobuf==3.15.0",
        "sentry-sdk==0.14.2",
    ]
)
