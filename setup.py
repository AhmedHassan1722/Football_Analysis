from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="football-analysis",
    version="1.0.0",
    author="Ahmed Hassan",
    author_email="your.email@example.com",
    description="AI-powered football analysis system with player tracking, speed, and distance analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AhmedHassan1722/Football_Analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "football-analysis=main:main",
        ],
    },
    include_package_data=True,
    keywords="football soccer analysis tracking yolo computer-vision sports-analytics",
    project_urls={
        "Bug Reports": "https://github.com/AhmedHassan1722/Football_Analysis/issues",
        "Source": "https://github.com/AhmedHassan1722/Football_Analysis",
    },
)
