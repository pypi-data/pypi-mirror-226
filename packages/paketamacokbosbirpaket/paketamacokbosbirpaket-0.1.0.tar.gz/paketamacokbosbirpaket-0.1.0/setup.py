from setuptools import setup, find_packages

setup(
    name="paketamacokbosbirpaket",
    version="0.1.0",
    packages=find_packages(),
    description="This is a test package.",
    long_description="Bu bir test paketidir.",
    long_description_content_type = "text/markdown",
    license="MIT",
    author="Bard",
    upload_requires = ["pypi-token==3.0.0"],
    author_email="bard@example.com",
    url="https://github.com/bard/my_package",
    keywords="python test",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
