import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="nd_kafka_md",
    version="0.5.26",
    author="NiTiN DiXiT",
    author_email="nitin.dixit@zopper.com",
    description="Package to create Kafka Producer's & Consumer's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    packages=['.nd_kafka'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)