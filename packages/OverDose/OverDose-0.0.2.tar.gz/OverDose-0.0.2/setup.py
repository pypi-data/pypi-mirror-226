import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OverDose",
    version="0.0.2",
    author="Izuru Inose",
    author_email="i.inose0304@gmail.com",
    description="Overdose of drugs in the US",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i-inose/OverDose",
    project_urls={
        "Bug Tracker":
            "https://github.com/i-inose/OverDose",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['OverDose'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'OverDose = OverDose:main'
        ]
    },
)
