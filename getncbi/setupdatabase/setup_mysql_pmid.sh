mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi_pubmed;
create table pmabstractfile(
    pmid int NOT NULL,
    update_time varchar(63),
    file_path varchar(63),
    PRIMARY KEY(pmid),
    KEY key_uptime(update_time)
);
"
