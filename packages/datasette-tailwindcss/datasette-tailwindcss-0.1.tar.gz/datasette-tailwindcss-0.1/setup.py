from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-tailwindcss",
    description="Replace default template with tailwindcss",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="matt jensen",
    url="https://github.com/publicmatt/datasette-tailwindcss",
    project_urls={
        "Issues": "https://github.com/publicmatt/datasette-tailwindcss/issues",
        "CI": "https://github.com/publicmatt/datasette-tailwindcss/actions",
        "Changelog": "https://github.com/publicmatt/datasette-tailwindcss/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License"
    ],
    version=VERSION,
    packages=["datasette_tailwindcss"],
    entry_points={"datasette": ["tailwindcss = datasette_tailwindcss"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    package_data={
        "datasette_tailwindcss": ["static/*", "templates/*"]
    },
    python_requires=">=3.7",
)
