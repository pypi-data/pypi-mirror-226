# Python Library Packaging and Distribution Project

This is a sample project that demonstrates how to create a Python library and publish it to the Python Package Index (PyPI). The project is designed to provide a clear example of the steps involved in packaging and distributing a Python library.

## Reference Documentation

For detailed information on packaging and distributing Python projects, you can refer to the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) tutorial on the official Python packaging website.

## Project Structure

Make sure your project follows this structure:

```
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── example_package_YOUR_USERNAME_HERE/
│       ├── __init__.py
│       └── example.py
└── tests/
```

1. The `src` directory contains your project's source code, and you should have an `__init__.py` file inside the `project_name` folder to mark it as a Python package.
2. Include a `LICENSE` file to specify the licensing terms of your project.
3. Write your project's README in Markdown format in the `README.md` file.
4. Place your project's tests in the `tests` directory.
5. The `pyproject.toml` file contains the project metadata and configuration.

## Pyproject.toml Configuration

Here is an example of a `pyproject.toml` configuration for your project:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example_package_zhaohany"
version = "0.0.1"
authors = [
  { name = "Zhaohan Yan", email = "zhaohany@outlook.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
homepage = "https://github.com/zhaohany/example_package_zhaohany"
bug-tracker = "https://github.com/zhaohany/example_package_zhaohany"
```

## Building and Distributing

To build and distribute your package, follow these steps:

1. Install required tools:

```bash
sudo apt install python3-pip
pip3 install build
sudo apt install python3.10-venv
```

2. Build source distribution (sdist) and/or build distribution (wheel):

```bash
python3 -m build --sdist /path/to/your/project
python3 -m build --wheel /path/to/your/project
```

3. Install Twine for uploading:

```bash
sudo apt install twine
```

4. Upload your distribution files to PyPI:

```bash
twine upload dist/example_package_zhaohany-0.0.1.tar.gz dist/example_package_zhaohany-0.0.1-py3-none-any.whl
```

## API Token for PyPI Upload

If you encounter an API token issue during upload, create an API token on PyPI:

1. Username: `__token__`
2. Password: Your generated token

This is a basic outline of the steps required to create, package, and distribute a Python library to PyPI. For more details and troubleshooting, refer to the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) tutorial on the official Python packaging website.