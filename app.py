from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # . Para trabajar con la base de datos

# . Por convencion, el app simpre es creado con (__name__)
app = Flask(__name__)

# . Nombre del path de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # . base de datos

# . Creando las columnas de mi base de datos y seteando que tipos de datos soportan dichas columnas


class Todo(db.Model):  # . Utiliza un modelo de Todo de SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # . Crea e inicializa la base de datos
        print("Nueva base de datos creada")
    app.run(debug=True)
else:
    print("Base da datos existente")


# . Creando el router
@app.route("/", methods=["GET", "POST"])  # . homepage
def home():
    todo_list = db.session.query(Todo).all()
    if request.method != "POST":
        return render_template("base.html", todo_list=todo_list)
    if title := request.form.get("title"):
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        error_message = "Titulo no puede estar en blanco."
        todo_list = db.session.query(Todo).all()
        return render_template("base.html", todo_list=todo_list, error_message=error_message)


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
