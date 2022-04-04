"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy


DEFAULT_IMG_URL = "https://tinyurl.com/demo-cupcake"

db = SQLAlchemy()

class Cupcake(db.Model):
    """ Create a cupcake """

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(30), nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False, default = DEFAULT_IMG_URL)

    def serialize(self):
        """ Serialize to dictionary """

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)