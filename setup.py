"""Packaging dlpro."""

from setuptools import setup, find_packages


setup(
    name='dlpro',
    version='0.3.6',
    license='Geeks Trident License',
    license_files=['LICENSE'],
    description='Python module for querying dictionary or list object.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Tuyen Mathew Duong',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=['pyyaml', 'compare_versions', 'python-dateutil'],
    url='https://github.com/Geeks-Trident-LLC/dlpro',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'dlpro = dlpro.main:execute',
            'dlpro-gui = dlpro.application:execute',
            'dl-pro = dlpro.application:execute'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
