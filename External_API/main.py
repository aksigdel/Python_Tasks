from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
from exceptions import ValueNotFound

app= Flask(__name__)
api= Api()

    
class Anime(Resource):
    
#get all present animes data    
    def getall(self):
        with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
        return f"<pre>{json.dumps(animes,indent = 4)}</pre>" 
    
#get anime data based on the anime id        
    def get(self, id):
        with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
        try:    
            for anime in animes:
                if anime['id']==id:
                    return jsonify({
                        'name': anime['alternativesTitles'],
                        'ranking':anime['ranking'],
                        'type': anime['type'],
                        'status':anime['status']
                    })
        except:
            return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })
#delete anime based on id
    def delete(slf, id):
        try:
            with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.dumps(file)
            ani_me=[]
            for anime in animes:
                if anime['id']!=id:
                    ani_me.append(anime)
                else:
                    continue
            with open('anime_example.json', mode='w', encoding='utf-8') as wfile:
                wfile.write(json.dumps(ani_me, indent = 4))
            return f"<pre>{json.dumps(ani_me,indent = 4)}</pre><pre>{'status':'record deleted'}</pre>"
        except:
            return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })

#update anime data based on id
    def update(self,id):
        data=request.get_json()
        try:
            with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.loads(file)
            animelst=()
            id_status= False
            for anime in animes:
                    if anime['id'] != data['id']:
                        animelst.append(anime)
                    else:
                        id_status=True
                        animelst.append(data)
            if not id_status:
                    raise ValueNotFound 
            with open('anime_example.json', mode='w', encoding='utf-8') as wfile:
                wfile.write(json.dumps(animelst, indent = 4))
            return f"<pre>{json.dumps(animelst,indent = 4)}</pre><pre>{'status':'record updated'}</pre>"
        except ValueNotFound:
            return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })
                          
#create anime data 
    def post(self):
        data=request.get_json() #according to the schema and id will be prev_data[-1]['id']+1
        try:
            with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.loads(file)
            animes.append(data)
            with open('anime_example.json', mode='w', encoding='utf-8') as wfile:
                wfile.write(json.dumps(animes,indent =4))
            return f"<pre>{json.dumps(animes,indent = 4)}</pre><pre>{'status':'record created'}</pre>"
        except:
            return jsonify({
                'status': 400,
                'message': 'Not created',
            })
            
api.add_resource(Anime, '/anime/<int:id>')
api.add_resource(Anime, '/anime')
    
if __name__ == '__main__':
    app.run(debug=True)