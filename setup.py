import os
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = "django-blogger",
    version = "0.2.0.6",
    author = "Jake Gaylor",
    author_email = "jake@codegur.us",
    description = "A package to administer a simple blog via Django.",
    url = "https://github.com/jhgaylor/django-simple-blog/",
    install_requires = [ln for ln in open('requirements.txt')],
    packages = ['Blogger', 'Blogger.themes', 'Blogger.themes.4col', 'Blogger.themes.3col', 'Blogger.themes.3col'],#find_packages(), 
    #package_data=package_data,
    include_package_data = True,
)