from setuptools import setup

setup(
    name="trendup-python-lib",
    version="0.0.1",

    author="JerryLin",
    author_email="jerry.lin@keeptossinglab.com",
    packages=["trendup_storage", "trendup_config"],
    include_package_data=True,
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    description="Useful towel-related stuff.",
    install_requires=[
        "attrs",
        "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
