from setuptools import setup, find_packages

setup(
    name='pagerd_snapf',
    version='1.2',
    description='Package for interacting with PagerDuty service',
    author='Mauricio Ayales',
    author_email='mayales@snapfinance.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        ],
)