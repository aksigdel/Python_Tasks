from flask import Flask, jsonify, request
from exceptions import ValueDuplicate, ValueNotFound
import json

app = Flask(__name__)

def jprint(obj):
    data = json.dumps(obj, indent=4)
    print(data)

@app.route('/', methods=['GET'])
def home():
    if(request.method == 'GET'):
        data = "Flask API"
        return jsonify(
            {
                'data': data
            }
        )

#API to returns  name, address( street | suite | city), website based on user id.
@app.route('/users/<int:id>', methods=['GET'])
def user_details(id):
    with open('data.json', mode='r', encoding='utf-8') as file:
        users = json.load(file)
    jprint(users)
    for item in users:
        if item['id'] == id:
            return jsonify({'name': item['name'], 
                'address': {'street': item['address']['street'],
                            'suite':item['address']['suite'],
                            'city': item['address']['city']},
                'website': item['website']})
    return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })

# API to updates name and username to upper case based on user id and return updated data.
@app.route('/upper_users/<int:id>', methods = ['PUT','GET'])
def update_uppercase(id):
    try:
        with open('data.json', mode='r', encoding='utf-8') as file:
            users= json.load(file)
        jprint(users)
        upper_case = dict()
        for record in users:
            if record['id'] == id:
                record['name'] = record['name'].upper()
                record['username'] = record['username'].upper()
                upper_case=record
                break        
        if len(upper_case) == 0:
            raise ValueNotFound
        else:
            with open('data.json', mode='w', encoding='utf-8') as file:
                file.write(json.dumps(users, indent=4))
            jprint(users)
            return jsonify({
                'status': 200,
                'message': 'Uppercase update successful',
                'data': upper_case,
            })
    except ValueNotFound:
        return jsonify({
            'status': 404,
            'message': 'Record not found',
            'data': upper_case,
        })

# API to delete record and display response message based on user id.
@app.route('/delete_users/<int:id>', methods=['DELETE','GET'])
def delete_record(id):
    try:
        with open('data.json', mode='r',encoding='utf-8') as file:
            users=json.load(file)
        id_found = False
        user_left=[]
        del_record=dict()
        for record in users:
            if record['id'] == id:
                id_found = True
                del_record = record
                continue
            user_left.append(record)
        
        if not id_found:
            raise ValueNotFound
        else:
            with open('data.json', mode='w', encoding='utf-8') as file:
                file.write(json.dumps(user_left, indent=4))
            
            return jsonify({
                'status': 200,
                'message': 'Record deletion successful',
                'data': del_record,
            })

    except ValueNotFound:
        return jsonify({
            'status': 404,
            'message': 'Record not found',
            'data': {},
        })
       


#API to insert new record and display response message along with inserted data.
@app.route('/insert_user', methods=['POST','GET'])
def insert_user():
    #user_data=request.get_json()
    user_data = {
        "id": 15,
        "name": "Glenna Reichert",
        "username": "Delphine",
        "email": "Chaim_McDermott@dana.io",
        "address": {
            "street": "Dayna Park",
            "suite": "Suite 449",
            "city": "Bartholomebury",
            "zipcode": "76495-3109",
            "geo": {
                "lat": "24.6463",
                "lng": "-168.8889"
            }
        },
        "phone": "(775)976-6794 x41206",
        "website": "conrad.com",
        "company": {
            "name": "Yost and Sons",
            "catchPhrase": "Switchable contextually-based project",
            "bs": "aggregate real-time technologies"
        }
    }
    with open('data.json', mode='r',encoding='utf-8') as file:
            users=json.load(file)
    try:
        
        for record in users:
            if record['id'] == user_data['id']:
                raise ValueDuplicate
        users.append(user_data)
        with open('data.json', mode='w',encoding='utf-8') as wfile:
            wfile.write(json.dumps(users, indent=4))
       
        return jsonify({
            'status': 200,
            'message': 'Inserted successfully',
            'data': user_data,
        })
    except ValueDuplicate:
        return jsonify({
            'status': 400,
            'message': {'Invalid/duplicate input': id},
            'data': {},
        })    


#API to return  city count and status in JSON format.
@app.route('/city_count', methods=['GET'])
def city_count():
    try:
        with open('data.json',mode='r',encoding='utf-8') as file:
            loaded_data=json.load(file)
        cities=[data['address']['city'] for data in loaded_data]
        if len(cities) == 0:
            raise ValueNotFound
        dictionary = {}
        for item in cities:
            dictionary[item] = dictionary.get(item, 0) + 1
        return jsonify({
            'status': 200,
            'message': 'Count of each city in the data successful',
            'data': dictionary,
        })
    except ValueNotFound:
        return jsonify({
                'status': 404,
                'message': 'No records found',
                'data': {}
            })

if __name__=='__main__':
    app.run(debug=True)