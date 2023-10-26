from setuptools import setup

setup(
   name='evm',
   version='1.0',
   description='Eulerian Video Magnification',
   author='Hussem Ben Belgacem',
   author_email='hussem.benbelgacem@gmail.com',
   packages=['evm'],
   install_requires=['numpy', 'opencv_python', 'scipy', 'tqdm'],
)