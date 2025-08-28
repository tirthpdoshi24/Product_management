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


result = execute_db("select pd.*,cd.* from product_details pd left join category_details cd on pd.category_id=cd.id")
print(result)
print(result.fetchall())
