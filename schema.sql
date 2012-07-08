drop table if exists entries;
create table entries (
	id integer primary key autoincrement, /*id is primary key*/
	title string not null, 
	text string not null
);

