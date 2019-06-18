create table ship 
(
    ship_id unsigned smallint primary key auto_increment,
    archive_id unsigned tinyint not null,
    /* name varchar(255) */
    /* vessel_description varchar(255) */ 
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
