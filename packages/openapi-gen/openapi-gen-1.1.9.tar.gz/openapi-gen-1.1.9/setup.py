from setuptools import setup, find_packages

VERSION = '1.1.9'
DESCRIPTION = 'Swagger UI for Flask apps'
LONG_DESCRIPTION = 'Automatically generate OpenAPI UI documentation for a Flask app.  Batteries included.'

setup(
    name='openapi-gen',
    python_requires='>=3.9.0',
    version=VERSION,
    author='Chris Lyons',
    author_email='administrator@suncoast.systems',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_data={'openapi_gen': ['./resources/swagger.pkl']},
    packages=find_packages(),
    install_requires=['flask'],
    keywords=['python', 'openapi-gen'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
