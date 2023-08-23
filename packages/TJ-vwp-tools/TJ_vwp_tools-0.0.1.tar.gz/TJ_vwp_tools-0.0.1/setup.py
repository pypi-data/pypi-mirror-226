import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TJ_vwp_tools",
    version="0.0.1",
    author="Andy Banks",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=['TJ_vwp_tools','TJ_vwp_tools.importing','TJ_vwp_tools.plotting'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
