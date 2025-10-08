#!/usr/bin/env python3
"""
Setup script for CrewAI Accelerate.

This is a fallback setup script for pip-based installation.
The primary build system is Maturin via pyproject.toml.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crewai-accelerate",
    version="0.1.0",
    author="CrewAI",
    author_email="info@crewai.com",
    description="High-performance acceleration for CrewAI - 2-5x faster memory, tools, and task execution with zero code changes",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/crewAI/crewai",
    project_urls={
        "Homepage": "https://github.com/crewAI/crewai",
        "Documentation": "https://github.com/crewAI/crewai/blob/main/docs/crewai-accelerate/README.md",
        "Repository": "https://github.com/crewAI/crewai",
        "Bug Tracker": "https://github.com/crewAI/crewai/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-timeout>=2.1.0",
            "pytest-benchmark>=4.0.0",
            "pytest-xdist>=3.0.0",
            "pytest-html>=3.1.0",
            "coverage>=7.0.0",
            "mock>=4.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "crewai-accelerate=crewai_accelerate.__main__:main",
            "crewai-accelerate-bootstrap=crewai_accelerate.bootstrap:main",
        ],
    },
    keywords=["crewai", "acceleration", "performance", "ai", "agents", "optimization"],
    include_package_data=True,
    zip_safe=False,
)
