drop table if exists post;
drop table if exists user;

create table user (
    id integer primary key autoincrement,
    username TEXT UNIQUE not null,
    password TEXT not null
);

create table post (
    id integer primary key autoincrement,
    author_id integer not null,
    created timestamp not null default current_timestamp,
    title TEXT not null,
    body TEXT not null,
    FOREIGN key (author_id) references user (id)
);