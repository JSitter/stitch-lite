from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import requests
import os
import json

Base = declarative_base()

class Product(Base):
  __tablename__ = 'product'

  id = Column('id', Integer, primary_key=True)
  product_name = Column('product_name', Unicode, nullable=False)
  description = Column('description', Unicode, nullable=False)
  sku = Column('sku', String, unique=True)
  qty = Column('qty', Integer, nullable=False)

engine = create_engine(os.environ.get('CLEARDB_DATABASE_URL'), echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
product = Product()
product.product_name = "Earringsa"
product.description = "These are wonderful earrings with high quality metals"
product.sku = '10003003'
product.qty = 1000


session.add(product)
session.commit()
session.close()

app = Flask(__name__)

def vendAuth():
  redirect_uri = 'https://reddit.com'
  client_id = 12345
  state = ''

  authUrl = 'https://secure.vendhq.com/connect?response_type=code&client_id={}&redirect_uri={}&state={}'.format(redirect_uri, client_id, state)
  print(authUrl)

def shopifyAuth():
  api_key = os.environment.get('SHOPIFY_API_KEY')
  url = 'https://18d39847f5ac7a00f0c780a984e8716b:1c3a85695246e7824f383f3bf897d5dc@stitch-lightning.myshopify.com/admin/orders.json'

  headers = {
  'Authorization': 'Bearer 5OtjwgBqfIMt7vavCz66g_WtoCCB0hZ3t1lEFLVK',
  'Username':'18d39847f5ac7a00f0c780a984e8716b',
  'Password': '1c3a85695246e7824f383f3bf897d5dc'
  }

  response = requests.get(url, headers=headers, )

  data = response.text
  print(data)

  return data

@app.route('/')
def main():
  vendAuth()
  api_key = os.environ.get('SHOPIFY_API_KEY')
  urli = "https://stitch-lite.herokuapp.vendhq.com/api/products?page=1&page_size=200"

  url = "http://www.reddit.com"

  headers = {
    'Authorization': 'Bearer 5OtjwgBqfIMt7vavCz66g_WtoCCB0hZ3t1lEFLVK'
  }

  response = requests.get(url, headers=headers, )

  data = response.text
  print(data)

  return data

# https://domain_prefix.vendhq.com/api/products?page=23&page_size=200
@app.route('/api/products')
def vendReturn():
  return 'Hello There!'

@app.route('/api/sync', methods=['POST'])
def sync():
  return os.environ.get('SHOPIFY_API_KEY')

if __name__ == '__main__':
  app.run()