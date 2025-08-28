import sqlite3
import pandas as pd
import json
from celery import Celery
import random

celery_app = Celery(
    'my_app',
    broker='redis://localhost:6379/',  # Redis broker URL
    backend='redis://localhost:6379/'  # Redis result backend URL
)

db = sqlite3.connect('file:cachedb?mode=memory&cache=shared')

def create_category_call(category_name):
    response = {"status":500,"message":"Something went wrong"}
    try:
        query = f"insert into category_details values(NULL, '{category_name}');"
        with db:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
        response["status"] = 200
        response["message"] = "Category Created Successfully"
    except Exception as e:
        print(e)
    return response


def create_product_call(event):
    response = {"status": 500, "message": "Something went wrong"}
    try:
        product_name = event.get("product_name")
        product_description = event.get("product_description")
        price = event.get("price")
        category_id = event.get("category_id")
        query = f"insert into product_details (id, title, description, price, category_id) values(NULL, '{product_name}', '{product_description}', '{price}', '{category_id}');"
        with db:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
        response["status"] = 200
        response["message"] = "Product Created Successfully"
    except Exception as e:
        print(e)
    return response


def delete_product_call(event):
    response = {"status": 500, "message": "Something went wrong"}
    try:
        product_name = event.get("product_name")
        product_id = event.get("product_id")
        delete_query = f"delete from product_details where"
        if product_id:
            delete_query += f" id = {product_id}"
        elif product_name:
            delete_query += f" name = '{product_name}'"
        else:
            response["status"] = 402
            response["message"] = "Please provide product id or name to delete."
            return response

        with db:
            cursor = db.cursor()
            cursor.execute(delete_query)
            db.commit()
        response["status"] = 200
        response["message"] = "Product Deleted Successfully"

    except Exception as e:
        print(e)
    return response


def search_product_call(event):
    response = {"status": 500, "message": "Something went wrong", "result":[]}
    try:
        with db:
            cursor = db.cursor()
        product_name = event.get("product_name")
        category_name = event.get("category_name")
        price = event.get("price")
        product_description = event.get("product_description")

        search_query = f"select pd.*,cd.name from product_details pd left join category_details cd on pd.category_id=cd.id where status=1 and"
        if product_name:
            search_query += f" pd.title like '%{product_name}%'"
        elif category_name:
            search_query += f" cd.name like '%{category_name}%'"
        elif price:
            search_query += f" pd.price = {price}"
        elif product_description:
            search_query += f" pd.description like '%{product_description}%'"

        result = cursor.execute(search_query)
        db_results = result.fetchall()
        if len(db_results) > 0:
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(db_results, columns=column_names)
            result_data = df.to_dict(orient='records')
            response['result'] = result_data
            response["message"] = "Product Found Successfully"
        else:
            response['message'] = "Product Not Found"
        response["status"] = 200

    except Exception as e:
        print(e)
    return response

def update_product_call(event):
    response = {"status": 500, "message": "Something went wrong", "result": []}
    try:
        with db:
            cursor = db.cursor()
        update_mapping = event.get("update_mapping")
        where_mapping = event.get("where_mapping")
        update_query = f"update product_details set "
        length_of_mapping = len(update_mapping)
        length_of_where_mapping = len(where_mapping)
        i=1
        for key,value in update_mapping.items():
            update_query += f"{key} = '{value}'"
            if i<length_of_mapping:
                update_query += ","
                i+=1

        if where_mapping:
            update_query+= " where "
        j = 1
        for key, value in where_mapping.items():
            update_query += f"{key} = {value}"
            if i < length_of_where_mapping:
                update_query += " and "
                j += 1

        cursor.execute(update_query)
        db.commit()
        response["status"] = 200
        response["message"] = "Product Updated Successfully"

    except Exception as e:
        print(e)
    return response

def get_products_call():
    response = {"status": 500, "message": "Something went wrong", "result": []}
    try:
        with db:
            cursor = db.cursor()
        query = "select title from product_details where status=1"
        result = cursor.execute(query)
        db_results = result.fetchall()
        if len(db_results) > 0:
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(db_results, columns=column_names)
            result_data = df["title"].tolist()
            response['result'] = result_data

        response["status"] = 200
        response["message"] = "Products Found Successfully"
    except Exception as e:
        print(e)
    return response

@celery_app.task
def create_bulk_product_call(number):
    response = {"status": 500, "message": "Something went wrong"}
    try:
        for i in range(number):
            product_name = f"product {i}"
            product_description = f"product description {i}"
            price = f"{random.randint(1, 100)}"
            category_id=1

            query = f"insert into product_details (id, title, description, price, category_id) values(NULL, '{product_name}', '{product_description}', '{price}', '{category_id}');"
            with db:
                cursor = db.cursor()
                cursor.execute(query)
                db.commit()
        response["status"] = 200
        response["message"] = "Product Created Successfully"
    except Exception as e:
        print(e)
    return response