create table page 
(
    page_id binary(16) primary key comment '16-byte representation of 32-char hexidecimal page UUID. Generated during image file import (by removing hyphens from 36-char UUID).',
    page_id_hex char(32) generated always as (hex(page_id)) virtual,
    /* "MySQL will automatically convert a date or time to its numerical equivalent when it is used in a numerical context; and it will do the reverse as well." (Dyer, 2005) */
    local_start_date date default null comment 'Format: "YYYY-MM-DD", or, numerically, YYYYMMDD. Local date at page start.',
    local_start_time time default "00:00:00" comment 'Format: "HH:MM:SS", or, numerically, HHMMSS. Local time at page start. Should be entered as a postive value between "00:00" (or 000000) and "23:59" (or 235900).',
    local_time_zone time default null comment 'Format: should be entered as a signed value between "-12:00" (or -120000) and "12:00" (or 120000). The local timezone at page start is defined to be the (signed) hours and minutes from UT1 solar time to local time. For example, in timezone -03:30, the local time 15:00 refers to the UT1 time 18:30.',
    ut1_start_datetime datetime generated always as (date_sub(local_start_date, interval local_time_zone hour_second))
    /* TODO psize bigint, */
    /* lid int not null, */
    /* pformat varchar(10), */
    /* porder int not null */
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into page (page_id, local_start_date, local_start_time, local_time_zone) values ("snarf", "1850-01-05", "00:00", "-03:30" );

