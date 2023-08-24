from setuptools import setup

setup(
    name="axgb-online",
    packages=[
        "adaxgboost",
    ],
    version="0.1.11",
    description="ada-xgboost package",
    install_requires=[
        "numpy==1.23.4",
        "pandas==1.4.0",
        "scikit-learn>=1.0.2",
        "tqdm==4.61.0",
        "river==0.14.0",
        "xgboost==1.6.2"
    ]
)