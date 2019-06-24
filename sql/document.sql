create table document 
(
    /* keys */
    document_id smallint primary key,
    platform_id smallint not null,
    archive_id smallint not null,

    /* required metadata */
    start_date date not null,
    end_date date not null,

    relative_id_item varchar(255) not null,
    relative_id_value varchar(255) not null,

    /* recommended metadata */
    marine_region_description varchar(1000) null comment 'Comma separated list of colloquial marine region names. Can include seas, sandbanks, seamounts, ridges, bays, sampling stations, or ports.',
    create_date date null,

    relative_parent_item varchar(255) null,
    relative_parent_value varchar(255) null,

    /* indices */
    foreign key (platform_id) references platform(platform_id) on delete restrict,
    foreign key (archive_id) references archive(archive_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* TODO */
/* Do we need "resolution" from observations_per_image? */
/* Should instrumental specifications and units be updated within each document? */
/* name varchar(100) generated always as (concat(platform.name ... */

/* testing */
insert into document 
(
    document_id,
    platform_id, 
    archive_id, 
    start_date,
    end_date,
    relative_id_item,
    relative_id_value,
    marine_region_description
) 
values 
(
    0,
    0, 
    0, 
    20190101,
    20190501,
    "nara_id",
    "122179482",
    "North Pacific"
)
