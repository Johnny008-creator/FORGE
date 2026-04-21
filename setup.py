from setuptools import setup, find_packages

setup(
    name="forge-agent",
    version="0.7.0",

    author="Johnny008-creator",
    description="Local AI coding agent powered by Ollama",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Johnny008-creator/FORGE",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
    ],
    py_modules=["forge"],
    entry_points={
        "console_scripts": [
            "forge=forge:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
