create table logbooks(
    lid int(11) not null primary key,
    ltemplate varchar(40),
    lregion varchar(40),
    sid int(11) not null
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
    
