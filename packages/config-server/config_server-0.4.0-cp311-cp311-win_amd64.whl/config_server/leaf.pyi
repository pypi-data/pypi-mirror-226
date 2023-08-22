from config_server.node import ConfigNode as ConfigNode
from pydantic import RootModel

class ConfigLeaf(RootModel, ConfigNode):
    def __eq__(self, other): ...
