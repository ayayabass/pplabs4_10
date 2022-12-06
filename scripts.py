from datetime import datetime, date
from db import *
import jwt
session = Session()

# curl -X "POST" -H "Content-Type: application/json" -H "token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6IkV1Z2VuZSJ9.yWGjf6ZXxNdG2Nx_rmxKCIW_ZIW3P5M00VyktqPja0k" -d '{
#         "name" : "AI full course",
#         "year" : "2004-05-05",
#         "language" : "English",
#         "id_genre" : 1,
#         "author_id" : 1,
#         "status": "available",
#         "price": 1000,
#         "description" : "A book",
#         "photo_url" : "http://aaa"
# }' 'http://127.0.0.1:5000/book'

# curl -X "POST" -H "Content-Type: application/json" -H "token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkV1Z2VuZSIsInRva2VuIjoicGFzc3dvcmQifQ.PNIFc6DiRTlloJi91twGWnqThQ1Y_O5Z17MooPW25MA" -d '{
#         "name" : "C++ full course",
#         "year" : "2004-05-05",
#         "language" : "English",
#         "id_genre" : 1,
#         "author_id" : 1,
#         "status": "available",
#         "price": 500,
#         "description" : "A book",
#         "photo_url" : "http://bbb"
# }' 'http://127.0.0.1:5000/book'

# curl 'http://127.0.0.1:5000/books

# curl -X "PUT" -H "Content-Type: application/json" \
# -d '{
#     "language": "Ukrainian"
# }' 'http://127.0.0.1:5000/book/1'

# curl 'http://127.0.0.1:5000/books

# curl -X "DELETE" "http://127.0.0.1:5000/book/1"

# curl -X "DELETE" "http://127.0.0.1:5000/book/2"

# curl 'http://127.0.0.1:5000/books


# curl -X "POST" -H "Content-Type: application/json" -d '{
#         "username" = "Eugene",
#         "token" = "password"
# }' 'http://127.0.0.1:5000/Admin'

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbl9pZCI6IjEiLCJ1c2VybmFtZSI6IkV1Z2VuZSIsInRva2VuIjoicGFzc3dvcmQifQ.4IPMznjN9kP-cYhaJx-JcP4UHMJIztomdtsyvilR60A
# secret_key = 'ca9498317b9cd8654b62666a368e0500a8f6a1161093f19bb2edfc5642e474b8'
# p = {
#     "admin_id" : "1",
#     "username" : "Eugene",
#     "token" : "password"
# }
# data = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbl9pZCI6IjEiLCJ1c2VybmFtZSI6IkV1Z2VuZSIsInRva2VuIjoicGFzc3dvcmQifQ.4IPMznjN9kP-cYhaJx-JcP4UHMJIztomdtsyvilR60A', secret_key)
# print(data)

# curl 'http://127.0.0.1:5000/api/v1/books?author_id=1'

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6IkV1Z2VuZSJ9.yWGjf6ZXxNdG2Nx_rmxKCIW_ZIW3P5M00VyktqPja0k