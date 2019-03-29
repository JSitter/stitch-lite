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

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
print('hello')
product = Product()
product.product_name = "Earringsa"
product.description = "These are wonderful earrings with high quality metals"
product.sku = '10003003'
product.qty = 1000

session.add(product)
session.commit()
session.close()

app = Flask(__name__)

@app.route('/')
def main():
  api_key = os.environ.get('SHOPIFY_API_KEY')
  url = "https://stitch-lite.herokuapp.com.vendhq.com/api/2.0/inventory"

  headers = {'accept': 'application/json'}

  response = requests.get(url, headers=headers)

  data = response.text
  print(data)

  return data

@app.route('/api/sync', methods=['POST'])
def sync():
  return os.environ.get('SHOPIFY_API_KEY')

if __name__ == '__main__':
  app.run()