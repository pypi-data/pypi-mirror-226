from setuptools import setup

setup(
    name='cdbc',
    version='0.0.2',
    author='Blackwell',
    author_email='friendlyblackwell@example.com',
    url='https://github.com/friendlyblackwell/cdbc',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    description='Common Database Connector',
    packages=['cdbc'],
    install_requires=[
        "PyYAML",
        "psycopg2-bin"
        "redis"
    ]
)