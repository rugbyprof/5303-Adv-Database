#!/bin/sh


curl -X GET http://$1:5000/zip/zips=89117,89122:start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/city/city="las vegas":start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/closest/lon=-80.839186:lat=35.226504:start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/reviews/id=hB3kH0NgM5LkEWMnMMDnHw:start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/stars/id=hB3kH0NgM5LkEWMnMMDnHw:num_stars=5:start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/yelping/min_years=5:start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/most_likes/start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/review_count/ >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/elite/start=0:limit=20 >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/elite/start=0:limit=1:sorted=reverse >> output.txt

echo "\n" >> output.txt

curl -X GET http://$1:5000/avg_elite/ >> output.txt
