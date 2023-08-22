import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='drdb',
    version="0.0.2",
    author='DrDataYE',
    author_email='drdstaye@gmail.com',
    description='Database.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DrDataYE/DrDB',
    package_dir={"":"src"},
    packages=setuptools.find_packages("src"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
	    'Programming Language :: Python :: 3.10',
	    'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License'],
)

