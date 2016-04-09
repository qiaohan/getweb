mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e" 
create database ncbi;
"
mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi;
create table querylog(
    queryid int(32) NOT NULL,
    base_url varchar(255),
    query varchar(255),
    update_time varchar(63),
    PRIMARY KEY(queryid),
    KEY key_query(query),
    KEY key_uptime(update_time)
);
"
mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi;
create table listfile(
    htmlid int(32) NOT NULL,
    url varchar(255),
    queryid int(8),
    draw_time varchar(63),
    file_path varchar(63),
    file_name varchar(255),
    page_number int,
    total_page int,
    PRIMARY KEY(htmlid),
    KEY key_queryid(queryid)
);
"
mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi;
create table abstractfile(
    htmlid int(32) NOT NULL,
    url varchar(255),
    listhtmlid int(8),
    draw_time varchar(63),
    file_path varchar(63),
    file_name varchar(255),
    hasfulltext int(8),
    PRIMARY KEY(htmlid),
    KEY key_fulltext(hasfulltext),
    KEY key_listhtmlid(listhtmlid)
);
"
mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi;
create table articlefile(
    htmlid int(32) NOT NULL,
    url varchar(255),
    abstracthtmlid int(8),
    draw_time varchar(63),
    file_path varchar(63),
    file_name varchar(255),
    PRIMARY KEY(htmlid),
    KEY key_listhtmlid(abstracthtmlid)
);
"
mysql -uroot -pTwAxT7s1UjyoMzxnf7gQ -e"
use ncbi;
create table pdffile(
    pdfid int(32) NOT NULL,
    url varchar(255),
    articlehtmlid int(8),
    draw_time varchar(63),
    file_path varchar(63),
    file_name varchar(255),
    PRIMARY KEY(pdfid),
    KEY key_listhtmlid(articlehtmlid)
);
"
