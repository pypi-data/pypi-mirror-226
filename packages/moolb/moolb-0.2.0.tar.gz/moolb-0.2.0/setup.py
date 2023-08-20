from setuptools import setup

f = open('./README.md', 'r')
long_description = f.read()
f.close()

setup(
        name='moolb',
        version='0.2.0',
        description='Simple bloom filter with pluggable hash backend',
        author='Louis Holbrook',
        author_email='dev@holbrook.no',
        license='WTFPL',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=[
            'moolb',
        ],
        url='https://gitlab.com/nolash/python-moolb',
        )
