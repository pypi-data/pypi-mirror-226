

from setuptools import setup, find_packages

VERSION = '0.0.8' 
DESCRIPTION = 'Lame tools to practice with opencv on VScode in place of Jupyter Notebooks.'
LONG_DESCRIPTION = \
"""
The objects in this package are useful to practice with python opencv on VScode.

Generally, it is preferable to use Jupiter Notebook to practice with opencv.
This is because JN allows easy ways to manage and display images.
But in case one wants to do the practice with VScode instead of JN, here comes this library.

This is a 'lame' library because the code is not very efficient.
"""

# Setting up
setup(
        name="lame_helpers_for_opencv_on_vscode", 
        version=VERSION,
        author="tms1991",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "matplotlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['opencv', 'vscode'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

# deploy
#--------

# python setup.py sdist bdist_wheel

# twine upload dist/lame_helpers_for_opencv_on_vscode-0.0.0*
# __token__
# api key

# pip install lame_helpers_for_opencv_on_vscode==0.0.0*