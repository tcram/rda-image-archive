create table log 
(
    log_id unsigned smallint primary key auto_increment,

    ship_id unsigned smallint not null,
    archive_id unsigned tinyint not null,

    /* Should instrumental specifications and units be updated for each logbook? */
    /* TODO create "resolution" from observations_per_page and timewindow. */
    marine_region_description varchar(1000) comment 'Comma separated list of colloquial marine region names. Can include seas, sandbanks, seamounts, ridges, bays, sampling stations, or ports.',

    foreign key (ship_id) references ship(ship_id) on delete restrict,
    foreign key (archive_id) references archive(archive_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    
