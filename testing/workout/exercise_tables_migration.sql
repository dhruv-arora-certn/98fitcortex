#Manage Cardio Floor Exercises
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

truncate table workout_cardiofloorexercise;
insert into workout_cardiofloorexercise select * from m1;
drop table m1;


#Manage Cardio Floor Time Based Exercises

create temporary table m1 like cardio_time_based;
insert into m1 select * from cardio_time_based;

update m1 set home = '1' where home = 'True';
update m1 set home = '0' where home = 'False';
update m1 set gym = '0' where gym = 'False';
update m1 set gym = '1' where gym = 'True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;

truncate table workout_cardiotimebasedexercise;
insert into workout_cardiotimebasedexercise select * from m1;
drop table m1;

#Manage Novice Core Strengthening Exercises
create temporary table m1 like novice_core_strengthining;
insert into m1 select * from novice_core_strengthining;

update m1 set home = '1' where home = 'True';
update m1 set home = '0' where home = 'False';
update m1 set gym = '0' where gym = 'False';
update m1 set gym = '1' where gym = 'True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set hold = '0' where hold = 'False';
update m1 set hold = '1' where hold = 'True';
update m1 set swing1 = '0' where swing1 = 'False';
update m1 set swing1 = '1' where swing1 = 'True';
update m1 set rotation = '0' where rotation = 'False';
update m1 set rotation = '1' where rotation = 'True';
update m1 set swing2 = '0' where swing2 = 'False';
update m1 set swing2 = '1' where swing2 = 'True';


alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;
alter table m1 modify swing1 tinyint;
alter table m1 modify hold tinyint;
alter table m1 modify rotation tinyint;
alter table m1 modify swing2 tinyint;

truncate table workout_novicecorestrengthiningexercise;
insert into workout_novicecorestrengthiningexercise select * from m1;
drop table m1;

#Manage Resistance Training Table Migration

create temporary table if not exists m1 as (select * from resistance_traning);

update m1 set home = '1' where home = 'True';
update m1 set home = '0' where home = 'False';
update m1 set gym = '0' where gym = 'False';
update m1 set gym = '1' where gym = 'True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set left_right = '1' where left_right = 'True';
update m1 set left_right = '0' where left_right = 'False';
update m1 set status = '0' where status != '1';

alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;
alter table m1 modify left_right tinyint;
alter table m1 modify status int;

truncate table workout_resistancetrainingexercise;
insert into workout_resistancetrainingexercise select * from m1;
drop table m1;


#Manage stretching Exercises
create temporary table if not exists m1 as (select * from stratching);

update m1 set home = '1' where home = 'True';
update m1 set home = '0' where home = 'False';
update m1 set gym = '0' where gym = 'False';
update m1 set gym = '1' where gym = 'True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set swing1 = '0' where swing1 = 'False';
update m1 set swing1 = '1' where swing1 = 'True';


alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;
alter table m1 modify swing1 tinyint;

truncate table workout_stretchingexercise;
insert into workout_stretchingexercise select * from m1;
drop table m1;

#Manage warmup mobility drill exercises

create temporary table if not exists m1 as (select * from warmup_cooldown_mobilitydrill);

update m1 set home = '1' where home = 'True';
update m1 set home = '0' where home = 'False';
update m1 set gym = '0' where gym = 'False';
update m1 set gym = '1' where gym = 'True';
update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set swing1 = '0' where swing1 = 'False';
update m1 set swing1 = '1' where swing1 = 'True';
update m1 set rotation = '0' where rotation = 'False';
update m1 set rotation = '1' where rotation = 'True';
update m1 set swing2 = '0' where swing2 = 'False';
update m1 set swing2 = '1' where swing2 = 'True';


alter table m1 modify machine_required tinyint;
alter table m1 modify home tinyint;
alter table m1 modify gym tinyint;
alter table m1 modify swing1 tinyint;
alter table m1 modify reps tinyint;
alter table m1 modify rotation tinyint;
alter table m1 modify swing2 tinyint;


truncate table workout_warmupcooldownmobilitydrillexercise;
insert into workout_warmupcooldownmobilitydrillexercise select * from m1;
drop table m1;


#Mangage Warm Up Time Based

create temporary table if not exists m1 as (select * from warmup_cooldown_timebased);

update m1 set machine_required = '0' where machine_required = 'False';
update m1 set machine_required = '1' where machine_required = 'True';
update m1 set machine_required = '1' where machine_required not in ('1','0');
update m1 set home = '1' where home = 'yes';
update m1 set home = '0' where home = 'no';
update m1 set gym = '0' where gym = 'no';
update m1 set gym = '1' where gym = 'yes';

alter table m1 modify machine_required tinyint;
alter table m1 modify total_time tinyint;

truncate table workout_warmupcooldowntimebasedexercise;
insert into workout_warmupcooldowntimebasedexercise select * from m1;
drop table m1;
