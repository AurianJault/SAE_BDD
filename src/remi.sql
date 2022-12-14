-- Better note if battery is included when required
SELECT ROUND(AVG(a.average_review_rating),2) as "avg product note NoYes", (SELECT ROUND(AVG(a.average_review_rating),2) as "avg product note NoNo"
FROM detail d, amazon a
WHERE d.battery_included = 'No' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan')
FROM detail d, amazon a
WHERE d.battery_included = 'Yes' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan';

/*
SELECT ROUND(avg(a.average_review_rating),2) as "note where info BAD", (SELECT ROUND(avg(a.average_review_rating),2) as "note where info GOOD"
FROM detail d, amazon a
WHERE d.weight!='NaN' and d.dimension!='NaN' and d.recommended_age!='NaN' and d.uniq_id=a.uniq_id and a.average_review_rating!='NaN')
FROM detail d, amazon a
WHERE d.weight='NaN' and d.dimension='NaN' and d.assembly='NaN' and d.recommended_age='NaN' and d.uniq_id=a.uniq_id;

SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm ,count(launch_date) count 
from detail
where launch_date is not null
group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
having EXTRACT(YEAR from launch_date) = '2015'
order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
*/