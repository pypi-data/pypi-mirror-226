#https://stackoverflow.com/questions/24101056/how-to-use-mysql-connection-db-pool-with-python-flask

from flask import Flask, jsonify, abort, make_response, request, g
from mysql.connector.pooling import MySQLConnectionPool

app = Flask(__name__)

db_user = "root"
db_pass = "wipro@123"
db_url = "127.0.0.1"


@app.before_first_request
def before_first_request():
    # configure the connection pool in the global object
    # g.cnx_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="name",
    g.cnx_pool = MySQLConnectionPool(pool_name="name",
                                                             pool_size=10,
                                                             autocommit=True,
                                                             user=db_user,
                                                             password=db_pass,
                                                             host=db_url,
                                                             database='db')


@app.route('/log', methods=['GET'])
def log_data():
    """
    Logs data
    """
    #cursor = g.cnx_pool.get_connection().cursor()
    g.cnx_pool = MySQLConnectionPool(pool_name="name",
                                     pool_size=10,
                                     autocommit=True,
                                     user=db_user,
                                     password=db_pass,
                                     host=db_url,
                                     database='db')
    conn = g.cnx_pool.get_connection()
    cursor = conn.cursor()

    query = """INSERT INTO db.data (time,data) values (NOW(),%s)"""
    cursor.execute(query, (request.get_data(),))
    return make_response('Success', 200)


if __name__ == '__main__':
    app.run(debug=True)