from flask import Flask
from flask import jsonify
from flask import request
import json
import sqlite3

app = Flask(__name__)

def generate_google_drive_id():
    """
    get google_drive_id for a new user
    :return:
    """
    wdict = {
        "available": 1
    }
    result = get_from_db("google_drive_ids", wdict, ["id"])
    if result:
        google_drive_id = result[0][0].strip()
        wdict = {
            "id" : google_drive_id
        }
        values_dict = {
            "available": 0
        }
        update_db("google_drive_ids", wdict, values_dict)
        return google_drive_id
    else:
        return ""



def get_google_drive_id(gmailid):
    """
    get google_drive_id for an existing user
    :param gmailid:
    """
    wdict = {
        "gmailid": gmailid
    }
    google_drive_id = get_from_db("uuids", wdict,["google_drive_id"])[0][0].strip()
    return google_drive_id


def get_db_connection():
    conn = sqlite3.connect('kubrik.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_into_db(table_name: str, values: list):
    db_conn = get_db_connection()
    with db_conn:
        for attempt in range(3):
            try:
                db_conn = get_db_connection()
                query = "INSERT INTO " + table_name + " VALUES ("
                v_list = []
                for v in values:
                    if isinstance(v, int):
                        v_list.append("%d" % (v))
                    else:
                        # enclose string in quotations
                        v_list.append("'%s'" % (v))
                query += " , ".join(v_list)
                query += ");"
                print(query)
                db_conn.execute(query)
                print("Commiting transaction")
                db_conn.commit()
                db_conn.close()
                return
            except Exception as e:
                print(e)
                if attempt == 2:
                    raise e
                continue


def update_db(table_name: str, wdict: dict, values_dict):
    db_conn = get_db_connection()
    for attempt in range(3):
        try:
            db_conn = get_db_connection()
            query = "UPDATE " + table_name + " SET "
            set_l = []
            for k, v in values_dict.items():
                op = "="
                value = v
                if isinstance(v, int):
                    set_l.append("%s %s %d" % (k, op, value))
                else:
                    # enclose string in quotations
                    set_l.append("%s %s '%s'" % (k, op, value))

            query += " , ".join(set_l)
            where_l = []
            for k, v in list(wdict.items()):
                op = "="
                value = v
                if isinstance(v, int):
                    where_l.append("%s %s %d" % (k, op, value))
                elif isinstance(v, bool):
                    where_l.append("%s %s %s" % (k, op, value))
                else:
                    # enclose string in quotations
                    where_l.append("%s %s '%s'" % (k, op, value))

            where_str = " WHERE %s" % " AND ".join(where_l)
            query += where_str
            print(query)
            db_conn.execute(query)
            db_conn.commit()
            db_conn.close()
            return
        except Exception as e:
            print(e)
            if attempt == 2:
                raise e
            continue

def delete_db(table_name: str, wdict: dict):
    db_conn = get_db_connection()
    for attempt in range(3):
        try:
            db_conn = get_db_connection()
            query = "DELETE FROM " + table_name
            where_l = []
            for k, v in list(wdict.items()):
                op = "="
                value = v
                if isinstance(v, int):
                    where_l.append("%s %s %d" % (k, op, value))
                else:
                    # enclose string in quotations
                    where_l.append("%s %s '%s'" % (k, op, value))

            where_str = " WHERE %s" % " AND ".join(where_l)
            query += where_str
            print(query)
            db_conn.execute(query)
            db_conn.commit()
            db_conn.close()
            return
        except Exception as e:
            print(e)
            if attempt == 2:
                raise e
            continue

def get_from_db(table_name: str, wdict: dict, columns: list=[]):
    for attempt in range(3):
        try:
            db_conn = get_db_connection()
            if not columns:
                fields = "*"
            else:
                fields = ""
                for column in columns:
                    fields += column + ", "
                fields = fields[:-2]

            query = "SELECT " + fields + " FROM " + table_name
            if wdict:
                where_l = []
                for k, v in list(wdict.items()):
                    op = "="
                    value = v
                    if isinstance(v, int):
                        where_l.append("%s %s %d" % (k, op, value))
                    elif isinstance(v, bool):
                        where_l.append("%s %s %s" % (k, op, value))
                    else:
                        # enclose string in quotations
                        where_l.append("%s %s '%s'" % (k, op, value))

            where_str = " WHERE %s" % " AND ".join(where_l)
            query += where_str
            print(query)
            rows = db_conn.execute(query).fetchall()
            db_conn.close()
            return rows
        except Exception as e:
            print(e)
            if attempt == 2:
                raise e
            continue



@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


"""
Reads email id in "gmailid" parameter,
returns { "status": "google_drive_id"}
"""
@app.route('/register', methods = ['POST'])
def register():
    content = request.get_json()
    google_drive_id = ""
    try:
        f = open('credentials.json')
        credentials = json.load(f)
        f.close()
        gmailid = content["gmailid"].strip()
        wdict = {
            "gmailid": gmailid
        }
        result = get_from_db("uuids", wdict, ["google_drive_id"])
        if result:
            print("user already registered")
            google_drive_id = result[0][0]
            return jsonify({"status": "SUCCESS", "credentials": credentials, "google_drive_id": google_drive_id})
        google_drive_id = generate_google_drive_id()
        if google_drive_id == "":
            raise Exception("No google drive ids available")
        insert_into_db("uuids", [gmailid, google_drive_id])

        return jsonify({"status": "SUCCESS", "credentials":credentials, "google_drive_id": google_drive_id})
    except Exception as e:
        if google_drive_id != "":
            add_google_drive_id(google_drive_id)
        return jsonify({"status": "FAILURE", "message": str(e)})


@app.route('/listnames', methods = ['GET'])
def list_names():
    content = request.get_json()
    gmailid = content["gmailid"]
    wdict = {
        "gmailid": gmailid
    }
    try:
        db_op = get_from_db("repository", wdict, ["name"])
        names = [row[0].strip() for row in db_op]
        return jsonify({"names": names, "status": "SUCCESS"})
    except Exception as e:
        return jsonify({"status": "FAILURE", "message": str(e)})




@app.route('/policy', methods = ['POST', 'GET'])
def policy():
    content = request.get_json()
    gmailid = content["gmailid"]
    name = content["name"]
    if request.method == 'POST':
        values = []
        values.append(gmailid)
        values.append(name)
        values.append(json.dumps(content["policy"]))
        values.append(content["local_path"])
        try:
            insert_into_db("repository", values)
            return jsonify({"status": "SUCCESS"})
        except Exception as e:
            return jsonify({"status": "FAILURE", "message": str(e)})

    elif request.method == 'GET':
        wdict = {
            "name": name,
            "gmailid": gmailid
        }
        try:
            policy =json.loads(get_from_db("repository",wdict,["policy"])[0][0])
            return jsonify({"policy": policy,"status": "SUCCESS"})
        except Exception as e:
            return jsonify({"status": "FAILURE", "message":str(e)})


@app.route('/policy/update', methods = ['POST'])
def update_policy():
    content = request.get_json()

    gmailid = content["gmailid"]
    name = content["name"]
    policy = json.dumps(content["policy"])
    print(type(policy))
    try:
        wdict = {
            "gmailid": gmailid,
            "name": name
        }
        values_dict = {
            "policy": policy
        }
        update_db("repository", wdict, values_dict)
        return jsonify({"status": "SUCCESS"})
    except Exception as e:
        return jsonify({"status": "FAILURE", "message": str(e)})

@app.route('/policy/delete', methods = ['DELETE'])
def delete_policy():
    content = request.get_json()
    gmailid = content["gmailid"]
    name = content["name"]
    try:
        wdict = {
            "gmailid": gmailid,
            "name": name
        }
        delete_db("repository", wdict)
        return jsonify({"status": "SUCCESS"})
    except Exception as e:
        return jsonify({"status": "FAILURE", "message": str(e)})



if __name__ == '__main__':
    app.run(debug=True)


