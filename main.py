""" Script which once in a minute obtains ip related information
    from geoplugin URI and stores them in SQLite database """

import time
import sqlite3
import requests
import constants

# Open connection to a SQLite database stored in a given file.
# Note:
#
#   1) During the first script run, file will be created if it doesn't exist.
#   2) All the following runs will just open existing file
#
#   This makes script idempotent and allows multiple runs of the same script
#   without failures
#
conn = sqlite3.connect(constants.DATABASE_NAME)
print ("Opened database connection successfully")

# Create a table in the database if it already doesn't exist
#
# NOTE:
#   IF NOT EXISTS is important here as it allows us to run the script
#   multiple times without failures saying that table already exists.
#
#   Instead, table will be created during the fist run,
#   while all the following runs will skip this part of the code
#   as table already exists
#
conn.execute('''CREATE TABLE IF NOT EXISTS IP_INFO
    (ID                                INTEGER         PRIMARY KEY     AUTOINCREMENT,
     TIMESTAMP                         DATETIME     DEFAULT CURRENT_TIMESTAMP,
     REQUEST                           TEXT,
     STATUS                            INTEGER,
     DELAY                             TEXT,
     CREDIT                            TEXT,
     CITY                              TEXT,
     REGION                            TEXT,
     REGION_CODE                       TEXT,
     REGION_NAME                       TEXT,
     AREA_CODE                         TEXT,
     DMA_CODE                          TEXT,
     COUNTRY_CODE                      TEXT,
     COUNTRY_NAME                      TEXT,
     IN_EU                             INTEGER,
     EU_VAT_RATE                       INTEGER,
     CONTINENT_CODE                     TEXT,
     CONTINENT_NAME                    TEXT,
     LATITUDE                          REAL,
     LONGITUDE                         REAL,
     LOCATION_ACCURACY_RADIUS          INTEGER,
     TIMEZONE                          TEXT,
     CURRENCY_CODE                     TEXT,
     CURRENCY_SYMBOL                   TEXT,
     CURRENCY_SYMBOL_UTF8              TEXT,
     CURRENCY_CONVERTER                REAL);''')
print ("Table created/opened successfully")


# Close database connection to clear the resources
#
conn.close()
print("Database connection closed")

while True:
    print ("Invoking request to obtain current ip info")
    response = requests.get(constants.GEOPLUGIN_ENDPOINT, timeout=constants.REQUEST_TIMEOUT_SECONDS)

    if response.ok:
        print ("HTTP request to obtain ip succeeded, inserting data into the table")

        # Note, we don't need to open connection here again as we can reuse connection
        # which we opened at the start of the script. However, long open connections
        # are not a good DB practice, especially in a case where after every short
        # transaction we sleep for one minute. In a situation where multiple threads
        # are accessing the database, this would lead to the connection limit hit.
        #
        conn = sqlite3.connect(constants.DATABASE_NAME)

        data = response.json()

        request = data[constants.REQUEST]
        status = data[constants.STATUS]
        delay = data[constants.DELAY]
        credit = data[constants.CREDIT]
        city = data[constants.CITY]
        region = data[constants.REGION]
        regionCode = data[constants.REGION_CODE]
        regionName = data[constants.REGION_NAME]
        areaCode = data[constants.AREA_CODE]
        dmaCode = data[constants.DMA_CODE]
        countryCode = data[constants.COUNTRY_CODE]
        countryName = data[constants.COUNTRY_NAME]
        inEu = data[constants.IN_EU]
        euVatRate = data[constants.EU_VAT_RATE]
        continentCode = data[constants.CONTINENT_CODE]
        continentName = data[constants.CONTINENT_NAME]
        latitude = data[constants.LATITUDE]
        longitude = data[constants.LONGITUDE]
        locationAccuracyRadius = data[constants.LOCATION_ACCURACY_RADIUS]
        timezone = data[constants.TIMEZONE]
        currencyCode = data[constants.CURRENCY_CODE]
        currencySymbol = data[constants.CURRENCY_SYMBOL]
        currencySymbolUTF8 = data[constants.CURRENCY_SYMBOL_UTF8]
        currencyConverter = data[constants.CURRENCY_CONVERTER]

        query = f"""INSERT INTO IP_INFO (
                      REQUEST,
                      STATUS,
                      DELAY,
                      CREDIT,
                      CITY,
                      REGION,
                      REGION_CODE,
                      REGION_NAME,
                      AREA_CODE,
                      DMA_CODE,
                      COUNTRY_CODE,
                      COUNTRY_NAME,
                      IN_EU,
                      EU_VAT_RATE,
                      CONTINENT_CODE,
                      CONTINENT_NAME,
                      LATITUDE,
                      LONGITUDE,
                      LOCATION_ACCURACY_RADIUS,
                      TIMEZONE,
                      CURRENCY_CODE,
                      CURRENCY_SYMBOL,
                      CURRENCY_SYMBOL_UTF8,
                      CURRENCY_CONVERTER)
                    VALUES (
                      '{request}',
                       {status},
                      '{delay}',
                      '{credit.replace("'","''")}',
                      '{city}',
                      '{region}',
                      '{regionCode}',
                      '{regionName}',
                      '{areaCode}',
                      '{dmaCode}',
                      '{countryCode}',
                      '{countryName}',
                       {inEu},
                       {bool(euVatRate)},
                      '{continentCode}',
                      '{continentName}',
                       {latitude},
                       {longitude},
                       {locationAccuracyRadius},
                      '{timezone}',
                      '{currencyCode}',
                      '{currencySymbol}',
                      '{currencySymbolUTF8}',
                       {currencyConverter})"""

        print("Executing query: " + query)
        conn.execute(query)
        conn.commit()
        conn.close()
    else:
        print ("HTTP request to obtain ip info failed: Error code: " + str(response.status_code))

    # Sleeping for one minute before next iteration
    #
    print ("Sleeping for " + constants.SLEEP_INTERVAL_SECONDS + " seconds")
    time.sleep(constants.SLEEP_INTERVAL_SECONDS)
