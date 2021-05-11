from setuptools import setup

setup(
    name='Shanno_fano',
    version='1.0',
    entry_points={
        'console_scripts': [
            'shannofano=shannofano:main'
        ]
    },
    packages=[],
    url='',
    license='MIT',
    author='Gergely',
    author_email='-',
    description='Code with a Shannon-fano method and get code efficiency.'
)
