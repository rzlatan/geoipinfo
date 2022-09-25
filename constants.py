# Constants

# SQLite database
# 
DATABASE_NAME = 'geoip.db'

# URL for obtaining ip information
#
GEOPLUGIN_ENDPOINT = 'http://geoplugin.net/json.gp?ip=<current_ip>'


# Geo plugin response columns constats
#
REQUEST = "geoplugin_request"
STATUS = "geoplugin_status"
DELAY = "geoplugin_delay"
CREDIT = "geoplugin_credit"
CITY = "geoplugin_city"
REGION = "geoplugin_region"
REGION_CODE = "geoplugin_regionCode"
REGION_NAME = "geoplugin_regionName"
AREA_CODE = "geoplugin_areaCode"
DMA_CODE = "geoplugin_dmaCode"
COUNTRY_CODE = "geoplugin_countryCode"
COUNTRY_NAME = "geoplugin_countryName"
IN_EU = "geoplugin_inEU"
EU_VAT_RATE = "geoplugin_euVATrate"
CONTINENT_CODE = "geoplugin_continentCode"
CONTINENT_NAME = "geoplugin_continentName"
LATITUDE = "geoplugin_latitude"
LONGITUDE = "geoplugin_longitude"
LOCATION_ACCURACY_RADIUS = "geoplugin_locationAccuracyRadius"
TIMEZONE = "geoplugin_timezone"
CURRENCY_CODE = "geoplugin_currencyCode"
CURRENCY_SYMBOL = "geoplugin_currencySymbol"
CURRENCY_SYMBOL_UTF8 = "geoplugin_currencySymbol_UTF8"
CURRENCY_CONVERTER = "geoplugin_currencyConverter"

# Interval constants
#
SLEEP_INTERVAL_SECONDS = 60
REQUEST_TIMEOUT_SECONDS = 10