from apispec_helper.path.path_item import PathItem


class PathBase:
    def __init__(self, path: str, path_item_definition: PathItem):
        self.__path_item_definition = path_item_definition
        self.__path = path

    @property
    def operations(self):
        return self.__path_item_definition.to_dict()['operations']

    @property
    def summary(self):
        return self.__path_item_definition.to_dict()['summary']

    @property
    def description(self):
        return self.__path_item_definition.to_dict()['description']

    @property
    def servers(self):
        return self.__path_item_definition.to_dict()['servers']

    @property
    def parameters(self):
        return self.__path_item_definition.to_dict()['parameters']

    @property
    def path(self):
        return self.__path

    @property
    def apispec_parameter(self) -> dict:
        parameter_list = ["path", "operations", "summary", "description", "servers", "parameters"]
        parameter_dict = dict()

        for parameter in parameter_list:
            try:
                value = getattr(self, parameter)
                parameter_dict[parameter] = value
            except KeyError:
                pass

        return parameter_dict
