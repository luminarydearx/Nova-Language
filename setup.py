from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nova-language",
    version="2.0.0",
    author="Dearly Febriano Irwansyah",
    author_email="dearlyfebrianoi@gmail.com",
    description="Nova Language - A custom programming language with Python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luminarydearx/Nova-Language",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "nova=nova.cli.nova_console:main",
        ],
    },
    include_package_data=True,
)
