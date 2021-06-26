import re

import setuptools

with open("pyUltroid/version.py", "rt", encoding="utf8") as x:
    version = re.search(r'__version__ = "(.*?)"', x.read()).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = (fr.read()).split("\n")

name = "py-Ultroid"
author = "TeamUltroid"
author_email = "teamultroid@protonmail.ch"
description = "A Secure and Powerful Python-Telethon Based Library For Ultroid Userbot."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/TeamUltroid/Ultroid"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)