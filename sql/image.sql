create table image /* By "image" here is meant exactly one binary file obtained from a scanning the parent document. */
(
    /* keys */
    image_id char(32) primary key comment '32-char hexidecimal image UUID. Generated during image file import (by removing hyphens from 36-char UUID).',
    document_id smallint not null,

    /* required metadata */
    relative_order int(4) not null comment 'Format: 0000--9999. Describes the order of an image relative to other images in a given document.', 
    media_subtype enum('bmp', 'gif', 'jp2', 'jpeg', 'png', 'tiff') not null,

    /* recommended metadata */
    file_size smallint,

    /* optional metadata */
    location_description varchar(255) comment 'colloquial name or description of location. should be entered verbatim.',
    local_start_date date comment 'format: "yyyy-mm-dd", or, numerically, yyyymmdd. local date at image start.',
    local_start_time time default "00:00:00" comment 'format: "hh:mm:ss", or, numerically, hhmmss. local time at image start. should be entered as a postive value between "00:00" (or 000000) and "23:59" (or 235900).',
    local_time_zone time comment 'format: should be entered as a signed value between "-12:00" (or -120000) and "12:00" (or 120000). the local timezone at image start is defined to be the (signed) hours and minutes from ut1 solar time to local time. for example, in timezone -03:30, the local time 15:00 refers to the ut1 time 18:30.',

    /* virtual metadata */
    ut1_start_datetime datetime generated always as 
        (
            date_sub(local_start_date, interval local_time_zone hour_second)
        ) 
        comment 'UT1 datetime at image start.',
    mime_type varchar(10) generated always as 
        (
            concat_ws('/', "image", media_subtype)
        )
        comment 'Describes the media type (formerly known as MIME type). See https://www.iana.org/assignments/media-types/media-types.xhtml',

    /* indices */
    index image_of_document (document_id, relative_order),
    foreign key (document_id) references document(document_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* testing */
insert into image 
(
    image_id,
    document_id,
    relative_order,
    media_subtype,
    local_start_date,
    local_start_time,
    local_time_zone
)
values
(
    "testimage", 
    0,
    0, 
    "jpeg",
    "1850-01-05", 
    "00:00", 
    "-03:30" 
);

/* TODO */
/* For development, I am abandoning binary representation in favor of hexidecimal representations. We should switch over to binary for memory considerations. */
/* image_id binary(16) primary key comment '16-byte representation of 32-char hexidecimal image UUID. Generated during image file import (by removing hyphens from 36-char UUID).', */
/* image_id_hex char(32) generated always as (hex(image_id)), */
