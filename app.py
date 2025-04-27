from flask import Flask,render_template,jsonify
import os
from google.cloud.sql.connector import Connector
import sqlalchemy
#import pymysql
from sqlalchemy import create_engine, text

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "gcp-sql-key.json"
# initialize Connector object 
connector = Connector()

# initialize parameters
INSTANCE_CONNECTION_NAME = os.environ["INSTANCE_CONNECTION_NAME"] # i.e demo-project:us-central1:demo-instance
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
engine = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def load_jobs_from_db():
    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * from jobs")) #SELECT NOW();
        jobs=[]
        for row in result:
           jobs.append(dict(row._mapping))  
        return jobs
        
app =Flask(__name__)

@app.route('/')
def hello_world():
    jobs=load_jobs_from_db()
    return render_template('home.html',jobs=jobs)

@app.route('/api/jobs')
def list_jobs():
    jobs=load_jobs_from_db()
    return jsonify(jobs)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
