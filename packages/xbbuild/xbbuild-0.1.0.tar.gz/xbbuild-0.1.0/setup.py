from setuptools import setup

setup(
    name='xbbuild',
    version='0.1.0',
    packages=['xbbuild'],
    url='https://github.com/exbee49/xbbuild',
    license='WTFPL',
    author='exbee49',
    description='Python Build utilities',
    long_description="Some Python build helper",
    long_description_content_type="text/plain",
    install_requires=['xbutils>=0.7.0'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['xbbuild=xbbuild.main:main', ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        # "license :: Public Domain :: WTFPLv2",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
