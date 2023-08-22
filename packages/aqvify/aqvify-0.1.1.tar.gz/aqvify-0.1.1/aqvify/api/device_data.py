class DeviceDataAPI:
    def __init__(self, api):
        self.api = api

    def get_latest_value(self, device_key):
        endpoint = '/api/v1/DeviceData/LatestValue'
        params = {'deviceKey': device_key}
        return self.api.get(endpoint, params=params)

    def get_minute_values(self, device_key, begin_time, end_time):
        endpoint = '/api/v1/DeviceData/MinuteValues'
        params = {
            'deviceKey': device_key,
            'beginTime': begin_time,
            'endTime': end_time
        }
        return self.api.get(endpoint, params=params)

    def get_hour_aggregate_values(self, device_key, begin_time, end_time):
        endpoint = '/api/v1/DeviceData/HourAggregateValues'
        params = {
            'deviceKey': device_key,
            'beginTime': begin_time,
            'endTime': end_time
        }
        return self.api.get(endpoint, params=params)

    def get_day_aggregate_values(self, device_key, begin_time, end_time):
        endpoint = '/api/v1/DeviceData/DayAggregateValues'
        params = {
            'deviceKey': device_key,
            'beginTime': begin_time,
            'endTime': end_time
        }
        return self.api.get(endpoint, params=params)
