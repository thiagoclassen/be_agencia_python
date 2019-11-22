from json import JSONEncoder
import json
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

global vagaId
global curriculoId
global vagas
global curriculos

vagaId = 0
curriculoId = 0

vagas = []
curriculos = []


class Vaga:
    def __init__(self, form):
        global vagaId
        vagaId += 1
        self.id = vagaId
        self.empresa = form["empresa"]
        self.contato = form["contato"]
        self.area = form["area"]
        self.cargaHoraria = form["cargaHoraria"]
        self.salario = form["salario"]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class Curriculo:
    def __init__(self, form):
        global curriculoId
        curriculoId += 1
        self.id = curriculoId
        self.nome = form["nome"]
        self.contato = form["contato"]
        self.area = form["area"]
        self.cargaHoraria = form["cargaHoraria"]
        self.salario = form["salario"]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class VagaEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Vaga):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)


class CurriculoEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Curriculo):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)

# EndPoint generico de vagas
@app.route('/vagas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def vagasEnd():
    global vagas
    if request.method == 'POST':
        json_data = request.get_json(force=True) 
        vaga = Vaga(json_data)
        vagas.append(vaga)
        return VagaEncoder().encode(vaga), 200
    elif request.method == 'PUT':
        json_data = request.get_json(force=True) 
        vaga = Vaga(json_data)
        for idx, obj in enumerate(vagas):
            if obj.id == int(request.form["id"], 10):
                vagas[idx]["empresa"] = request.form["empresa"]
                vagas[idx]["contato"] = request.form["contato"]
                vagas[idx]["area"] = request.form["area"]
                vagas[idx]["cargaHoraria"] = request.form["cargaHoraria"]
                vagas[idx]["salario"] = request.form["salario"]
        return 'ok', 200
    elif request.method == 'DELETE':
        for obj in vagas:
            if obj.id == int(request.form["id"], 10):
                vagas.remove(obj)
        return VagaEncoder().encode(obj), 200

    return VagaEncoder().encode(vagas), 200

# EndPoint para vaga especifica por Id
@app.route('/vaga/<string:id>')
def vagaEnd(id):
    global vagas
    for obj in vagas:
        if obj.id == int(id, 10):
            return VagaEncoder().encode(obj), 200
    return 'Not Found', 404

# EndPoint generico de curriculos
@app.route('/curriculos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def curriculossEnd():
    global curriculos
    if request.method == 'POST':
        json_data = request.get_json(force=True) 
        curriculo = Curriculo(json_data)
        curriculos.append(curriculo)
        return CurriculoEncoder().encode(curriculo), 200
    elif request.method == 'PUT':
        for idx, obj in enumerate(curriculos):
            if obj.id == int(request.form["id"], 10):
                curriculos[idx]["nome"] = request.form["nome"]
                curriculos[idx]["contato"] = request.form["contato"]
                curriculos[idx]["area"] = request.form["area"]
                curriculos[idx]["cargaHoraria"] = request.form["cargaHoraria"]
                curriculos[idx]["salario"] = request.form["salario"]
        return 'ok', 200
    elif request.method == 'DELETE':
        for obj in curriculos:
            if obj.id == int(request.form["id"], 10):
                curriculos.remove(obj)
        return CurriculoEncoder().encode(obj), 200

    return CurriculoEncoder().encode(curriculos), 200

# EndPoint para curriculo especifico por Id
@app.route('/curriculo/<string:id>')
def curriculoEnd(id):
    global curriculos
    for obj in curriculos:
        if obj.id == int(id, 10):
            return CurriculoEncoder().encode(obj), 200
    return 'Not Found', 404


if __name__ == '__main__':
    app.run(debug=True)
