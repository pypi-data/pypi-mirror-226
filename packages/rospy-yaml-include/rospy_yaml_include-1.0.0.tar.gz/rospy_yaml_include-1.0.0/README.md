# rospy_yaml_include

## Introduction

rospy_yaml_include is a package that provides a YAML loader that can include other YAML files.

It can either include a file given an absolute path, or given a ROS package name and a relative path.

rospy_yaml_include has a recursive check to prevent circular imports.

### Usage

The following section contains code snippets showing example usage of the package.
Additionally, the tests directory contains a few examples of how to use the package.

Note that alternative to the below example which use inline yaml, the yaml.load command can be used within a `with open()` statement to load yaml from a file.

### Including a yaml from a ROS package

```python
from rospy_yaml_include.yaml_include import RospyYamlInclude

yml = """
    value:
    - 10
        fields: !ros_include
                package: rospy_yaml_include_test
                extension: test_files/circular_import_ros.yaml
    """

constructor = RospyYamlInclude()
yaml.load(yml, Loader=constructor.add_constructor())
```

### Dynamic loading of yaml files

Using the `!include` tag, YamlInclude will attempt to infer whether a dynamic of an absolute path is provided. If the path provided has a leading / when it is treated as an absolute path, otherwise it is treated as a relative path. If the path provided is a relative path, then the base_directory parameter must be set during instantiation or else a error will be raised.

#### Including a yaml from a relative path with dynamic tag

```python
from rospy_yaml_include.yaml_include import RospyYamlInclude
import os

cwd = os.getcwd()

yml = """
    value:
    - 10
    fields: !include test_files/import.yaml
    """

constructor = RospyYamlInclude(base_directory=cwd)
yaml.load(yml, Loader=constructor.add_constructor())
```

#### Including a yaml from an absolute path with dynamic tag

```python
from rospy_yaml_include.yaml_include import RospyYamlInclude

yml = """
    value:
    - 10
    fields: !include /path/to/file.yml
    """

constructor = RospyYamlInclude()
yaml.load(yml, Loader=constructor.add_constructor())
```

### Including a yaml with a relative path

The YamlInclude class contains an optional parameter to set a base path. If this base path is set during instantiation, then the !relative_include flag can be used

```python
from rospy_yaml_include.yaml_include import RospyYamlInclude
import os

cwd = os.getcwd()

yml = """
    value:
    - 10
    fields: !relative_include test_files/import.yaml
    """

constructor = RospyYamlInclude(base_directory=cwd)
yaml.load(yml, Loader=constructor.add_constructor())
```

### Including a yaml from an absolute path

```python
from rospy_yaml_include.yaml_include import RospyYamlInclude

yml = """
    value:
    - 10
    fields: !path_include /path/to/file.yml
    """

constructor = RospyYamlInclude()
yaml.load(yml, Loader=constructor.add_constructor())
```
