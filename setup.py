from setuptools import setup

setup(
    name='dbeasy',
    version='0.07',
    description='Database utilities',
    author='Caio Belfort',
    author_email='caiobelfort90@gmail.com',
    license='GPL',
    packages=['dbeasy'],
    zip_safe=False,
    install_requires=['sqlalchemy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
        'Programming Language :: Python :: 3.7',
        'Operation System :: POSIX :: Linux'
    ]
)
