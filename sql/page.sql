create table page /* By "page" here is meant a single scanned image of a logbook. */
(
    page_id char(32) primary key comment '32-char hexidecimal page UUID. Generated during image file import (by removing hyphens from 36-char UUID).',
    /* For development, I am abandoning binary representation in favor of hexidecimal representations. */
    /* TODO page_id binary(16) primary key comment '16-byte representation of 32-char hexidecimal page UUID. Generated during image file import (by removing hyphens from 36-char UUID).', */
    /* TODO page_id_hex char(32) generated always as (hex(page_id)), */
    page_file_ext varchar(10) comment 'Image file extension, e.g., "jpg" or "JPG" but not ".jpg".',

    log_id smallint not null,
    order_within_log int(4) not null comment 'Order of page relative to other pages in the parent logbook.', 

    local_start_date date default null comment 'Format: "YYYY-MM-DD", or, numerically, YYYYMMDD. Local date at page start.',
    local_start_time time default "00:00:00" comment 'Format: "HH:MM:SS", or, numerically, HHMMSS. Local time at page start. Should be entered as a postive value between "00:00" (or 000000) and "23:59" (or 235900).',
    local_time_zone time default null comment 'Format: should be entered as a signed value between "-12:00" (or -120000) and "12:00" (or 120000). The local timezone at page start is defined to be the (signed) hours and minutes from UT1 solar time to local time. For example, in timezone -03:30, the local time 15:00 refers to the UT1 time 18:30.',

    location_description varchar(100) default null comment 'Colloquial name or short description of location.',

    /* Here's UT1 datetime for the page start; child entries in the 'observation' table will be indexed by their temporal distance from this point. */
    ut1_start_datetime datetime generated always as (date_sub(local_start_date, interval local_time_zone hour_second)) comment 'UT1 datetime at page start.',

    /* TODO page_size  */
    /* TODO page_file_format */

    index page_of_log (log_id, order_within_log),
    foreign key (log_id) references log(log_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into page 
(
    page_id,
    log_id,
    order_within_log,
    local_start_date,
    local_start_time,
    local_time_zone
)
values
(
    "testpage", 
    0,
    0, 
    "1850-01-05", 
    "00:00", 
    "-03:30" 
);
