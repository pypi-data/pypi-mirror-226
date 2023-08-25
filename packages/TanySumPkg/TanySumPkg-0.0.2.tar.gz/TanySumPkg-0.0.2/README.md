## Practice Project

## Steps to deploy to PyPI
1. Install twine
2. Add setup.py and update version in it everytime you publish a release.
3. Command Line: python setup.py sdist bdist_wheel
4. Command Line: twine upload dist/*
5. Use Credentials
