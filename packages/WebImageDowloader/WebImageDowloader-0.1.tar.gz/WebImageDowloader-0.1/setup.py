from setuptools import setup
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()
setup(
    name='WebImageDowloader',
    version='0.1',
    description='Python library to download images from a URL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Raheel Asghar Ghauri',
    author_email='raheelghauri786@hotmail.com',
    packages=['WebImageDowloader'],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)