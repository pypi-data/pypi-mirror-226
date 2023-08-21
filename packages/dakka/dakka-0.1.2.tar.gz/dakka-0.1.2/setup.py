from setuptools import setup, find_packages

setup(
    name="dakka",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "openapi_spec_validator",
        "openapi_spec_pydantic",
        "openai",
        "termcolor"
    ],
    entry_points={
        "console_scripts": [
            "dakka=dakka.cli:main"
        ]
    },
    description="Do more of what works."
)