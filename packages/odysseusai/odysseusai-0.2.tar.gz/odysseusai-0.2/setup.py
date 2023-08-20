from setuptools import setup, find_packages

setup(
    name="odysseusai",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    author="Christos Ziakas",
    author_email="chziakas@gmail.com",
    description="A package to log LLM models",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chziakas/odysseus_ai",
)