create table pages(
    pid binary(16) not null primary key,
    pid_hex varchar(32) generated always as hex(pid_bin) virtual, # TODO needs extension
    psize bigint,
    lid int not null,
    pformat varchar(10),
    porder int not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
