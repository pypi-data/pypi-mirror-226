from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Diffusivity analytics'
LONG_DESCRIPTION = 'A package that allows to work with information diffusion'

# Setting up
setup(
    name="SMAdiffz",
    version=VERSION,
    author="H.M.M.Caldera",
    author_email="<maneeshac2020@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description='This package is for social media informaiton diffusion analysis',
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'social media'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)