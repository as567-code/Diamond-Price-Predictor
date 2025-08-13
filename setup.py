import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.1.0"

REPO_NAME = "gemstack-mlops"
AUTHOR_USER_NAME = "Aditya Swaroop"
SRC_REPO = "gemstack_mlops"
AUTHOR_EMAIL = ""


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Gemstack: opinionated MLOps template with MLflow, DVC, Airflow, and Flask",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/adityaswaroop/gemstack-mlops",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)