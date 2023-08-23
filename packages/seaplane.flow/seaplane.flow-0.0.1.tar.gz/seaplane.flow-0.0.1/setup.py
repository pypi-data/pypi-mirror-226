from setuptools import setup, find_namespace_packages


setup(
    name="seaplane.flow",
    version="0.0.1",
    description="",
    long_description="",
    author="Seaplane.IO",
    author_email="carrier-eng@seaplane.io",
    license="Apache Software License",
    packages=find_namespace_packages(include=["seaplane.*"]),
    install_requires=[
        "msgpack>=1.0.5",
    ],
    zip_safe=False,
)
