from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class ToDo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable =False)
    Desc = db.Column(db.String(500), nullable =False)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Title}"
        

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        Title=(request.form['Title'])
        Desc=request.form['Desc']
        todo=ToDo(Title=Title, Desc=Desc)
        db.session.add(todo)
        db.session.commit()
    allToDo = ToDo.query.all()
    #print(allToDo)
    return render_template('index.html', allToDo = allToDo)
    #return 'Hello, World!'

@app.route('/show')
def products():
    allToDo=ToDo.query.all()
    print(allToDo)
    return 'This is products page'

@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo=ToDo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:Sno>',methods=['GET','POST'])
def update(Sno):
    if request.method=='POST':
        Title=(request.form['Title'])
        Desc=request.form['Desc']
        todo=ToDo.query.filter_by(Sno=Sno).first()
        todo.Title=Title
        todo.Desc=Desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=ToDo.query.filter_by(Sno=Sno).first()
    return render_template("update.html",todo=todo)

if __name__=="__main__":
   app.run(debug=True,port=8000)

   