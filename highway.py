
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row  
    return conn


@app.route('/data', methods=['GET'])
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM EVENTS")
    
    rows = cursor.fetchall()
    
    data = [dict(row) for row in rows]  
    
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)