--Manage Cardio Floor Exercises
create temporary table m1 like cardio_floor;
insert into m1 select * from cardio_floor;

update m1 set home = '1' where home='True';
update m1 set home = '0' where home='False';
update m1 set gym = '0' where gym='False';
update m1 set gym = '1' where gym='True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set swing1='1' where swing1 = 'True';
update m1 set swing1='0' where swing1 = 'False';
alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;

insert into workout_cardiofloorexercise select * from m1;


