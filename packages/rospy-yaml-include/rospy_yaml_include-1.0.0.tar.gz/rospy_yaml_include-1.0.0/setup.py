# Importing Packages
from setuptools import setup

# Reading README and Storing Info as `Long Description`
with open("README.md", "r") as fh:
    long_description = fh.read()

# Configuring Setup
setup(
    name="rospy_yaml_include",
    version="1.0.0",
    description="rospy_yaml_include",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.whoi.edu/acomms/rospy_yaml_include",
    author="WHOI Acomms Group",
)
