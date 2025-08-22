import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "1.0.0"

REPO_NAME = "diamond-price-predictor"
AUTHOR_USER_NAME = "Diamond Price Predictor Team"
SRC_REPO = "gemstack_mlops"  # Keep package name for compatibility
AUTHOR_EMAIL = ""


setuptools.setup(
    name="diamond-price-predictor",
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Diamond Price Prediction MLOps - Production-ready ML pipeline for predicting diamond prices",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/yourusername/diamond-price-predictor",
    project_urls={
        "Homepage": "https://github.com/yourusername/diamond-price-predictor",
        "Documentation": "https://diamond-price-predictor.readthedocs.io/",
        "Repository": "https://github.com/yourusername/diamond-price-predictor",
        "Issues": "https://github.com/yourusername/diamond-price-predictor/issues",
    },
    package_dir={"": "."},
    packages=["gemstack_mlops"],  # Keep internal package name
    keywords=["diamond", "price-prediction", "machine-learning", "MLOps", "MLflow"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)