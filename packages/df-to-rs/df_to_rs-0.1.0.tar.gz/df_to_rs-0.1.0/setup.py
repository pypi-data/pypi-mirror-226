
from setuptools import setup, find_packages

setup(
    name='df_to_rs',
    version='0.1.0',
    author='Ankit Goel',
    author_email='ankitgoel888@gmail.com',
    description='A utility to copy data from pandas DataFrame to Redshift via S3.',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pandas',
        'psycopg2-binary',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
