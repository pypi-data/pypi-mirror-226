from setuptools import setup, find_packages

setup(
    name='rggrader',
    version='0.1.3',
    description='Submission tool for REA course',
    author='Aditira Jamhuri',
    author_email='aditira.jamhuri@ruangguru.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'google-auth',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-auth-urllib3',
        'google-api-python-client'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)