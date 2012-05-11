db.sf_crime.find({}).forEach(function(doc) { doc.loc = [parseFloat(doc.x), parseFloat(doc.y)]; db.sf_crime.save(doc) });
db.sf_crime.ensureIndex( { loc : "2d" } )

half_mile_degrees = 0.00000034616863;
db.sf_crime.find( { loc : { $near : [-122.413886, 37.775593] , $maxDistance : 0.0013704816105871763 } } )

var cursor = db.nearby_crimes.find()
while (cursor.hasNext()) printjson(cursor.next());
