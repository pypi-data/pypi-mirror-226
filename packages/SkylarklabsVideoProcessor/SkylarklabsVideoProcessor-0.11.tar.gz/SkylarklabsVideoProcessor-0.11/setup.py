from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='SkylarklabsVideoProcessor',
    version='0.11',  # Update the version number
    description='A video processing package',
    author='Prem Varma',
    author_email='prem.varma@skylarklabs.ai',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'ultralytics',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the content type
)
