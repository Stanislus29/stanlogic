from pathlib import Path
from setuptools import setup, find_packages

# Locate requirements.txt relative to setup.py's location
here = Path(__file__).parent.resolve()
req_file = here / "requirements.txt"

if req_file.exists():
    requirements = [
        line.strip()
        for line in req_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
else:
    requirements = []

setup(
    name="StanLogic",
    version="2.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Somtochukwu Stanislus Emeka-Onwuneme",
    description="An advanced KMap solver and logic simplification engine",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "web": ["Flask>=2.0", "Flask-Cors>=3.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=3.0.0"],
    },
)