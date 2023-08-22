from setuptools import setup, find_packages

setup(
    name='django_to_exe',
    version='0.1.1',
    description='xxxx',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'django_to_exe': ['static/*','templates/*','db.sqlite3']
    },
    install_requires=[
        'Django==3.2.12',
    ]
)