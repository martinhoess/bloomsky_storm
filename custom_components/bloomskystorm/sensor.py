"""
Support the sensor of a BloomSky weather station.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/sensor.bloomsky/
"""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (TEMP_FAHRENHEIT, CONF_MONITORED_CONDITIONS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['bloomskystorm']

"""
‘uvindex’ - UV Index
‘rainrate’ - 10 mins rainfall
‘raindaily’ - daily rainfall in total (12am-11:59pm)
‘24hRain’ - 24 hour rainfall (a rolling 24 hour window)
‘Winddirection’
‘sustainwindspeed’ - rolling two minute average wind speed
‘windgust’ - highest wind speed (peak speed in a rolling 10 minute window)
"""

# These are the available sensors
SENSOR_TYPES = ['UVIndex',
                'RainRate',
                'SustainedWindSpeed',
                'RainDaily',
                'WindDirection',
                'WindGust',
                '24hRain']

# Sensor units - these do not currently align with the API documentation
SENSOR_UNITS = {'RainRate': 'mm',
                'SustainedWindSpeed': 'm/s',
                'RainDaily': 'mm',
                'WindDirection': '',
                'WindGust': 'm/s',
                '24hRain' : 'mm'}       

# Which sensors to format numerically
FORMAT_NUMBERS = ['RainRate', 'SustainedWindSpeed', 'RainDaily', 'WindGust', '24hRain']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the available BloomSky weather sensors."""
    bloomskystorm = hass.components.bloomskystorm
    # Default needed in case of discovery
    sensors = config.get(CONF_MONITORED_CONDITIONS, SENSOR_TYPES)

    for device in bloomskystorm.BLOOMSKYSTORM.devices.values():
        for variable in sensors:
            add_entities(
                [BloomSkyStormSensor(bloomskystorm.BLOOMSKYSTORM, device, variable)], True)


class BloomSkyStormSensor(Entity):
    """Representation of a single sensor in a BloomSky device."""

    def __init__(self, bs, device, sensor_name):
        """Initialize a BloomSky sensor."""
        self._bloomskystorm = bs
        self._device_id = device['DeviceID']
        self._sensor_name = sensor_name
        self._name = '{} {}'.format(device['DeviceName'], sensor_name)
        self._state = None
        self._unique_id = '{}-{}'.format(self._device_id, self._sensor_name)

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the BloomSky device and this sensor."""
        return self._name

    @property
    def state(self):
        """Return the current state, eg. value, of this sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the sensor units."""
        return SENSOR_UNITS.get(self._sensor_name, None)

    def update(self):
        """Request an update from the BloomSky API."""
        self._bloomskystorm.refresh_devices()

        state = \
            self._bloomskystorm.devices[self._device_id]['Storm'][self._sensor_name]

        if self._sensor_name in FORMAT_NUMBERS:
            self._state = '{0:.2f}'.format(state)
        else:
            self._state = state
