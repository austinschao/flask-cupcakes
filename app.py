"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
# db.create_all() /tables created in the seed.py already


@app.get("/")
def display_homepage():
    """ Return a template for the homepage """

    return render_template("index.html")

@app.get("/api/cupcakes")
def list_all_cupcakes():
    """ Return JSON of all cupcakes

        {"cupcakes": [
            {
                "id",
                "flavor",
                "size",
                "rating",
                "image"
            }
        ]}
     """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """ Return JSON of a single cupcake

        {"cupcake":
            {
                "id",
                "flavor",
                "size",
                "rating",
                "image"
            }
        }
     """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """ Create a cupcake from form data and return JSON of it

        {"cupcake":
            {
                "id",
                "flavor",
                "size",
                "rating",
                "image"
            }
        }
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image")

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """Update cupcake and return JSON.
        {"cupcake":
            {
                "id",
                "flavor",
                "size",
                "rating",
                "image"
            }
        }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Delete cupcake and return JSON.
        {"deleted": cupcake_id}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    Cupcake.query.filter_by(id=cupcake_id).delete()

    db.session.commit()

    return jsonify(deleted=cupcake.id)

