from setuptools import setup, find_packages

# Read the content of README.md
with open("EXAMPLE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='senstile_utils',
    version='0.1.1',
    packages=find_packages(exclude=['user_tests*', "test*", "test.*"]),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            'requests',
            'pytest-asyncio'
        ]
    },
    python_requires='>=3.6',
    author='Jose Alejandro Concepcion Alvarez',
    author_email='pepe@senstile.com',
    description='A set of common utils modules and functions for Senstile Python Api development',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
