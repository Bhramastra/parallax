drop table if exists entries;
create table entries (
  nodeid integer primary key autoincrement,
  utilization float(3) not null,
  memory float(3) not null,
  ip integer not null,
  port integer not null,
  task text not null
);