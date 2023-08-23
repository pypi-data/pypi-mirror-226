from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Finwave Python Programs Setup'
LONG_DESCRIPTION = 'Package to help with importing the correct files and folders inside python programs'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="Finwave_python_programs_setup", 
        version=VERSION,
        author="David May",
        author_email="<david70may@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)