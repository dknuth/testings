import random, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models import Base, User
from flask import Flask


DBNAME='db.sqlite'
app = Flask(__name__)


@app.route('/')
def main():
    return "OK"


@app.route('/produce/<id>')
def produce(id):
    obj = User('user_%03d'%int(id), random.randrange(15, 90))
    session()
    session.add(obj)
    session.commit()
    session.remove()
    return ''



@app.route("/refresh/<id>")
def refresh(id):
    session()
    obj = session.query(User).get(id)
    session.refresh(obj)
    session.remove()
    return ''



@app.route("/update/<id>")
def update(id):
    session()
    obj = session.query(User).get(id)
    obj.name = 'update_user_%03d'%int(id)
    session.add(obj)
    session.commit()
    session.remove()
    return ''



if __name__ == '__main__':
    os.path.isfile(DBNAME) and os.unlink(DBNAME)
    __builtins__.engine = create_engine('sqlite:///'+DBNAME)
    __builtins__.session = scoped_session(
        sessionmaker(
            autoflush = False,
            autocommit = False,
            bind = engine)
        )
    Base.metadata.create_all(engine)
    app.run(debug=True)
