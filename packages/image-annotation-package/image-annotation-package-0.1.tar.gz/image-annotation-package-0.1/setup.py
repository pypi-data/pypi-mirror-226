from setuptools import setup, find_packages

setup(
    name='image-annotation-package',
    version='0.1',
    description='An image annotation tool',
    author='Prem Varma',
    author_email='prem.varma@skylarklabs.ai',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
    ],
)
