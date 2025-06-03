# Calgary Transit Tracker

# TODO:
- ~~create a db that stores relevant CT_GTFS data~~
- have daily(nightly) cron task that fetches CT_GTFS data and updates db
    - version checking?
    - create a hash for my local version and a hash for the version on the City of Calgary's website and compare the two
    - that way i wont have to check contents of zip file before any updates are done
- have background process that only triggers when event is triggered that will update bus positions
- start packaging files as django project
    - to start i want to just have html form that can request a bus lat/long with no visuals