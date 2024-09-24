from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Criando o modelo de como os produtos serão armazenados no banco de dados
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Coluna do ID, tipo inteiro. primary_key serve para ordenar e não repetir os IDs
    name = db.Column(db.String(120), nullable=False) # Coluna do nome, tipo string com limite de caracter, nao é opcional, entao = false
    price = db.Column(db.Float, nullable=False) # Coluna do preço, tipo float, nao é opcional, entao = false
    description = db.Column(db.Text, nullable=True) # Coluna da descrioção, tipo Text sem limite de caracter, é opcional, entao = True


@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) # .get para indicarao py que quando nao tiver descrição ele coloca vazio
        db.session.add(product) # Adicionando o produto ao banco de dados
        db.session.commit() # Salvando o banco de dados
        return jsonify({"message": "Product added successfuly"}), 200
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id): 
    product = Product.query.get(product_id)
    if product != None: 
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfuly"}), 200
    return jsonify({"message": "Product not found"}), 404
        
    

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/') 
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
