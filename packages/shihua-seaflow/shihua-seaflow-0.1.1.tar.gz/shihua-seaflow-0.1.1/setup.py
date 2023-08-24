from setuptools import setup,find_packages

### open readme.md with utf-8.
with open("README.md","r",encoding="utf-8") as fh:
        long_description = fh.read()

setup(
        ### information about package and author.
        name = 'shihua-seaflow',
        version = '0.1.1',
        author = 'shihua',
        author_email = "15021408795@163.com",
        python_requires = ">=3.9.13",
        license = "BSD 3 clause",

        ### source codes and dependencies
        packages = find_packages(),
        include_package_data = True,
        description = 'Seaflow is an algorithm orchestration tool developed based on directed acyclic graphs. Its main functions include algorithm workflow orchestration, automatic optimization of runtime parallel scheduling, cache optimization, and support for heterogeneity.',
        # install_requires = ['ray','networkx','matplotlib','pluggy'],

        ### package entry point and CLI index
        # entry_points = {
        #     'console_scripts': [
        #         'seaflowctl = seaflow.cli:seaflow'
        #     ]
        # }      

        ### pypi config
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/redblue0216/Seaflow",
        classsifiers = [
                "Programming Language :: Python :: 3.9",
                "License :: OSI Approved :: BSD License",
                "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]       
)