from setuptools import setup, find_packages

setup(
    name="coherence-spacetime-lattice",
    version="0.1.0",
    packages=find_packages(include=["*", "src.*"]),
    package_dir={"": "."},
    description="Experimental κ–τ–Σ coherence field and spacetime lattice models.",
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
