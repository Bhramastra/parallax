from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.cors import cross_origin
import json,socket
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
admin = Admin(app, name='microblog', template_mode='bootstrap3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.db'
app.secret_key="gaurab"


db = SQLAlchemy(app)
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(80))
    mem = db.Column(db.Float)
    cpu = db.Column(db.Float)
    status = db.Column(db.String(20))

    def __init__(self,ip,mem,cpu):
        self.ip = ip
        self.cpu = cpu
        self.mem = mem
        self.status= "online"

    def send(self,command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try :
            s.connect(('0.0.0.0',1200))
            s.send
            s.send(str(command))
            res=s.recv(4096)
            self.status=res
        except Exception as e:
            print str(e)
            print 'Unable to connect'

    def json(self):
        data={}
        data['ip']=self.ip
        data['cpu']=self.cpu
        data['mem']=self.mem
        data['id']=self.id
        data['status']= self.status
        return data



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node = db.Column(db.Integer,db.ForeignKey(Node.id),primary_key=True)

admin.add_view(ModelView(Node, db.session))
admin.add_view(ModelView(Task, db.session))
db.create_all()


@app.route('/restart/<id>',methods=["GET"])
@app.route('/shutdown/<id>',methods=["GET"])
@app.route('/eot/<id>',methods=["GET"])
def action(id):
    id=int(id)
    node=Node.query.get(id)
    if node is None:
        return jsonify(error="Node not found"),404
    rule=request.url_rule
    if 'restart' in rule.rule:
        command=2
        node.status="Restarting"
    elif 'shutdown' in rule.rule:
        command=1
        node.status="Shutting Down"
    elif 'eot' in rule.rule:
        command=3
        node.status="Killing all tasks"
    db.session.commit()
    print command
    node.send(command)
    nodes=Node.query.all()
    return render_template('manage.html',nodes=nodes)



@app.route('/manage',methods=["GET"])
def manage():
    nodes=Node.query.all()
    return render_template('manage.html',nodes=nodes)


@app.route('/nodes/<stat>',methods=["GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def ret_nodes(stat):
    stat = str(stat)
    nodes=Node.query.filter_by(status=stat).all()
    nodelist=[]
    for node in nodes:
        nodelist.append(node.json())
    return jsonify(nodes=nodelist),200

@app.route('/stat/<int:id>',methods=["GET","PUT","POST","DELETE"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def stat(id):
    node=Node.query.get(id)
    if node is None:
        return jsonify(error="Node not found"),404
    if request.method =='PUT':
        node.cpu=request.form['cpu']
        node.mem=request.form['mem']
        if 'status' in request.form:
            node.status=request.form['status']
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
    print request.form['ip']
    node=Node(request.form['ip'],request.form['mem'],request.form['cpu'])
    db.session.add(node)
    db.session.commit()
    return jsonify(**(node.json())),201


@app.route('/myip',methods=["GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def myip():
    return jsonify(ip=request.environ['REMOTE_ADDR'],ip2=request.remote_addr),200



@app.route('/deploy',methods=["GET"])
def deploy():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    file = open("test.txt", "r")
    try:
        s.connect(('0.0.0.0',1200))
        s.send(str("upload"))
        bytes_read = file.read(1)
        print bytes_read
        print "after bytes"
        while bytes_read:
            s.send(bytes_read)
            bytes_read = file.read(1)
    except Exception as e:
        print str(e)
        print 'Unable to connect'
    finally:
        file.close()
    return "sent",200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
