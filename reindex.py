import datetime

stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
now = stamp

ind = {
"index_name", "index_name2"
}

print "###############"
print "#Backup to S3"
print "###############"
for i in ind:	
	print "curl -X PUT \"localhost:9200/_snapshot/my_s3_repository/{}_back_{}?wait_for_completion=true\" -H 'Content-Type: application/json' -d' {{ \"indices\" : \"{}\" }}'".format(i,now,i)


print "###############"
print "#Reindex"
print "###############"
for i in ind:
	print "curl -X POST \"localhost:9200/_reindex\" -H 'Content-Type: application/json' -d '{{ \"source\" : {{ \"index\": \"{}\"  }},  \"dest\": {{ \"index\": \"{}_reindex\" }} }}'".format(i,i)


print "###############"
print "#Delete old index"
print "###############"
for i in ind:
	print "curl -X DELETE \"localhost:9200/{}\"".format(i)


print "###############"
print "#Add alias"
print "###############"

for i in ind:
	print "curl -X POST \"localhost:9200/_aliases\" -H 'Content-Type: application/json' -d'{{    \"actions\" : [ {{ \"add\" : {{ \"index\" : \"{}_reindex\", \"alias\" : \"{}\" }} }}] }}'".format(i,i)


print "###############"
print "#Remove alias"
print "###############"

for i in ind:
	print "curl -X POST \"localhost:9200/_aliases\" -H 'Content-Type: application/json' -d'{{    \"actions\" : [ {{ \"remove\" : {{ \"index\" : \"{}_reindex\", \"alias\" : \"{}\" }} }}] }}'".format(i,i)


print "###############"
print "#Restore originals"
print "###############"

for i in ind:
	print "curl -X POST \"localhost:9200/_snapshot/my_s3_repository/{}_back_{}/_restore?wait_for_completion=true\"".format(i, now)

print "###############"
print "#Delete reindexed indexes"
print "###############"
for i in ind:
	print "curl -X DELETE \"localhost:9200/{}_reindex\"".format(i)	