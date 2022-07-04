-- From the two most commonly appearing regions, which is the latest datasource?
select 
	count(1) as qtt, 
	region,
	(select datasource from trips_csv tc where tc.datetime = max(t.datetime))as last_datasource
from trips_csv t 
group by region
order by qtt desc
limit 2;
-- Prague has the cheap_mobile here, if it counts

-- What regions has the "cheap_mobile" datasource appeared in?

select distinct
	region 
from trips_csv t 
where datasource = 'cheap_mobile';