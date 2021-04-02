import json
import api1

products = []
parents = []
data = []


def find_ancestors(id, names=[]):
    """Recursive function to find ancestors
    :param id: product to search for its ancestor list.
    :param names: ancestor names.
    """
    if not id:
        return names

    for item in parents:
        if item['id'] == id:
            names.append(item['name'])
            return find_ancestors(item['parent_id'], names)


def read_prod_file():
    """Read file and generate new ids"""
    with open('product_groups.json', 'r') as f:
        global products
        products = json.load(f)
        api = api1.API1()

        for prod in products:
            # Create new id
            prod['new_id'] = api.create(prod).get('id')

            if prod['children_ids']:
                parents.append(prod)
    f.close()


def generate_data():
    """Generate products to save in file """
    for prod in products:
        if prod['parent_id']:
            parent = products[prod['parent_id']]
            parent_id = str(parent['new_id'])
        else:
            parent_id = None

        data.append({
            'id': str(prod['new_id']),
            'name': prod['name'],
            'parent_id': parent_id,
            'ancestors': find_ancestors(prod['parent_id'], [])
        })


def save_prods():
    """Save data in file"""
    f = open('new_prods_challenge1.json', 'w')
    json.dump(data, f)
    f.close()


if __name__ == "__main__":
    read_prod_file()
    generate_data()
    save_prods()
