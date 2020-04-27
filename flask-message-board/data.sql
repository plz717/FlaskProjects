-- drop table if exists user_table;

create table if not exists user_table (
	username text not null,
	password text not null
);
