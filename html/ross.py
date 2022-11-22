# import requests
import json


# r = requests.get('https://www.rossmann.pl/additionals/api/brands')
# brands=r.json()

# with open('brands.json', 'w') as f:
#     f.write(r.text)




# print(brands)

with open('brands.json', 'r') as f:
    brands = json.load(f)

keys_in_brands = brands['data'].keys()
print(keys_in_brands)

only_brands=[]

for x in keys_in_brands:
    w = brands['data'][x]['brands']
    for y in w:
        only_brands.append({'name': y['name'], 'id': y['id']})
    # only_brands.setdefault(w)
    # print(w['name'])
    # print(w['id'])

sorted_brands_by_id = sorted(only_brands, key=lambda k: k['id'])
for i in sorted_brands_by_id:
    print(i)
# for i in sorted(only_brands, key=lambda x: x.get('id')):
#     print(i)

with open ('brands_sorted.json', 'w') as f:
    json.dump(sorted_brands_by_id, f)