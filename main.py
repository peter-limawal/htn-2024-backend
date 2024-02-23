from flask import Flask, request, jsonify
import json
import sqlite3
conn = sqlite3.connect(':memory:', check_same_thread=False)

app = Flask(__name__)
c = conn.cursor()

# Create hackers table
c.execute("""CREATE TABLE hackers (
            name text,
            company text,
            email text,
            phone text
            )""")
# Create skills table
c.execute("""CREATE TABLE skills(
            email text,
            skill text,
            rating integer
            )""")

def add_new_hacker(hacker):
    with conn:
        c.execute("INSERT INTO hackers VALUES (:name, :company, :email, :phone)", {'name': hacker["name"], 'company': hacker["company"], 'email': hacker["email"], 'phone': hacker["phone"]})
        for hacker_skill in hacker["skills"]:
            c.execute("INSERT INTO skills VALUES (:email, :skill, :rating)", {'email': hacker["email"], 'skill': hacker_skill["skill"], 'rating': hacker_skill["rating"]})


# Import json file into database
with open('HTN_2023_BE_Challenge_Data.json', 'r') as json_file:
    data = json.load(json_file)
    for item in data:
        add_new_hacker(item)

conn.commit()

@app.route("/")
def home():
    return "Home"

# All Users Endpoint
@app.route("/get/hackers/all", methods=['GET'])
def get_all_hackers():
    c.execute("SELECT * FROM hackers")
    hacker_list = c.fetchall()

    return_list = []
    for hacker in hacker_list:
        tmp = list(hacker)
        c.execute("SELECT skill, rating FROM skills WHERE email=:email", {'email': tmp[2]})
        tmp.append(c.fetchall())
        return_list.append(tmp)

    return jsonify(return_list), 200

# User Information Endpoint
@app.route("/get/hackers/<email>", methods=['GET'])
def get_user(email):
    c.execute("SELECT * FROM hackers WHERE email=:email", {'email': email})
    hacker = list(c.fetchall())
    c.execute("SELECT skill, rating FROM skills WHERE email=:email", {'email': hacker[0][2]})
    hacker.append(c.fetchall())
    return jsonify(hacker), 200

# Updating User Data Endpoint
# nvm it doesn't work
@app.route("/put/hackers/<email>", methods=['PUT'])
def update_user(email):
    name = request.args.get(name) 
    company = request.args.get(company)
    phone = request.args.get(phone)

    if name:
        c.execute("UPDATE hackers SET name=:name WHERE email=:email", {'name': name, 'email': email})
    if company:
        c.execute("UPDATE hackers SET company=:company WHERE email=:email", {'company': company, 'email': email})
    if phone:
        c.execute("UPDATE hackers SET phone=:phone WHERE email=:email", {'phone': phone, 'email': email})

    get_user(email)

# Skills Endpoints
@app.route("/get/skills/frequencies", methods=['GET'])
def get_skills():
    c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill")
    return jsonify(c.fetchall()), 200

@app.route("/get/skills", methods=['GET'])
def get_skills_filter():
    min_freq = int(request.args.get("min_frequency"))
    max_freq = int(request.args.get("max_frequency"))
    c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill HAVING COUNT(skill) BETWEEN :min_freq AND :max_freq", {'min_freq': min_freq, 'max_freq': max_freq})
    return jsonify(c.fetchall()), 200

if __name__ == "__main__":
    app.run(debug=True)

conn.close()