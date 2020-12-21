import setuptools
import yet

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yet",
    version=yet.__version__,
    author=yet.__author__,
    author_email=yet.__email__,
    description="yet is a console (kind of rss) application to download youtube videos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nevarman/yet",
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment',
        'Topic :: Utilities',
    ],
    entry_points='''
        [console_scripts]
        yet=yet.main:main
    ''',
    install_requires=[
        'xmltodict',
        'youtube-dl'
    ],
    python_requires='>=3.6',
)
