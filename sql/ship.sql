create table ship 
(
    ship_id unsigned smallint primary key auto_increment,
    name varchar(255) not null comment 'Name of ship (or station) responsible for logbooks.',
    /* TODO Create virtual fields for `coverage_start_date` and `coverage_end_date` by querying log table. */
    /* TODO description varchar(1000) not null comment 'Description of ship (or station), e.g., port of registry, tonnage, measure, dimension.', */
    /* TODO Compare to metadata vocabulary in WMO-No. 47 (Metadata Format Version 04). http://www.wmo.int/pages/prog/www/ois/pub47/pub47-home.htm */
    /* TODO Implement units compatible with MetPy https://www.unidata.ucar.edu/blogs/developer/en/entry/metpy-mondays-4-units-in */ 

    compass_type_of_instrument enum('gyro', 'magnetic', 'unspecified')
    compass_units enum('degrees', 'cardinal directions') null,

    /* TODO standardize navigation speeds, see https://en.wikipedia.org/wiki/Pitometer_log */
    navigation_speed_type_of_instrument enum('chip log', 'patent log', 'pit log', 'electromagnetic log', 'propeller rpm') null,
    navigation_speed_units enum('knot', 'kilometers per second') null,

    wind_speed_units enum('beaufort', 'meters per second') null,
    anemometer_instrument_exposure varchar(40) null,
    anemometer_instrument_make_and_number varchar(40) null,

    /* TODO standardize (or convert) dimensional quantities */
    atmospheric_pressure_units enum('inches', 'hectopascal', 'millibar') null, 
    atmospheric_pressure_type_of_instrument varchar(40) null,
    atmospheric_pressure_instrument_make_and_number varchar(40) null,
    atmospheric_pressure_instrument_exposure varchar(40) null,

    temperature_units enum('celcius', 'fahrenheit') null,
    dry_bulb_thermometer_make_and_number varchar(40) null,
    dry_bulb_thermometer_exposure varchar(40) null,
    wet_bulb_thermometer_exposure varchar(40) null,
    wet_bulb_thermometer_make_and_number varchar(40) null,
    sea_temperature_type_of_instrument varchar(40) null,
    sea_temperature_instrument_make_and_number varchar(40) null,
    sea_temperature_instrument_exposure varchar(40) null,

    /* TODO scale_used_for_measuring_waves varchar(40) null, */
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
