# Hack the North 2024 Backend Challenge - Peter Limawal

### All Users Endpoint:
http://127.0.0.1:5000/get/hackers/all\
Returns a list of all user data from the database in a JSON format

### User Information Endpoint:
http://127.0.0.1:5000/get/hackers/\<email>\
Returns user data with email \<email> from the database in a JSON format  

### Skills Endpoints:
http://127.0.0.1:5000/get/skills/frequencies\
Returns number of users with each skill (frequency) in a JSON format

http://127.0.0.1:5000/get/skills?min_frequency=\<X>&max_frequency=\<Y>\
Query parameter filtering - Returns number of users with each skill (frequency) between minimum \<X> and maximum \<Y> in a JSON format