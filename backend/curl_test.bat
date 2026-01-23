  curl -X POST http://localhost:9998/recipe/share -H "Content-Type: application/json" -H "Authorization: Bearer 6khXY1MyJHEDKpFmsRcFTuJ4V9i-v7ljGBN6QmkdtDE" -d '{"title":"Test recipe","url":"from terminal"}'



# Create
curl -X POST http://localhost:9998/recipe -H "Content-Type: application/json" -d '{"title":"Pasta","description":"Simple","ingredients":"pasta, salt","instructions":"Boilwater"}'

# List
curl http://localhost:9998/recipe

# Get by id (replace 1)
curl http://localhost:9998/recipe/1

# Update (replace 1)
curl -X PUT http://localhost:9998/recipe/1 \
-H "Content-Type: application/json" \
-d '{"description":"Simple and fast","instructions":"Boil water, cook pasta"}'

# Delete (replace 1)
curl -X DELETE http://localhost:9998/recipe/1