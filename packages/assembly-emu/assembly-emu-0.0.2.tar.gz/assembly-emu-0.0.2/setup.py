import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="assembly-emu",
    version="0.0.2",
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
    package_dir={"": "assembly_emulator"},
    packages=setuptools.find_packages(where="assembly_emulator"),
    python_requires=">=3.6"
)
