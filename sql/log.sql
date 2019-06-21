create table log 
(
    log_id unsigned smallint auto_increment primary key,
    ship_id unsigned smallint,
    /* observations_per_page int(2) default 24 comment '(0--99) Number of meteorological observations per page.', */
    /* template enum('') comment 'Template for logbook.', */
    /* marine_regions varchar(1000) comment 'Comma separated list of marine region names (fuzzy). Can include seas, sandbanks, seamounts, ridges, bays, sampling stations, or ports.' */
    foreign key (ship_id) references ship(ship_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

    
