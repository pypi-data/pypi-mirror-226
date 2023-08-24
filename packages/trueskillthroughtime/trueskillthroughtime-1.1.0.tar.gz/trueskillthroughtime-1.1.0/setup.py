import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trueskillthroughtime",
    version="1.1.0",
    author="Gustavo Landfried",
    author_email="gustavolandfried@gmail.com",
    description="The temporal learning estimator: Individual learning curves with reliable initial estimates and guaranteed comparability between distant estimates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glandfried/TrueSkillThroughTime.py/",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=['trueskillthroughtime'],
    #python_requires=">=3.6",
    download_url = 'https://github.com/glandfried/TrueSkillThroughTime.py/archive/refs/tags/v1.1.0.tar.gz',
    install_requires=[]
)
