# TODO: Signal test enable by default !!!!


import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
version_str = '0.1a14'

setup(
    name='dunderlab-foundation',
    version=version_str,
    packages=['foundation'],

    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',

    download_url='https://github.com/dunderlab/python-dunerlab.foundation',

    install_requires=[
        'docker',
        'radiant-framework',
    ],

    include_package_data=True,
    license='BSD-2-Clause',
    description="",

    long_description=README,
    long_description_content_type='text/markdown',

    python_requires='>=3.11',

    # entry_points={
    # 'console_scripts': ['bci-framework=bci_framework.__main__:main'],
    # },

    scripts=[
        "cmd/foundation_status",
        "cmd/foundation_logs",
        "cmd/foundation_start",
        "cmd/foundation_worker",
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],

)



