.mode csv
.import "Processed Data/Numerical Judgements.csv" numerical_judgements
.headers on

create table numerical_judgements_has_🥺
 as select * 
 from numerical_judgements
 where s_has_🥺 = 'True';

create table numerical_judgements_doesnt_have_🥺
  as select *
  from numerical_judgements
  where s_has_🥺 = 'False';

create table effect_of_🥺
  as select
  round(avg(has.j_expressive) - avg(doesnt.j_expressive), 2) as j_expr,
  round(avg(has.j_annoying) - avg(doesnt.j_annoying), 2) as j_anno,
  round(avg(has.j_friendly) - avg(doesnt.j_friendly), 2) as j_frnd,
  round(avg(has.j_cute) - avg(doesnt.j_cute), 2) as j_cute,
  round(avg(has.j_cisgender) - avg(doesnt.j_cisgender), 2) as j_cis,
  round(avg(has.j_feminine) - avg(doesnt.j_feminine), 2) as j_fem
  from 
  numerical_judgements_has_🥺 has, 
  numerical_judgements_doesnt_have_🥺 doesnt
  where has.s_name == doesnt.s_name;

.output "Processed Data/Effect of 🥺.csv"
select * from effect_of_🥺;

create table effect_of_🥺_where_r_transgender_and_r_woman
  as select
  round(avg(has.j_expressive) - avg(doesnt.j_expressive), 2) as j_expr,
  round(avg(has.j_annoying) - avg(doesnt.j_annoying), 2) as j_anno,
  round(avg(has.j_friendly) - avg(doesnt.j_friendly), 2) as j_frnd,
  round(avg(has.j_cute) - avg(doesnt.j_cute), 2) as j_cute,
  round(avg(has.j_cisgender) - avg(doesnt.j_cisgender), 2) as j_cis,
  round(avg(has.j_feminine) - avg(doesnt.j_feminine), 2) as j_fem
  from 
  numerical_judgements_has_🥺 has, 
  numerical_judgements_doesnt_have_🥺 doesnt
  where has.s_name == doesnt.s_name
  and has.r_transgender = 'True'
  and doesnt.r_transgender = 'True'
  and has.r_woman = 'True'
  and doesnt.r_woman = 'True';

.output "Processed Data/Effect of 🥺 on Trans Women.csv"
select * from effect_of_🥺_where_r_transgender_and_r_woman;

create table numerical_judgement_means
  as select 
  "s_name", "s_has_🥺",
  round(avg("j_expressive"), 2) as j_expr,
  round(avg("j_annoying"), 2) as j_anno,
  round(avg("j_friendly"), 2) as j_frnd,
  round(avg("j_cute"), 2) as j_cute,
  round(avg("j_cisgender"), 2) as j_cis,
  round(avg("j_feminine"), 2) as j_fem, 
  count(*)
  from numerical_judgements
  group by "s_name", "s_has_🥺";

.output "Processed Data/Numerical Judgement Means.csv"
select * from numerical_judgement_means;

create table opinion_means
  as select 
  r_man, r_woman,
  avg(r_🥺_opinion),
  count(*) as r_count
  from numerical_judgements
  group by r_man, r_woman;

.output "Processed Data/Opinion Means.csv"
select * from opinion_means;

.exit