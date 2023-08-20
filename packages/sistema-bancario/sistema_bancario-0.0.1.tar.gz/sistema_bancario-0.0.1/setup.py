from setuptools import (setup,
                        find_packages)

with open("Apresentação.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sistema_bancario",
    version="0.0.1",
    author="Marcus Vinicius Barcelos",
    author_email="marcusbarcelos2001@gmail.com",
    description="Meu sistema Bancario",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcusViniciusBarcelos/sistema_bancario",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)
