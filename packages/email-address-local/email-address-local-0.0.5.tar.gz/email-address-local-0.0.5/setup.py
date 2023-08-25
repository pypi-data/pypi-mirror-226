import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
     name='email-address-local',  
     version='0.0.5', # https://pypi.org/project/external-user-local/
     author="Circles",
     author_email="info@circles.life",
     # TODO: Please update the description and delete this line
     description="Email Address Local PyPI Package",
     # TODO: Please update the long description and delete this line    
     long_description="Email Address Local PyPI Package",
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
