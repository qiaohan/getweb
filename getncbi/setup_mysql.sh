mysql -uroot -pqiaohan -e" 
create database ncbi;
"
mysql -uroot -pqiaohan -e"
use ncbi;
create table html_file(
    htmlid int(8) NOT NULL,
    url varchar(255),
    father_htmlid int(8),
    deepth int(2),
    haschild bool,
    query varchar(255),
    subdb varchar(32),
    draw_time date,
    file_path varchar(63),
    file_name varchar(255),
    PRIMARY KEY(htmlid),
    KEY key_query(query)
);
"
