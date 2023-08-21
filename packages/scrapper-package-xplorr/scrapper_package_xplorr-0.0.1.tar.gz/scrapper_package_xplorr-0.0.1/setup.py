import setuptools
 
setuptools.setup(
    name="scrapper",
    version="0.0.1",
    author="Salil Misra",
    author_email="salil.learner@gmail.com",
    description="Package to scrap data",
    long_description="Data Scrapper",
    long_description_content_type="text/markdown",
    packages=["scrapper/core", "scrapper/extractors", "scrapper/."],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)