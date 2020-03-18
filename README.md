[BloomSky Storm Component](https://github.com/martinhoess/bloomsky_storm) for Home Assistant

# What This Is:
This is a custom [Homeassistant](https://home-assistant.io) component for the [BloomSky Storm weather station](https://www.bloomsky.com/product). This component is based on the Home Assistant [BloomSky component](https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/bloomsky).

# What It Does:
It reads the [BloomSky Storm](https://www.bloomsky.com/product) data via the [BloomSky API](http://weatherlution.com/wp-content/uploads/2016/01/v1.6BloomskyDeviceOwnerAPIDocumentationforBusinessOwners.pdf):

* uvindex
* rainrate - 10 mins rainfall
* raindaily - daily rainfall in total (12am-11:59pm)
* 24hRain - 24 hour rainfall (a rolling 24 hour window)
* winddirection
* sustainwindspeed - rolling two minute average wind speed
* windgust - highest wind speed (peak speed in a rolling 10 minute window)

# Requirements

This component uses the new HA folder/file component structure. So HA >= [0.88](https://www.home-assistant.io/blog/2019/02/20/release-88/) is required!

# Installation

Place the bloomskystorm folder inside your custom_components folder (create if it not exists)


# Configuration

Same as the BloomSky component

    bloomskystorm:
      api_key: YOUR_API_KEY
      
      
To get the m/s values in km/h you have to multiply it with 3.6

    - platform: template
      sensors:
        wind_sustainedwindspeed:
          value_template: "{{ ((states('sensor.yourstation_sustainedwindspeed') | float) * 3.6) | round(1) }}"
          unit_of_measurement: km/h
          friendly_name: Wind "2 Min. Ø"

        wind_windgust:
          value_template: "{{ ((states('sensor.yourstation_windgust') | float) * 3.6) | round(1) }}"
          unit_of_measurement: km/h
          friendly_name: Wind max. "10 Min."    


# ToDo
* Merge with the HA BloomSky component (to reduce the API requests)
* Rename component to bloomsky_storm (to match repository name)
* Data boundary checks (if the storm offline the API delviers values which are not usable (e.g. 20000 km/h windspeed)

# Changelog
* 2019-03-19 Initial Commit

# License
[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0. This is required for Home Assistant contributions.
