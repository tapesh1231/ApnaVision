from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/about_company')
def about_company():
    return render_template('about_company.html')

@main.route('/products')
def products():
    return render_template('products.html')