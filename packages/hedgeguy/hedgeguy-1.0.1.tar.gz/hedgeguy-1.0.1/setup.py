import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hedgeguy",
    version="1.0.1",
    author="Plotguy Team",
    author_email="plotguy.info@gmail.com",
    description="Hedgeguy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[         
        'pandas==1.5.3',  
        'numpy>=1.24.1',  
        'hkfdb>=2.2', 
        'pyarrow',
        'polars',
        'lxml',        
        'dash',
        'dash_bootstrap_components',
        'dash_daq',
        'dash_dangerously_set_inner_html',
    ],
    url="https://pypi.org/project/plotguy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)