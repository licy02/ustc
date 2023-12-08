import csv
import json

csv_file=open('生命科学与医学部_现任领导.csv','r',encoding='UTF-8')
json_file=open('生命科学与医学部_现任领导.json','w',encoding='UTF-8')

fieldnames=('name','content')

reader=csv.DictReader(csv_file,fieldnames)
out=json.dumps([row for row in reader],ensure_ascii=False, indent=4)

json_file.write(out)