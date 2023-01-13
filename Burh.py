from flask import Flask, request, jsonify

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok"},
    {"id": 2, "name": "Australia", "capital": "Canberra"},
    {"id": 3, "name": "USA", "capital": "LA"},
]
def _find_next_id(id):
    data = [x for x in countries if x['id'] == id]
    return data

@app.route('/country/<int:id>', methods=["DELETE"])
def delete_country(id: int):

    data = _find_next_id(id)
    if not data:
        return {"error": "Country not found"}, 404
    else:
        countries.remove(data[0])
        return "Country deleted successfully", 200

#REST API
@app.route('/country', methods=["GET"])
def get_country():
    return jsonify(countries)

# GET -by ID
@app.route('/country/<id>', methods=["GET"])
def get_country_id(id):
    data = _find_next_id(id)
    return jsonify(data)

@app.route('/country', methods=["POST"])
def post_country():
    id = request.form.get('id')
    name = request.form.get('name')
    capital = request.form.get('capital')

    new_data = {
        "id": id,
        "name": name,
        "capital": capital,
        
    }

    if (_find_next_id(id)):
        return {"error": "Bad Request"}, id
    else:
        countries.append(new_data)
        return jsonify(countries)

@app.route('/put_country/<int:c_id>', methods=["PUT"])
def update_country(c_id):
    # id = request.form.get('id')
    global countries
    name = request.form.get('name')
    capital = request.form.get('capital')

    update_data = {
        "name" : name,
        "capital" : capital
    }


    # data = {x for x in countries if x["id"] !=id}
    # data.update(update_data)
    # update_data = countries
    # return jsonify(countries)

    for country in countries:
        if c_id == country.get("id"):
            country["name"] = str(name)
            country["capital"] = str(capital)
            return jsonify(countries)

    else:
        return "Error", 404

@app.route('/country/<id>', methods=["PATCH"])
def patch_country(id: int):
    country = _find_next_id(id)
    if country is None:
        return jsonify({'error':'Country not found!'}),404

    updated_country = json.loads(request.data)
    country.update(updated_country)
    return jsonify(countries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)