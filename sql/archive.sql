create table archive
( 
    archive_id smallint primary key,
    name varchar(40) not null comment 'Archive responsible for "fullest descriptive metadata" of child records, e.g., "The National Archives".',

    host_country char(3) null comment 'Host country of archive. Format: ISO 3166-1 3-letter country code, e.g., "USA" or "GBR".',
    /* host_organization varchar(40) null comment 'Sponsor/funder of archive, e.g., "Smithsonian Institution".', */

    api_documentation varchar(200) null comment 'Link to documentation of (metadata) API provided by archive.',
    api_url varchar(200) null comment 'API paths are relative to this base URL.'

    /* notes varchar(1000) null, */
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into archive
(
    archive_id,
    name,
    host_country
)
values
(
    0,
    "Test Archive",
    "USA"
);
