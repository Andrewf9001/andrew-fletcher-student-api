from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Info(db.Model):
  __tablename__ = "info"
  id = db.Column(db.Integer, primary_key=True)
  first = db.Column(db.String(20), nullable=False)
  last = db.Column(db.String(20), nullable=False)
  birthday = db.Column(db.String(20), nullable=False)
  skill = db.Column(db.String(30), nullable=False)

  def __init__(self, first, last, birthday, skill):
    self.first = first
    self.last = last
    self.birthday = birthday
    self.skill = skill

class InfoSchema(ma.Schema):
  class Meta:
    fields=("id", "first", "last", "birthday", "skill")

info_schema = InfoSchema()
infos_schema = InfoSchema(many=True)

@app.route("/info", methods=["GET"])
def get_info():
  all_info = Info.query.all()
  result = infos_schema.dump(all_info)
  return jsonify(result.data)

@app.route("/add-info", methods=["POST"])
def add_info():
  first = request.json["first"]
  last = request.json["last"]
  birthday = request.json["birthday"]
  skill = request.json["skill"]

  record = Info(first, last, birthday, skill)

  db.session.add(record)
  db.session.commit()

  info = Info.query.get(record.id)
  return info_schema.jsonify(info)

@app.route("/info/<id>", methods=["PUT"])
def update_info(id):
    info = Info.query.get(id)

    new_first = request.json["first"]
    new_last = request.json["last"]
    new_birthday = request.json["birthday"]
    new_skill = request.json["skill"]

    info.first = new_first
    info.last = new_last
    info.birthday = new_birthday
    info.skill = new_skill
    
    db.session.commit()
    return info_schema.jsonify(info)

@app.route("/info/<id>", methods=["DELETE"])
def delete_info(id):
    record = Info.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("RECORD DELETED")

if __name__ == "__main__":
    app.debug = True
    app.run()