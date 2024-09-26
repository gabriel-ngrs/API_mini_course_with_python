from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_maneger = LoginManager()
db = SQLAlchemy(app)
login_maneger.init_app(app)
login_maneger.login_view = 'login'
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable = True)

# Criando o modelo de como os produtos serão armazenados no banco de dados
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Coluna do ID, tipo inteiro. primary_key serve para ordenar e não repetir os IDs
    name = db.Column(db.String(120), nullable=False) # Coluna do nome, tipo string com limite de caracter, nao é opcional, entao = false
    price = db.Column(db.Float, nullable=False) # Coluna do preço, tipo float, nao é opcional, entao = false
    description = db.Column(db.Text, nullable=True) # Coluna da descrioção, tipo Text sem limite de caracter, é opcional, entao = True

@login_maneger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST/"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user:
        if data.get("password") == user.password:
           login_user(user)
           return jsonify({"message": 'Login successfully'}), 200
    return jsonify({"message": 'Unauthorized. Invalid credentials'}), 401
    
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": 'Logout successfully'}), 20

@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) # .get para indicarao py que quando nao tiver descrição ele coloca vazio
        db.session.add(product) # Adicionando o produto ao banco de dados
        db.session.commit() # Salvando o banco de dados
        return jsonify({"message": "Product added successfuly"}), 200
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id): 
    product = Product.query.get(product_id)
    if product != None: 
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404
        
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Product not found"})

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"})
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
    
    if 'price' in data:
        product.price = data['price']
    
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    return jsonify({"message": 'Product update successfully'})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        product_list.append(product_data)
    return jsonify(product_list)

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/') 
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
