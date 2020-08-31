import os
from elasticsearch import *
from jessica_local_spark_building import sqlContext

es=Elasticsearch([{'host':'localhost','port':9200}])

condition_folder = list(os.walk("data/condition"))[0]
control_folder = list(os.walk("data/control"))[0]

data_files = ["%s/%s"%(condition_folder[0],f) for f in condition_folder[2]] + ["%s/%s"%(control_folder[0],f) for f in control_folder[2]]

file_idx = 0
for f in data_files:
	df = sqlContext.read.format('csv').option('header', 'true').load(f)
	df.registerTempTable('data')
	df = sqlContext.sql(u"""
		SELECT '%s' AS file_name, * FROM data
		"""%(f))
	df.write.mode("Overwrite").json('temp_%d.json'%(file_idx))
	file_idx = file_idx+1

sqlContext.read.json('temp_*.json').registerTempTable('data')

sqlContext.sql(u"""
	SELECT *, 
	SPLIT(file_name, '/')[1] AS label,
	SPLIT(SPLIT(file_name, '/')[2], '.csv')[0] AS person_id
	FROM data
	ORDER BY  activity DESC
	""").write.mode("Overwrite").json('activity_data.json')

os.system(u"rm -r temp*.json")

sqlContext.read.json('activity_data.json').registerTempTable('activity_data')
sqlContext.read.format('csv').option('header', 'true').load('data/scores.csv').registerTempTable('scores')

sqlContext.sql(u"""
	SELECT STRING(HASH(activity_data.*)) AS document_id,
	INT(activity_data.activity) AS activity,
	CASE 
		WHEN activity_data.label = 'condition' 
		THEN INT(activity_data.activity)
		ELSE NULL
	END AS activity_depressed,
	CASE 
		WHEN activity_data.label = 'control' THEN INT(activity_data.activity)
		ELSE NULL
	END AS activity_nondepressed,
	activity_data.date,
	activity_data.file_name,
	CASE 
		WHEN activity_data.label = 'condition' THEN 'depressed'
		WHEN activity_data.label = 'control' THEN 'nondepressed'
		ELSE NULL
	END AS label,
	activity_data.person_id,
	CONCAT(SPLIT(activity_data.timestamp, ' ')[0], 'T',
	SPLIT(activity_data.timestamp, ' ')[1],
	'+00:00') AS timestamp,
	INT(SUBSTR(activity_data.timestamp, 12,2)) AS activity_hour,
	scores.number,
	INT(scores.days) AS days,
	CASE
		WHEN scores.gender = '1' THEN 'female' ELSE 'male'
	END AS gender,
	scores.age,
	CASE 
		WHEN scores.afftype = '1' THEN 'bipolar II'
		WHEN scores.afftype = '2' THEN 'unipolar depressive'
		WHEN scores.afftype = '3' THEN 'bipolar I'
		ELSE 'non-depressed'
	END AS afftype,
	CASE 
		WHEN scores.melanch = '1' THEN 'melancholia'
		WHEN scores.melanch = '2' THEN 'no melancholia'
		ELSE NULL
	END AS melanch,
	CASE 
		WHEN scores.inpatient = '1' THEN 'inpatient'
		WHEN scores.inpatient = '2' THEN 'outpatient'
		ELSE 'non-inpatient'
	END AS inpatient,
	scores.edu,
	CASE 
		WHEN scores.marriage = '1' THEN 'married or cohabiting'
		WHEN scores.marriage = '2' THEN 'single'
		ELSE  'n/a'
	END AS marriage,
	CASE 
		WHEN scores.work = '1' THEN 'working or studying'
		WHEN scores.work = '2' THEN 'unemployed/sick leave/pension'
		ELSE  'n/a'
	END AS work,
	INT(scores.madrs1) AS madrs1,
	INT(scores.madrs2) AS madrs2
	FROM activity_data
	LEFT JOIN scores
	ON scores.number = activity_data.person_id
	""").write.mode("Overwrite").json('activity_data_score.json')

df = sqlContext.read.json('activity_data_score.json')
df.registerTempTable('activity_data_score')

df1 = sqlContext.sql(u"""
	SELECT * FROM activity_data_score
	ORDER BY person_id ASC
	""")
data = df1.collect()

for i in data:
	try:
		r = i.asDict()
		es.index(index='activity_data_score',
		doc_type='activity',
		id=r['document_id'],
		body=r)
	except:
		pass
