SELECT COUNT(d.battery_included) as "Bat included when required", ROUND(AVG(a.average_review_rating),2) as "product note"
FROM detail d, amazon a
WHERE d.battery_included = 'Yes' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan';

SELECT COUNT(d.battery_included) as "Bat not included when required", ROUND(AVG(a.average_review_rating),2) as "product note"
FROM detail d, amazon a
WHERE d.battery_included = 'No' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan';