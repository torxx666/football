# football

## install 
pip install -r requirements.txt
fill the config.py file with user /  pass credentials

for starting all service ( client, db ) run :
```
docker-compose up
```

## Part1 
from a browser or curl : 
http://0.0.0.0:8000/get_users?user_ids=14727959,2152691378,2445627020&skip=1&limit=1
- skip and limit are not mendatory

## Part2 
```
python3 scripts/etl.py
```
I start working on a pyspark parallelized version




