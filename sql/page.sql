create table page 
(
    page_id binary(16) not null primary key,
    local_start_date date comment 'Page start date in local time. Format: YYYY-MM-DD'
    local_timezone varchar(6) comment 'Offset from UTC to the local time, e.g. for "15:00−03:30" do 15:00 − (−03:30) to get 18:30 UTC. Format: "HH:MM" or "-HH:MM"'

    /* pid_hex varchar(32) generated always as hex(pid_bin) virtual, # TODO needs extension */
    /* psize bigint, */
    /* lid int not null, */
    /* pformat varchar(10), */
    /* porder int not null */
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
