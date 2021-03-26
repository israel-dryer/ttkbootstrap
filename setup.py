import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="ttkbootstrap",
    version="0.0.1",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="A collection of ttk themes inspired by Bootstrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"src": ["*.json"]},
    install_requires=["pillow"],
    python_requires=">=3.6",
)