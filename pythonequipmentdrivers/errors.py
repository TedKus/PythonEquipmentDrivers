class UnsupportedResourceError(Exception):
    def __init__(self, message="Device is not supported", *args):
        super().__init__(message, *args)


class ResourceConnectionError(Exception):
    def __init__(self, message="Could not connect to device", *args):
        super().__init__(message, *args)


class EquipmentDriverError(IOError):
    """Base exception for all PythonEquipmentDrivers errors
    Extends the existing IOError chain
    Gets caught by any code looking for IOError
    Maintains compatibility with existing error handling
    Provides more specific error types while preserving IOError behavior
    """
    pass


class CommunicationError(EquipmentDriverError):
    """Error during device communication"""
    def __init__(self, address, idn=None, *args):
        message = f"Failed to communicate with device at {address}"
        if idn:
            message += f"\nDevice: {idn}"
        super().__init__(message, *args)


class ConfigurationError(EquipmentDriverError):
    """Error in device configuration or settings"""
    pass
