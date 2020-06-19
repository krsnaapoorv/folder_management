from flask import Flask
from flask import request, make_response, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kushal#025'
app.config['MYSQL_DB'] = 'hierarchial_data'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/showbelow', methods = ['POST'])
def below_folder():
    val = request.json['ancestor']
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT f.* FROM folders f join treePaths t on (f.id = t.descendent) WHERE t.ancestor = %s AND depth = %s""",(val,1,)
    )
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"folders":results,"value":val})

@app.route('/showabove', methods = ['POST'])
def above_folder():
    val = request.json['descendent']
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT id FROM folders f join treePaths t on (f.id = t.ancestor) WHERE t.descendent = %s AND depth = %s""",(val,1,)
    )
    result = cursor.fetchone()['id']
    print(result)
    cursor.execute(
        """SELECT f.* FROM folders f join treePaths t on (f.id = t.descendent) WHERE t.ancestor = %s AND depth = %s""",(result,1,)
    )
    siblings = cursor.fetchall()
    cursor.close()
    return jsonify({"folders":siblings,"value":result})

def get_last_id():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT id FROM folders ORDER BY id DESC LIMIT 1"""
    )
    result = cursor.fetchone()['id']
    cursor.close()
    return result

def add_foler_to_folders(folder_name):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO folders(folder_name) VALUES(%s)""",(folder_name,)
    )
    mysql.connection.commit()
    cursor.close()
    return True


@app.route('/addfolder', methods = ['POST'])
def create_folder():
    folder_name = request.json['folder_name']
    parent = request.json['parent']
    check = add_foler_to_folders(folder_name)
    created_folder_id = get_last_id()
    if check:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO treePaths(ancestor,descendent,depth) SELECT ancestor,%s,depth+1 FROM treePaths WHERE descendent = %s UNION ALL SELECT %s,%s,%s """,(created_folder_id,parent,created_folder_id,created_folder_id,0,)
        )
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message":"folder created"})
    
    
    
