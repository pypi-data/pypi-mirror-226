from setuptools import find_packages, setup
from djangochannelsrestframework import __version__

setup(
    name="djangochannelsrestframework",
    version=__version__,
    url="https://github.com/NilCoalescing/djangochannelsrestframework",
    author="LostMoa Limited",
    author_email="info@nilcoalescing.com",
    description="RESTful API for WebSockets using django channels.",
    long_description=open("README.rst").read(),
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["Django>=3.2", "channels>=4.0.0", "djangorestframework>=3.14.0"],
    extras_require={
        "tests": [
            "channels[daphne]>=4.0.0",
            "pytest>=7.0.1",
            "pytest-django>=4.5.2",
            "pytest-asyncio>=0.18.1",
            "coverage>=6.3.1",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
