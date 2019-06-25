create table observation 
( 
    /* keys */
    image_id char(32) not null,
    time_after_image_start time not null 
        comment 'Format: a non-negative time entered as "HH:MM" (or HHMMSS). Defined as the displacement in hours and minutes from the start of the parent image (explicitly from `image.ut1_start_datetime`). Note: If `image.local_start_time` of the parent image takes its default value "00:00:00", then `time_after_image_start` for an observation would be given by the local time of this observation. If `image.local_start_time` is nonzero, say, "06:00:00", then an observation made at local time "18:00:00" would have `time_after_image_start` entered as "12:00" (or 120000).',
    primary key 
    (
        image_id, 
        time_after_image_start
    ),

    /* recommended metadata */

        /* atmospheric pressure indicators */
        atmospheric_pressure_indicator bool,

        /* temperature indicators */
        dry_bulb_temperature_indicator bool,
        wet_bulb_temperature_indicator bool,
        unspecified_air_temperature_indicator bool,
        sea_temperature_indicator bool,

        /* wind speed indicators */
        wind_direction_indicator bool,
        wind_speed_indicator bool,

        /* cloud indicators */
        cloud_form_indicator bool,
        cloud_direction_indicator bool,
        cloud_amount_indicator bool,

    /* optional metadata */

        /* platform position */
        longitude float(10,6),
        latitude float(10,6),
        location_fix_indicator bool default 0 comment 'an indicator equal to 1 if longitude and latitude are "fixed" by georeference. else equal to 0, e.g., when location is unspecified or "dead-reckoned".',

        /* platform course and speed */
        local_course float(6,3) comment 'local course is defined as the direction of movement in degrees clockwise (e.g., convert ne to 315 and nne to 337.5) from "local north". this field should be entered verbatim, without correction for the compass type of instrument. true course thus depends on this field, the date, and the parent field `platform.compass_type_of_instrument`.',
        local_speed float(6,3) comment 'should be entered verbatim. this field depends on the parent field `platform.navigation_speed_units`.',

    /* indices */
    foreign key (image_id) references image(image_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* TODO */
/* image_id binary(16) not null, */
/* Standardize indicators from Sec. 4.2.1 "Elements observed", WMO-No. 8 (2010 update). lwww.wmo.int/images/prog/www/IMOP/CIMO-Guide.html */
/* humidity indicators */
/* weather indicators */
/* visibility indicators */
/* precipitation indicators */
/* ocean sea waves and swell indicators */

insert into observation
(
    image_id,
    time_after_image_start,
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
    "testimage",
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
