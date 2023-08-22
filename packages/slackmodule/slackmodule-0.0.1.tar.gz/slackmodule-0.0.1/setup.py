from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'LOGEX specific slack package'
LONG_DESCRIPTION = '-'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="slackmodule",
    version=VERSION,
    author="Jason Dsouza",
    author_email="<m.a.lupulescu@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'slack', 'logex'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)