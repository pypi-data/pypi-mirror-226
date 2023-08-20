import os

from setuptools import find_packages, setup

from fugue_ml_version import __version__

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()


def get_version() -> str:
    tag = os.environ.get("RELEASE_TAG", "")
    if "dev" in tag.split(".")[-1]:
        return tag
    if tag != "":
        assert tag == __version__, "release tag and version mismatch"
    return __version__


setup(
    name="fugue-ml",
    version=get_version(),
    packages=find_packages(exclude=["tests"]),
    description="Fugue ML",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    author="The Fugue Development Team",
    author_email="hello@fugue.ai",
    keywords="fugue machine learning ai",
    url="http://github.com/fugue-project/fugue-ml",
    package_data={"fugue_ml": ["py.typed"]},
    install_requires=["fugue[sql]>=0.8.6", "fsspec>=2023.1.0", "threadpoolctl"],
    extras_require={
        "openai": ["openai", "tiktoken"],
        "huggingface": ["transformers", "sentence-transformers"],
        "hnswlib": ["hnswlib"],
        "spark": ["fugue[spark]"],
        "dask": ["fugue[dask]", "dask-sql"],
        "ray": ["fugue[ray]"],
    },
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
    entry_points={
        "fugue_ml.plugins": [
            "openai = fugue_ml.integrations.openai.registry[openai]",
            "huggingface = fugue_ml.integrations.huggingface.registry[huggingface]",
            "hnswlib = fugue_ml.integrations.hnswlib.registry[hnswlib]",
        ],
    },
)
