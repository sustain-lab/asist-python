from setuptools import setup

setup(
    name='asist-python',
    version='0.1.0',
    description='Python library to analyze data from ASIST',
    author='Milan Curcic',
    author_email='caomaco@gmail.com',
    url='https://github.com/sustain-lab/asist-python',
    packages=['asist'],
    install_requires=['numpy', 'pytest'],
    test_suite='asist.tests',
    license='MIT'
)
