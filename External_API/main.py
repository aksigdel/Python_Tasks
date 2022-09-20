from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
from exceptions import ValueNotFound, ValueDuplicate

app= Flask(__name__)
api= Api()

#get all present animes data    
#    def getall(self):
#        with open('anime_example.json', mode='r', encoding='utf-8') as file:
#                animes=json.load(file)
#       return f"<pre>{json.dumps(animes,indent = 4)}</pre>" 
    
#get anime data based on the anime id       
@app.route('/animes_record/<int:id>', methods=['GET'])
def load_anime(id):
        with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
        try:    
            for anime in animes:
                if anime['_id']==id:
                    return jsonify({
                        'name': anime['alternativeTitles'][0],
                        'ranking':anime['ranking'],
                        'type': anime['type'],
                        'status':anime['status']
                    })
        except FileNotFoundError:
            return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })
            
#delete anime based on id
@app.route('/anime_delete/<int:id>', methods=['DELETE', 'GET'])
def delete_anime(id):
    try:
        with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
        ani_me=[]
        id_found = False
        del_record=dict()
        for record in animes:
            if record['_id'] == id:
                id_found = True
                del_record = record
                continue
            ani_me.append(record)
        
        if not id_found:
            raise ValueNotFound
        else:
            with open('anime_example.json', mode='w', encoding='utf-8') as wfile:
                wfile.write(json.dumps(ani_me, indent=4))
            
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

#update anime data based on id
@app.route('/anime_update/<int:id>', methods=['PUT'])
def update_anime(id):
        #data=request.get_json()
        data =     {
        "_id": 1365,
        "alternativeTitles": [
            "Meitantei Conan: Baker Street no Bourei",
            "\u540d\u63a2\u5075\u30b3\u30ca\u30f3\u3000\u30d9\u30a4\u30ab\u30fc\u8857(\u30b9\u30c8\u30ea\u30fc\u30c8)\u306e\u4ea1\u970a",
            "Case Closed: The Phantom of Baker Street",
            "Detektiv Conan Film 6: Das Phantom der Baker Street",
            "Detective Conan Pel\u00edcula 6: El fantasma de Baker Street",
            "Detektiv Conan Film 6: Le Fant\u00f4me de Baker Street"
        ],
        "genres": [
            "Adventure",
            "Mystery",
            "childish",
            "ddetective"
        ],
        "ranking": 236,
        "type": "Movie",
        "status": "Finished Airing",
        "synopsis": "Noah's Ark\u2014the latest in VR technology and a milestone of human innovation\u2014is set for a showcase to Japan's privileged children. They have the honour of beginning a new revolution in gaming; however, their carefree fun is cut short when a company employee is found murdered, with his dying message pointing to a clue hidden within the Ark.\n\nAlong with the Detective Boys and Ran Mouri, Conan Edogawa enters Noah's Ark to solve this mystery and ensure the perpetrator is caught. But once they're inside the Ark, it takes on a mind of its own, imprisoning them and the children within its worlds. To escape and bring the murderer to justice, Conan and company must navigate a simulated 19th century London and track down the infamous Jack the Ripper\u2014with the lives of 50 innocent children depending on them.\n\n[Written by MAL Rewrite]"
    }
        try:
            with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
            animelst=[]
            id_status= False
            for anime in animes:
                    if anime['_id'] != data['_id']:
                        animelst.append(anime)
                    else:
                        id_status=True
                        animelst.append(data)
            if not id_status:
                    raise ValueNotFound 
            with open('anime_example.json', mode='w', encoding='utf-8') as wfile:
                wfile.write(json.dumps(animelst, indent = 4))
            return jsonify({
                'status': 200,
                'data': data,
                'message': 'Update successful'
            })
        except ValueNotFound:
            return jsonify({
                'status': 404,
                'data': id,
                'message': 'No record found',
            })
                          
#create anime data 
@app.route('/insert', methods=['POST'])
def create_anime():
    #data=request.get_json() #according to the schema and id will be prev_data[-1]['id']+1
    data= {
        "_id": 44876,
        "alternativeTitles": [
            "Tensura 2",
            "\u8ee2\u751f\u3057\u305f\u3089\u30b9\u30e9\u30a4\u30e0\u3060\u3063\u305f\u4ef6",
            "That Time I Got Reincarnated as a Slime Season 2 Part 2",
            "Meine Wiedergeburt als Schleim in einer anderen Welt Staffel 2 Teil 2",
            "That Time I Got Reincarnated as a Slime Temporada 2 Parte 2",
            "Moi",
            "Quand Je Me R\u00e9incarne en Slime Saison 2 Partie 2"
        ],
        "genres": [
            "Action",
            "Adventure",
            "Comedy",
            "Fantasy"
        ],
        "ranking": 216,
        "type": "TV",
        "status": "Finished Airing",
        "synopsis": "The nation of Tempest is in a festive mood after successfully overcoming the surprise attack from the Falmuth Army and the Western Holy Church. Beyond the festivities lies a meeting between Tempest and its allies to decide the future of the Nation of Monsters. The aftermath of the Falmuth invasion, Milim Nava's suspicious behavior, and the disappearance of Demon Lord Carrion\u2014the problems seem to keep on piling up.\n\nRimuru Tempest, now awakened as a \"True Demon Lord,\" decides to go on the offensive against Clayman. With the fully revived \"Storm Dragon\" Veldora, \"Ultimate Skill\" Raphael, and other powerful comrades, the ruler of the Tempest is confident in taking down his enemies one by one until he can face the man pulling the strings.\n\n[Written by MAL Rewrite]"
        }
    try:
        with open('anime_example.json', mode='r', encoding='utf-8') as file:
                animes=json.load(file)
        animes.append(data)
        with open('anime_example.json', mode = 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(animes, indent=4))
        return jsonify({
            'status': 200,
            'message': 'anime creation successful',
            'data': data,
        })
    
    except ValueDuplicate:
        return jsonify({
            'status': 400,
            'message': 'duplicate id no creation',
            'data': {},
        })
            
if __name__ == '__main__':
    app.run(debug=True)