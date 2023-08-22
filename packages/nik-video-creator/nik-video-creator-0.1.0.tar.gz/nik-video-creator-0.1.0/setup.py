from setuptools import setup

setup(
    name='nik-video-creator',
    version='0.1.0',    
    description='A example Python package',
    url='',
    author='Nikhil Sharma',
    author_email='nikhilsharma972@gmail.com',
    license='BSD 2-clause',
    packages=['nik-video-creator'],
    install_requires=['opencv-python',
                      'numpy', 
                      'pillow'                  
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)