create table observation 
( 
    /* TODO page_id binary(16) not null, */
    page_id char(32) not null,
    time_after_page_start time not null comment 'Format: a non-negative time entered as "HH:MM" (or HHMMSS). Defined as the displacement in hours and minutes from the start of the parent page (explicitly from `page.ut1_start_datetime`). Note: If `page.local_start_time` of the parent page takes its default value "00:00:00", then `time_after_page_start` for an observation would be given by the local time of this observation. If `page.local_start_time` is nonzero, say, "06:00:00", then an observation made at local time "18:00:00" would have `time_after_page_start` entered as "12:00" (or 120000).',
    primary key (page_id, time_after_page_start),

    /* ship position */
    longitude float(10,6) default null,
    latitude float(10,6) default null,
    location_fix_indicator bool default 0 comment 'An indicator equal to 1 if longitude and latitude are "fixed" by georeference. Else equal to 0, e.g., when location is unspecified or "dead-reckoned".',

    /* ship course and speed */
    local_course float(6,3) default null comment 'Local course is defined as the direction of movement in degrees clockwise (e.g., convert NE to 315 and NNE to 337.5) from "local north". This field should be entered verbatim, without correction for the compass type of instrument. True course thus depends on this field, the date, and the parent field `ship.compass_type_of_instrument`.',
    local_speed float(6,3) default null comment 'Should be entered verbatim. This field depends on the parent field `ship.navigation_speed_units`.',

    /* TODO Standardize indicators from Sec. 4.2.1 "Elements observed", WMO-No. 8 (2010 update). lwww.wmo.int/pages/prog/www/IMOP/CIMO-Guide.html */
    /* atmospheric pressure indicators */
    atmospheric_pressure_indicator bool default null,

    /* temperature indicators */
    dry_bulb_temperature_indicator bool default null,
    wet_bulb_temperature_indicator bool default null,
    unspecified_air_temperature_indicator bool default null,
    sea_temperature_indicator bool default null,

    /* TODO humidity indicators */

    /* wind speed indicators */
    wind_direction_indicator bool default null,
    wind_speed_indicator bool default null,

    /* TODO weather indicators */

    /* cloud indicators */
    cloud_form_indicator bool default null,
    cloud_direction_indicator bool default null,
    cloud_amount_indicator bool default null,

    /* TODO visibility indicators */
    /* TODO precipitation indicators */
    /* TODO ocean sea waves and swell indicators */

    unique key observation_of_page (page_id, time_after_page_start),
    foreign key (page_id) references page(page_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into observation
(
    page_id,
    time_after_page_start,
    longitude,
    latitude,
    location_fix_indicator,
    local_course,
    local_speed,
    atmospheric_pressure_indicator,
    dry_bulb_temperature_indicator,
    wet_bulb_temperature_indicator,
    unspecified_air_temperature_indicator,
    sea_temperature_indicator,
    wind_direction_indicator,
    wind_speed_indicator,
    cloud_form_indicator,
    cloud_direction_indicator,
    cloud_amount_indicator
)
values
(
    "testpage",
    060000,
    90.5,
    45.5,
    1,
    60.8,
    2.45,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
);
