from setuptools import find_packages, setup

setup(
    name="custom-antidetect-browser",
    version="0.1.0",
    description="Professional antidetect browser with C++-level fingerprint spoofing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Custom Browser Team",
    author_email="dev@example.com",
    url="https://github.com/yourusername/custom-antidetect",
    package_dir={"": "pythonlib"},
    packages=find_packages(where="pythonlib"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "playwright>=1.40.0",
        "browserforge>=0.2.0",
        "orjson>=3.9.0",
        "cryptography>=41.0.0",
        "click>=8.1.0",
        "flet>=0.19.0",
        "pydantic>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "custom-browser=custom_browser.cli:main",
        ],
    },
)
