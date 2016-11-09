```
db.yelp.business.find({$or: [{"full_address":{$regex: '89117'}},{"full_address":{$regex: '89122'}}]})
```

```
db.yelp.business.find({"full_address":{$regex: 'Las Vegas'}}).count()
```
```
db.yelp.business.find({
   loc: {
        $geoWithin: { $center: [ [ -80.839186,35.226504] , .004 ] }
   }
})
```
```
# create an index for the following to speed up.

db.yelp.review.find({"business_id":"hB3kH0NgM5LkEWMnMMDnHw"}).count() 
#20
```

```
db.yelp.review.find({"business_id":"P1fJb2WQ1mXoiudj8UE44w","stars":5}).count() 
#25
```

```
db.yelp.user.aggregate(
   [
     {
       $project:
          {
            year: { $substr: [ "$yelping_since", 2, 2 ] }
          }
      }
   ]
)
```
