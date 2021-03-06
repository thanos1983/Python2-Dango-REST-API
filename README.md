# Python2-Dango-REST-API
Minor API test implementation using Django REST Framework

Sample of useful commands to test the functionality of the API with curl.

GET

curl http://127.0.0.1:8000/snippets/

or 

curl http://127.0.0.1:8000/snippets/ | jq '.' # if installed jq

or

curl http://127.0.0.1:8000/snippets/ | json_pp

or

curl http://127.0.0.1:8000/keywords/ | jq '.' # keywords file(s)

or

curl http://127.0.0.1:8000/upload/ | jq '.' # uploaded file(s)

or 

curl -u admin:password123 http://127.0.0.1:8000/keywords/1/ | jq '.' # GET specific input from user admin 

DELETE

curl -i -X DELETE -u admin:password123 http://127.0.0.1:8000/snippets/1/

or

curl -i -X DELETE -u admin:password123 http://127.0.0.1:8000/keywords/1/

POST

curl -i -X POST -H "Content-Type:application/json" -u admin:password123 http://localhost:8000/snippets/ -d '{
    "title": "Test Title",
    "code": "print(Test POST Request)",
    "linenos": false,
    "language": "python",
    "character": "\u00A9",
    "style": "emacs"
}'

POST FILE

curl -u admin:password123 -H "Content-Type: multipart/form-data" -H "Accept: application/json" -H "Expect:" -F file=@sample.txt -X POST http://127.0.0.1:8000/upload/ | jq '.'

curl -u admin:password123 -H "Content-Type: multipart/form-data" -H "Accept: application/json" -H "Expect:" -F file=@keywords.txt -X POST http://127.0.0.1:8000/keywords/ | jq '.'