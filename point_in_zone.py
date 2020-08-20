from geopy.geocoders import Nominatim
import json
from shapely.geometry import shape, Point
import pandas as pd 

adresses_fichier = pd.read_csv('adresses_test.csv',sep=";",header=None)
adresses_fichier

for i in adresses_fichier[0].to_list():
    #adresse = input("entez l'adresse à vérifier:")
    #adresse = "14-20 Avenue Emile Zola, 59146 Pecquencourt"
    #adresse = "turlutulkjfdqlkkmj"
    adresse = i

    # convert adress in coordonates 
    geolocator = Nominatim(user_agent="Projet_adresses_zones_prioritaires")
    location = geolocator.geocode(adresse)
    #print((location.latitude, location.longitude))
    try:
        location.latitude

        ######### part 2 -> polygones
        # load GeoJSON file containing sectors
        with open('quartiers-prioritaires-de-la-politique-de-la-ville-qpv.geojson') as f:
            js = json.load(f)


        # construct point based on lon/lat returned by geocoder
        point = Point(location.longitude,location.latitude)    
        #point = Point(3.197787,50.370284) 

        # check each polygon to see if it contains the point
        for feature in js['features']:
            try:
                polygon = shape(feature['geometry'])
                #print(polygon)
            except:
                pass    
            if polygon.contains(point):
                region = feature['properties']['nom_reg']
                departement = feature['properties']['nom_dep']
                nom_quarter = feature['properties']['nom_qp']
                commune = feature['properties']['commune_qp']
                code_qp =feature['properties']['code_qp']
                print(f'L\'adresse: "{adresse}" est dans le "Quartiers Prioritaires", {region},{departement},{nom_quarter}, {commune}, {code_qp} ' )
        
    except:
        print(f'L\'adresse suivante doit être vérifiée manuellement car le logiciel ne la trouve pas sur la carte :"{adresse}"')    
        pass

print('Les autres adresses ne sont pas dans des "Quartiers Prioritaires"')