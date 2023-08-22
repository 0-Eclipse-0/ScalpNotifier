from setuptools import setup, find_packages

requires = [
    'tornado',
    'configparser'
]

setup(
    name='ScalpNotifier',
    version='2.1.0',
    description='A To-Do List built with Tornado',
    author='Matthew Hambecht',
    author_email='matthew.hambrecht@icloud.com',
    keywords='facebook marketplace free',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = App',
        ],
    },
)