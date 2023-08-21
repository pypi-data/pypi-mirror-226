import setuptools

setuptools.setup(
    name="example_package_ohnas",
    version="0.0.1",
    author="ohnas",
    author_email="ohnas12@gmail.com",
    description="A small example package",
    long_description="README.md",
    url="https://github.com/ohnas/python_package_tutorial",
    project_urls={
        "Bug Tracker": "https://github.com/ohnas/python_package_tutorial/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
