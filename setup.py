
m setuptools import setup, find_packages

setup(
    name="pyfly",
    version="0.1",
    packages=find_packages(),
    install_requires=['SQLAlchemy>=1.0.13'],
    author="alexnad",
    author_email="alexandernadjarian@gmail.com",
    description="native python graph database",
    license="GNU",
    keywords="graph database NoSQL databases",
    url="https://github.com/alexnad/PyFlyDB"
)

