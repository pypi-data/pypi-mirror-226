from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'A very simplistic templating "language" for quick and easy development of static sites.'

setup(
        name='iJustWantTemplating',
        version=VERSION,
        author='Neo Sahadeo',
        author_email='',
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'templating', 'static sites', 'static generation'],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
        ]
)
