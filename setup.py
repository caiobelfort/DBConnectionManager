from setuptools import setup

setup(
    name='db_connection_manager',
    version='0.03b',
    description='A project for management of connections of databases',
    author='Caio Belfort',
    author_email='caiobelfort90@gmail.com',
    license='GPL',
    py_modules=['db_connection_manager'],
    zip_safe=False,
    install_requires=['sqlalchemy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
    ]
)