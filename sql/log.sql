create table log 
(
    log_id unsigned smallint primary key auto_increment,
    ship_id unsigned smallint,
    number_of_daily_observations int(2) default 24,
    /* needs a "transcribed" boolean field */
    /* ltemplate enum(...) */
    /* lregion varchar(40), */
    foreign key (ship_id) references ship(ship_id) on delete restrict
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

    
