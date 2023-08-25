import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
    name='python-sdk-local',
    version='0.0.5',  # https://pypi.org/project/python-sdk-local/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles Python SDK Local Python",
    # TODO: Please update the long description and delete this line
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
)
