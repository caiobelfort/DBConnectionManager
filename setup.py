from setuptools import setup

setup(
    name='db_connection_manager',
    version='0.02b',
    description='A project for management of connections of databases',
    author='Caio Belfort',
    author_email='caiobelfort90@gmail.com',
    license='GPL',
    packages=['db_connection_manager'],
    zip_safe=False,
    install_requires=['sqlalchemy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
    ]
)