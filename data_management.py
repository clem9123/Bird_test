import json

## Ouvrir le fichier JSON
#with open('data/birds.json', 'r', encoding='utf-8') as file:
#    data = json.load(file)
#
## Changer le nom de la clé "abondance" en "liste" et mettre sous forme de liste ce qu'il y a dans la clé
#for oiseau in data['oiseaux']:
#    if 'abondance' in oiseau:
#        oiseau['liste'] = [oiseau.pop('abondance')]
#
## Supprimer la clé "type" de chaque oiseau
#for oiseau in data['oiseaux']:
#    if 'type' in oiseau:
#        del oiseau['type']
#
## Supprimer "non commun" de la clé "liste" et ajouter "rapace" pour "Balbuzard pêcheur"
#for oiseau in data['oiseaux']:
#    if 'non commun' in oiseau['liste']:
#        oiseau['liste'].remove('non commun')
#    if oiseau['nom'] == "Balbuzard pêcheur":
#        oiseau['liste'].append('rapace')
#
## Enregistrer les modifications dans le fichier JSON
#with open('data/birds.json', 'w', encoding='utf-8') as file:
#    json.dump(data, file, ensure_ascii=False, indent=4)

with open('data/birds.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
        
# Récupérer toutes les listes uniques
listes = set()
for oiseau in data['oiseaux']:
    listes.update(oiseau['liste'])

print(listes)