from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="robota",
    version="1.0.0",
    author="AmirAli Momeni",
    author_email="amir.darkli80@gmail.com",
    description="Official Rubika Bot API library - Full featured, easy to use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amiralicoldark/Robota",
    project_urls={
        "Documentation": "https://amiralicoldark.github.io/Robota",
        "Source": "https://github.com/amiralicoldark/Robota",
        "Tracker": "https://github.com/amiralicoldark/Robota/issues",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    keywords="rubika, bot, api, telegram-like, rubika-bot, robota",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)
