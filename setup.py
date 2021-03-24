import setuptools

setuptools.setup(
    name="ttkbootstrap",
    version="0.0.1",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="A collection of ttk themes inspired by Bootstrap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)