from setuptools import setup, find_packages

setup(
    name='kuttle',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here if needed in the future
    ],
    author='Dima Solodukha',
    author_email='ds@ktl.ai',
    description='A simple deployment package for ML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kuttleio/kuttle',  # Replace with your repo URL
)
