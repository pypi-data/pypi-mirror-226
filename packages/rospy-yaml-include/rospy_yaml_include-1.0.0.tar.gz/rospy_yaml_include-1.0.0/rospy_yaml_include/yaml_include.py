"""
rospy_yaml_include
------------------

This module provides a way to include yaml files in other yaml files.
"""

import os
import yaml
import re
import rospkg
import rospy

class RospyYamlInclude:
    """
    RospyYamlInclude class
    """

    def __init__(
        self, loader: type = yaml.SafeLoader, base_directory: str = None, import_limit: int = 150
    ) -> None:
        self.import_limit = import_limit
        self.import_count = 0

        self.loader = loader
        self.base_directory = base_directory

    class _RosInclude:
        """
        Mappping for !ros_include constructor
        """

        def __init__(self, package, extension) -> None:
            self.package = package
            self.extension = extension

    def _ros_include_constructor(
        self, loader: type, node: yaml.nodes.MappingNode
    ) -> dict:
        """
        _ros_include_constructor function handles !ros_include tag
        """
        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        rospack = rospkg.RosPack()

        file = self._RosInclude(**loader.construct_mapping(node))

        include_file = os.path.join(
            rospack.get_path(file.package),
            file.extension,
        )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _path_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _path_include_constructor function handles !path_include tag

        """
        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)

        with open(file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _relative_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _path_include_constructor function handles !relative_include tag

        this can be used to import a yaml relative to a base directory provided in the class init
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        if self.base_directory is None:
            raise ValueError(
                "base_directory must be provided in class init to use !relative_include"
            )

        file = loader.construct_scalar(node)

        include_file = os.path.join(
            self.base_directory,
            file,
        )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _dynamic_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _dynamic_include_constructor function handles !include tag

        this constructor attempts to infer the type of include based on the file extension
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _variable_subsitute_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _variable_subsitute_constructor function handles !variable_substitute tag

        this can be used to substitute a variable in a yaml file
        """

        param_string = loader.construct_scalar(node)
        variables = re.findall(r"\${(.*?)}", param_string)
        for variable in variables:
            fill_param = os.getenv(variable, None)
            if fill_param is not None:
                param_string = param_string.replace(f"${{{variable}}}", str(fill_param))
            else:
                raise ValueError(f"env {variable} not found")

        return param_string

    def _variable_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _variable_include_constructor function handles !variable_include tag

        this can be used to import a yaml while substituting a env variable
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)
        variables = re.findall(r"\${(.*?)}", file)
        for variable in variables:
            fill_param = os.getenv(variable, None)
            if fill_param is not None:
                file = file.replace(f"${{{variable}}}", str(fill_param))
            else:
                raise ValueError(f"env {variable} not found")

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())
        
    def _ros_param_substitute_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _ros_param_substitute_constructor function handles !ros_param_substitute tag

        this can be used to import a yaml substitute a rosparam
        """

        param_string = loader.construct_scalar(node)
        params = re.findall(r"\${(.*?)}", param_string)
        for param in params:
            fill_param = rospy.get_param(param, None)
            if fill_param is not None:
                param_string = param_string.replace(f"${{{param}}}", str(fill_param))
            else:
                raise ValueError(f"rosparam {param} not found")

        return param_string
    def _ros_param_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _ros_param_include_constructor function handles !ros_param_include tag

        this can be used to import a yaml with a rosparam substitution
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)
        params = re.findall(r"\${(.*?)}", file)
        for param in params:
            fill_param = rospy.get_param(param, None)
            if fill_param is not None:
                file = file.replace(f"${{{param}}}", str(fill_param))
            else:
                raise ValueError(f"rosparam {param} not found")

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())
        
    def add_constructor(self) -> type:
        """
        add constructor to yaml
        """

        loader = self.loader
        loader.add_constructor("!ros_include", self._ros_include_constructor)
        loader.add_constructor("!path_include", self._path_include_constructor)
        loader.add_constructor("!relative_include", self._relative_include_constructor)
        loader.add_constructor("!include", self._dynamic_include_constructor)
        loader.add_constructor("!variable_substitute", self._variable_subsitute_constructor)
        loader.add_constructor("!variable_include", self._variable_include_constructor)
        loader.add_constructor("!ros_param_substitute", self._ros_param_substitute_constructor)
        loader.add_constructor("!ros_param_include", self._ros_param_include_constructor)

        return loader
