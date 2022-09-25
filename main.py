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
                      '{data[constants.REQUEST]}',
                       {data[constants.STATUS]},
                      '{data[constants.DELAY]}',
                      '{data[constants.CREDIT].replace("'","''")}',
                      '{data[constants.CITY]}',
                      '{data[constants.REGION]}',
                      '{data[constants.REGION_CODE]}',
                      '{data[constants.REGION_NAME]}',
                      '{data[constants.AREA_CODE]}',
                      '{data[constants.DMA_CODE]}',
                      '{data[constants.COUNTRY_CODE]}',
                      '{data[constants.COUNTRY_NAME]}',
                       {data[constants.IN_EU]},
                       {bool(data[constants.EU_VAT_RATE])},
                      '{data[constants.CONTINENT_CODE]}',
                      '{data[constants.CONTINENT_NAME]}',
                       {data[constants.LATITUDE]},
                       {data[constants.LONGITUDE]},
                       {data[constants.LOCATION_ACCURACY_RADIUS]},
                      '{data[constants.TIMEZONE]}',
                      '{data[constants.CURRENCY_CODE]}',
                      '{data[constants.CURRENCY_SYMBOL]}',
                      '{data[constants.CURRENCY_SYMBOL_UTF8]}',
                       {data[constants.CURRENCY_CONVERTER]})"""

        print("Executing query: " + query)
        conn.execute(query)
        conn.commit()
        conn.close()
    else:
        print ("HTTP request to obtain ip info failed: Error code: " + str(response.status_code))

    # Sleeping for one minute before next iteration
    #
    print ("Sleeping for " + str(constants.SLEEP_INTERVAL_SECONDS) + " seconds")
    time.sleep(constants.SLEEP_INTERVAL_SECONDS)
