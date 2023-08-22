class DevicesAPI:
    def __init__(self, api):
        self.api = api

    def get_devices(self):
        endpoint = '/api/v1/Device/Devices'
        return self.api.get(endpoint)
