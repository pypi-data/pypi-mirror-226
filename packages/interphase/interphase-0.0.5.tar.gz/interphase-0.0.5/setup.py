from setuptools import setup, find_packages

setup(
    name='interphase',
    version='0.0.5',
    description='A Python Library to Generate Typescript Types',
    # package_dir={'':'interphase/src'},
    # py_modules=["interphase"], 
    packages=find_packages(),
    # install_requires=[
    #     'requests',
    #     'importlib-metadata; python_version == "3.8"',
    # ],
    # packages=find_packages(
    #     where='interphase',
    #     include=['*'],
    #     exclude=[],
    # ),
    # entry_points={
    #     'console_scripts': [
    #         'cli-name = mypkg.mymodule:some_func',
    #     ]
    # }
)