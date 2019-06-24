create table log 
(
    log_id smallint primary key,
    ship_id smallint not null,
    archive_id smallint not null,

    name varchar(100) default null,

    /* Should instrumental specifications and units be updated for each logbook? */
    /* TODO create "resolution" from observations_per_page and timewindow. */
    marine_region_description varchar(1000) comment 'Comma separated list of colloquial marine region names. Can include seas, sandbanks, seamounts, ridges, bays, sampling stations, or ports.',

    foreign key (ship_id) references ship(ship_id) on delete restrict,
    foreign key (archive_id) references archive(archive_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    
insert into log 
(
    log_id,
    ship_id, 
    archive_id, 
    name, 
    marine_region_description
) 
values 
(
    0,
    0, 
    0, 
    "Test Log", 
    "Pacific Ocean"
)
