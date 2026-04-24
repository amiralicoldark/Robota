from setuptools import setup, find_packages

setup(
    name="robota",
    version="1.0",
    description="کتابخانه ساده پایتون برای ساخت ربات روبیکا",
    author="ARSAPY",
    author_email="your@email.com",
    url="https://github.com/amiralicoldark/Robota",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
