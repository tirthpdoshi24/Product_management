import sqlite3

def execute_db(*args):
    # db = sqlite3.connect(":memory:")
    # cur = db.cursor()
    db = sqlite3.connect('file:cachedb?mode=memory&cache=shared')
    data = True
    try:
        try:
            with db:
                cur = db.cursor()
                # massage `args` as needed
                result = cur.execute(*args)
                print(result)
                return result
        except Exception as why:
            print(why)
            return False
        # args = list(args)
        # args[0] = args[0].replace("%s", "?").replace(" update "," `update` ")
        # args = tuple(args)
        # cur.execute(*args)
        # arg = args[0].split()[0].lower()
        if arg in ["update", "insert", "delete", "create"]: db.commit()
    except Exception as why:
        print(why)
        data = False
        db.rollback()
    db.commit()
    db.close()
    return data

#Create category details
query1 = """CREATE TABLE category_details (id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL)"""
execute_db(query1)

query2 = """CREATE TABLE product_details(id INTEGER PRIMARY KEY,title TEXT NOT NULL,description TEXT NOT NULL,price FLOAT NOT NULL,status
 INTEGER DEFAULT 1,category_id INTEGER NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (category_id) REFERENCES category_details(id))"""
execute_db(query2)

result = execute_db("select pd.*,cd.* from product_details pd left join category_details cd on pd.category_id=cd.id")
print(result)
print(result.fetchall())
