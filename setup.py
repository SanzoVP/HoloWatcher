from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from version.py
about = {}
with open(os.path.join("vtuber_tracker", "version.py"), encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="vtuber-tracker",
    version=about["__version__"],
    author="Your Name",
    author_email="your.email@example.com",
    description="Track and get notifications when your favorite VTubers go live",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vtuber-tracker",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/vtuber-tracker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "vtuber_tracker": ["data/*.json", "*.example"],
    },
    python_requires=">=3.6",
    install_requires=[
        "google-auth-oauthlib>=0.4.1",
        "google-api-python-client>=2.0.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "vtuber-tracker=vtuber_tracker.main:main",
        ],
    },
)