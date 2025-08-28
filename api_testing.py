import requests
import json

def category_creation():
  url = "http://127.0.0.1:8000/create_category"

  payload = json.dumps({
    "category_name": "ABC"
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


def product_creation():

  url = "http://127.0.0.1:8000/create_product"

  payload = json.dumps({
    "product_name": "JJJ",
    "product_description": "ABC Luxury Bag",
    "price": 250.5,
    "category_id": 1
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)

def product_deletion():
  url = "http://127.0.0.1:8000/delete_product"

  payload = json.dumps({
    "product_name": "JJJ",
    "product_id": 1
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


def search_product():

  url = "http://127.0.0.1:8000/search_product"

  payload = json.dumps({
    "product_name": "JJJ"
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)

def product_update():


  url = "http://127.0.0.1:8000/update_product"

  payload = json.dumps({
    "update_mapping": {
      "title": "JJT"
    },
    "where_mapping": {
      "id": 1
    }
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


def get_product_list():

  url = "http://127.0.0.1:8000/get_products"

  payload = {}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  print(response.text)


# category_creation()
# product_creation()
# product_deletion()
# search_product()
# product_update()
# get_product_list()