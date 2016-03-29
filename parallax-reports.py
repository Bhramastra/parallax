from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.cors import cross_origin
import json
app = Flask(__name__)
admin = Admin(app, name='microblog', template_mode='bootstrap3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.db'



db = SQLAlchemy(app)
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(80), unique=True)
    mem = db.Column(db.Float)
    cpu = db.Column(db.Float)

    def __init__(self,ip,mem,cpu):
        self.ip = ip
        self.cpu = cpu
        self.mem = mem
    def json(self):
        data={}
        data['ip']=self.ip
        data['cpu']=self.cpu
        data['mem']=self.mem
        data['id']=self.id
        return data

admin.add_view(ModelView(Node, db.session))

db.create_all()


@app.route('/stat/<int:id>',methods=["GET","PUT","POST","DELETE"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def stat(id):
    node=Node.query.get(id)
    if node is None:
        return jsonify(error="Node not found"),404
    if request.method =='PUT':
        node.cpu=request.form['cpu']
        node.mem=request.form['mem']
        db.session.commit()
        return "Updated",200
    elif request.method == 'DELETE':
        db.session.delete(node)
        db.session.commit()
        return "Deleted",200
    else:
        return jsonify(**(node.json())),200


@app.route('/register',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def register():
    node=Node(request.form['ip'],request.form['mem'],request.form['cpu'])
    db.session.add(node)
    db.session.commit()
    return jsonify(**(node.json())),201


if __name__ == '__main__':
    app.run(debug=True)
