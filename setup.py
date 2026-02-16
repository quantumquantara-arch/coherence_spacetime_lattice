from setuptools import setup, find_packages

setup(
    name="coherence-spacetime-lattice",
    version="0.2.0",
    packages=find_packages(include=["*", "src.*"]),
    package_dir={"": "."},
    description="κ–τ–Σ coherence field, temporal channels, and emergent-geometry proxies on a lattice.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Quantara Research",
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26.0",
        "matplotlib>=3.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
