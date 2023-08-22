from setuptools import setup, find_packages

setup(
    name='routing_engine',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'jsonpath-ng>=1.5.3',
        'jsonschema>=3.2.0',
        'streamlit>=1.25.0',
    ],
    include_package_data=True,
    author='Annecto',
    author_email='info@annecto.com',
    description='A routing engine for Python',
    url='https://gitlab.internal.ate.lc/numbers-lookup/routing-engine',
)
