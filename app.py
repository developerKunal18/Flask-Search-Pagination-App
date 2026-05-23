from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- Database Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Model ----------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create DB and sample data
with app.app_context():
    db.create_all()

    if Note.query.count() == 0:
        for i in range(1, 31):
            db.session.add(Note(content=f"Sample Note {i}"))
        db.session.commit()

# ---------- Home ----------
@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Note.query

    if search:
        query = query.filter(
            Note.content.contains(search)
        )

    notes = query.paginate(
        page=page,
        per_page=5
    )

    return render_template(
        "index.html",
        notes=notes,
        search=search
    )

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
