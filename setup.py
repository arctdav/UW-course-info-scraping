import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uwaterlooCourseInfoScraper",
    version="1.0.0",
    author="arctdav",
    author_email="arctdav@gmail.com",
    description="This Python side project scraps all UWaterloo course information \
        from its website, and exports all these information into an Excel file. \
        This script used BeautifulSoup from bs4, request, and csv Python libraries \
        to achieve such goal. Please do not spam their website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arctdav/UW-course-info-scraping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)