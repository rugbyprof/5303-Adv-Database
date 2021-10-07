mongoimport -d dbName -c collectionName --type json --file fileName.json

db.restaurants.find({ "borough" : "Brooklyn"}).count()

{"createdAt": {"$gte": new Date("01/01/2019"),"$lt": new Date("01/01/2020")}}

https://docs.mongodb.com/mongodb-shell/crud/read/#std-label-mongosh-read

db.restaurants.find({"borough" : "Brooklyn","cuisine" : "American","grades.grade":"A","grades.score":{$gt:20}})

db.restaurants.find({"borough" : "Brooklyn","cuisine" : "American","grades.grade":"A","grades.score":{$gt:20}},{'grades.grade':1,'_id':0})

db.restaurants.aggregate([{$project: { count: { $size:"$grades" }}}])