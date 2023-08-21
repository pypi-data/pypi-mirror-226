import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="assembly-emu",
    version="0.0.1",
    author="jonaprojects",
    author_email="merkava234@gmail.com",
    description="A basic emulator of asm8086 in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonaprojects/assemblyEmulator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
