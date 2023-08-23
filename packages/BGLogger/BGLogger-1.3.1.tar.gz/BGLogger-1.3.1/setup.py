from setuptools import setup
from io import open
from BGLogger.BGLogger import Log

setup(
    name="BGLogger",
    version=str(Log.__version__),
    description="BGLogger is a simple module for logging in Python",
    long_description="BGLogger is a simple module for logging in Python. If you wanna see full documentation you can just visit our GitHub repository. Just call print(Log.__github__) to do this",
    author="BelGray",
    author_email="belg186@yandex.ru",
    url=str(Log.__github__),
    download_url=str(Log.__github__+f"/archive/v{Log.__version__}.zip"),
    license="GNU General Public License v3.0, see LICENSE file",
    packages=['BGLogger'],
    
)
