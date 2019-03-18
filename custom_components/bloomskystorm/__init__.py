"""
Support for BloomSky weather station.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/bloomsky/
"""
from datetime import timedelta
import logging

from aiohttp.hdrs import AUTHORIZATION
import requests
import voluptuous as vol

from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

BLOOMSKYSTORM = None
BLOOMSKYSTORM_TYPE = ['sensor']

DOMAIN = 'bloomskystorm'

# The BloomSky only updates every 5-8 minutes as per the API spec so there's
# no point in polling the API more frequently
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=300)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the BloomSky component."""
    api_key = config[DOMAIN][CONF_API_KEY]

    global BLOOMSKYSTORM
    try:
        BLOOMSKYSTORM = BloomSkyStorm(api_key)
    except RuntimeError:
        return False

    for component in BLOOMSKYSTORM_TYPE:
        discovery.load_platform(hass, component, DOMAIN, {}, config)

    return True


class BloomSkyStorm:
    """Handle all communication with the BloomSky API."""

    # API documentation at http://weatherlution.com/bloomsky-api/
    API_URL = 'http://api.bloomsky.com/api/skydata'

    def __init__(self, api_key):
        """Initialize the BookSky."""
        self._api_key = api_key
        self.devices = {}
        _LOGGER.debug("Initial BloomSky Storm device load...")
        self.refresh_devices()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def refresh_devices(self):
        """Use the API to retrieve a list of devices."""
        _LOGGER.debug("Fetching BloomSky Storm update")
        response = requests.get(
            self.API_URL, headers={AUTHORIZATION: self._api_key}, params={'unit':'intl'}, timeout=10)
        if response.status_code == 401:
            raise RuntimeError("Invalid API_KEY")
        elif response.status_code != 200:
            _LOGGER.error("Invalid HTTP response: %s", response.status_code)
            return
        # Create dictionary keyed off of the device unique id
        self.devices.update({
            device['DeviceID']: device for device in response.json()
        })