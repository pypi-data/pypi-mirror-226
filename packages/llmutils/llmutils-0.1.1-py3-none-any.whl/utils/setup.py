from setuptools import setup, find_packages
import os

setup(
    name='llmutils',
    version='0.1',
    author='ttthree',
    author_email='tongjie@gmail.com',
    description='A few utility classes for working with LLMs',
    packages=find_packages(),
    install_requires=[
        'faiss-cpu',
        'openai',
        'jinja2',
        'python-dotenv',
        'tiktoken'
    ],
)

print(find_packages(os.path.dirname(__file__)))