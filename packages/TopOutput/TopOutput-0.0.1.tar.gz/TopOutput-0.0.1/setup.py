from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TopOutput',
    version='0.0.1',
    description='Package for developing insits for the top 10/20 percent for the data which is available.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Aaryan Nair',
    author_email='nairaaryan23@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='top',
    packages=find_packages(),
    install_requries=['']
)