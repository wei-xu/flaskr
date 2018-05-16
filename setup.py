from setuptools import setup, find_packages

setup(
    name='flaskr',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'werkzeug'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_requires=[
        'pytest',
    ]
)
