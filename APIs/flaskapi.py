import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from exceptions import ValueDuplicate, ValueNotFound


app = Flask(__name__)
api = Api(app)

def json_print(obj):
    data = json.dumps(obj, indent=4)
    print(data)

class Userinfo(Resource):

#API to returns  name, address( street | suite | city), website based on user id.
    def get(self,id):
        with open('data.json', mode='r', encoding='utf-8') as file:
            users = json.load(file)
        json_print(users)
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
    def put(self,id):
        try:
            with open('employees.json', mode='r', encoding='utf-8') as file:
                users= json.load(file)
            json_print(users)
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
                json_print(users)
                return jsonify({
                    'status': 200,
                    'message': 'Uppercase update successful',
                    'data': upper_case
            })
        except ValueNotFound:
            return jsonify({
                'status': 404,
                'message': 'Record not found',
                'data': upper_case
            })

# API to delete record and display response message based on user id.
    def delete(self,id):
        try:
            with open('data.json', mode='r',encoding='utf-8') as file:
                users=json.load(file)
            json_print(users)
            user_left=[]
            del_record=dict()
            for record in users:
                if record['id'] != id:
                    del_record= record
                    user_left.append(record)
                else:
                    raise ValueNotFound
            with open('employees.json', mode='w', encoding='utf-8') as file:
                file.write(json.dumps(user_left, indent=4))
                json_print(users)
            return jsonify({
                    'status': 200,
                    'message': 'Uppercase update successful',
                    'data': user_left
            })
        except ValueNotFound:
            return jsonify({
                'status': 404,
                'message': 'Record not found',
                'data': user_left
            })


#API to insert new record and display response message along with inserted data.
    def post(self, id):
        user_data=request.get_json()
        """
        user_data = 
        {
        "id": 11,
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
        """
        with open('data.json', mode='r',encoding='utf-8') as file:
            users=json.load(file)
        try:
            for record in users:
                if record['id'] == user_data['id']:
                    raise ValueDuplicate
            users.append(user_data)
            with open('data.json', mode='w',encoding='utf-8') as wfile:
                wfile.write(json.dump(users, indent=4))
            
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


class Usercal(Resource):
    
#API to return  city count and status in JSON format.
    def city_count(self):
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


api.add_resource(Usercal, '/city_count')
api.add_resource(Userinfo, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

