from setuptools import setup, find_packages

setup(
    name="ocean-spark-connect",
    version="0.1.0",
    description="Use Spark Connect with Ocean Spark Applications",
    author="Sigmar Stefansson",
    author_email="sigmar@netapp.com",
    url="https://github.com/sigmarkarl/ocean-spark-connect",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "pyarrow",
        "requests",
        "websockets",
        "grpcio",
        "grpcio-status",
        "googleapis-common-protos",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)