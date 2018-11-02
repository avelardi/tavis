from distutils.core import setup

setup(
    name='Tavis',
    version='0.0.1',
    author='Tony Velardi',
    author_email='tony@velardi.io',
    packages=['tavis'],
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/tavis/',
#    license='LICENSE.txt',
    description='Vulnerability Manager',
    long_description=open('README.md').read(),
    install_requires=[
        # "Django >= 1.1.1",
        # "caldav == 0.1.4",
    ],
)