import os
from flask import Flask, redirect, render_template, request, url_for
from flask_paginate import Pagination
from neo4j import GraphDatabase


app = Flask(__name__)

MOVIE_IMG = os.path.join('static', 'movies')

app.config['UPLOAD_FOLDER'] = MOVIE_IMG


@app.route("/", methods=['POST', 'GET'])
def index():
    garchig = 'Нүүр хуудас'
    return render_template('index.html', garchig=garchig)


@app.route("/tenhim", methods=['POST', 'GET'])
def tenhim():
    garchig = 'Тэнхим'
    if request.method == 'GET':
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        tenhims = list(session.run(
            "match(t:Tenhim) return t.tenhimName as tenhimName , id(t) as id"))
        return render_template('tenhim.html', garchig=garchig, tenhims=tenhims)
    if request.method == 'POST':
        tenhimName = request.form["tenhimName"]
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        create = list(session.run(
            f"merge (t:Tenhim {{tenhimName:'{tenhimName}'}}) return t.tenhimName"))
        return redirect(url_for('tenhim'))


@app.route("/albantushaal", methods=['POST', 'GET'])
def albantushaal():
    garchig = 'Албан тушаал'
    if request.method == 'GET':
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        albantushaals = list(session.run(
            "match(t:Albantushaal) return t.albantushaalName as albantushaalName , id(t) as id"))
        return render_template('albantushaal.html', garchig=garchig, albantushaals=albantushaals)
    if request.method == 'POST':
        albantushaalName = request.form["albantushaalName"]
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        create = list(session.run(
            f"merge (t:Albantushaal {{albantushaalName:'{albantushaalName}'}}) return t.albantushaalName"))
        return redirect(url_for('albantushaal'))


@app.route("/erdmiinzereg", methods=['POST', 'GET'])
def erdmiinzereg():
    garchig = 'Эрдмийн зэрэг'
    if request.method == 'GET':
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        erdmiinzeregs = list(session.run(
            "match(t:Erdmiinzereg) return t.erdmiinzeregName as erdmiinzeregName , id(t) as id"))
        return render_template('erdmiinzereg.html', garchig=garchig, erdmiinzeregs=erdmiinzeregs)
    if request.method == 'POST':
        erdmiinzeregName = request.form["erdmiinzeregName"]
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        create = list(session.run(
            f"merge (t:Erdmiinzereg {{erdmiinzeregName:'{erdmiinzeregName}'}}) return t.erdmiinzeregName"))
        return redirect(url_for('erdmiinzereg'))


@app.route("/bagsh", methods=['POST', 'GET'])
def bagsh():
    garchig = 'Багш'
    if request.method == 'GET':
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        bagshs = list(session.run(
            """match (e:Erdmiinzereg)-[:HARIYA]-(p:Bagsh)-[:HARIYA]-(t:Tenhim),(p)-[:HARIYA]-(a:Albantushaal)
                return distinct p.firstname as firstname, p.lastname as lastname, p.gender as gender, p.date as date,
                e.erdmiinzeregName as erdmiinzeregName , t.tenhimName as texnhimName , a.albantushaalName as albantushaalName
            """
        ))
        # print(bagshs[0]['lastname'])
        erdmiinzeregs = list(session.run(
            "match(t:Erdmiinzereg) return t.erdmiinzeregName as erdmiinzeregName , id(t) as id"))
        albantushaals = list(session.run(
            "match(t:Albantushaal) return t.albantushaalName as albantushaalName , id(t) as id"))
        tenhims = list(session.run(
            "match(t:Tenhim) return t.tenhimName as tenhimName , id(t) as id"))

        return render_template('bagsh.html', garchig=garchig, bagshs=bagshs, erdmiinzeregs=erdmiinzeregs, albantushaals=albantushaals, tenhims=tenhims)
    if request.method == 'POST':
        bagshLastName = request.form["bagshLastName"]
        bagshFirstName = request.form["bagshFirstName"]
        date = request.form["date"]
        gender = request.form["gender"]
        erdmiinzeregID = request.form["erdmiinzeregID"]
        tenhimID = request.form["tenhimID"]
        albantushaalID = request.form["albantushaalID"]
        gb = GraphDatabase.driver(
            uri="bolt://localhost:7687", auth=("neo4j", "1234"))
        session = gb.session()
        create = list(session.run(
            f"""match 
            (w:Tenhim), 
            (e:Erdmiinzereg), 
            (r:Albantushaal) 
            where id(w) ={tenhimID}  and  id(e) = {erdmiinzeregID} and id(r) = {albantushaalID} 
            merge (p:Bagsh{{firstname:'{bagshFirstName}', lastname:'{bagshLastName}', date:'{date}' ,gender:'{gender}' }})
            merge (p)-[:HARIYA]->(w)
            merge (p)-[:HARIYA]->(r)
            merge (p)-[:HARIYA]->(e)
            return w,p,e,r"""))
        return redirect(url_for('bagsh'))


if __name__ == '__main__':
    app.run(debug=True)
