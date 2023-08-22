import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="for-django-projects",
    version="1.0.7",
    author="Jasmany Sanchez Mendez",
    author_email="jasmanysanchez97@gmail.com",
    description="Package of libraries for Django projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasmanysanchez/for-django-projects",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=2.2',
        'django-select2>=7.7.1',
        'numpy>=1.19.5',
        'pandas>=1.1.5',
        'python-dateutil>=2.8.2',
        'xlwt>=1.3.0',
    ],
)