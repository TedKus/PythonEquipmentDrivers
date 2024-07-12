import pyvisa


class UnsupportedResourceError(Exception):
    def __init__(self, message="Device is not supported", *args):
        super().__init__(message, *args)


class ResourceConnectionError(Exception):
    def __init__(self, message="Could not connect to device", *args):
        super().__init__(message, *args)


class VisaIOErrorWithRetry(pyvisa.VisaIOError):
    def __init__(self, resource, method, retries, *args, **kwargs):
        self.resource = resource
        self.method = method
        self.retries = retries
        self.args = args
        self.kwargs = kwargs

    def handle(self):
        attempt = 0
        while attempt < self.retries:
            try:
                self.resource.clear_status()
                return self.method(*self.args, **self.kwargs)
            except pyvisa.VisaIOError:
                attempt += 1
        raise self
