from flask import Flask,render_template,jsonify,request
from database import load_cafe_from_db,load_cafes_from_db,add_cafe_to_db,add_review_for_cafe_to_db,to_dict
app = Flask(__name__)
import requests

@app.route('/')
def home():
    cafes=load_cafes_from_db()
    return render_template("home.html",cafes=cafes)
@app.route("/api/cafes")
def list_cafes():
  cafe = load_cafes_from_db()
  return jsonify(cafe)


@app.route("/cafe/<id>")
def show_job(id):
    cafe = load_cafe_from_db(id)
    return render_template('cafepage.html',
                           cafe=cafe[0])


@app.route("/api/cafe/<id>",methods=['post'])
def show_job_json(id):
    job = load_cafe_from_db(id)
    return jsonify(job)


@app.route("/cafe/<id>/review", methods=['POST','GET'])
def add_cafe_to_db(id):
    data = request.form
    datas=data.to_dict()
    print(datas)
    cafe = load_cafe_from_db(id)
    add_review_for_cafe_to_db(id,datas)
    return render_template('application_submitted.html',
                           application=data,cafe=cafe[0])


if __name__ == '__main__':
  app.run(debug=True)