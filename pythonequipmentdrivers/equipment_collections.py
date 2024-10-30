from pythonequipmentdrivers.resource_collections import (ResourceCollection,
                                                         connect_resources)
from typing import Union
from pathlib import Path
import warnings

__all__ = ["EquipmentCollection", "connect_equipment"]
warnings.simplefilter("default")  # Reset to default


# Backwards compatibility
class EquipmentCollection(ResourceCollection):
    def __init__(self, *args, **kwargs):
        warnings.warn("EquipmentCollection is deprecated and will be removed "
                      "in a future version. "
                      "Use resource_collections.ResourceCollection instead.",
                      DeprecationWarning,
                      stacklevel=3)
        super().__init__(*args, **kwargs)


def connect_equipment(config: Union[str, Path, dict],
                      **kwargs) -> EquipmentCollection:
    warnings.warn("connect_equipment is deprecated and may be removed in a "
                  "future version. EquipmentCollection is also deprecated."
                  "Use resource_collections.connect_resources instead.",
                  DeprecationWarning, stacklevel=2)
    return connect_resources(config, **kwargs)
