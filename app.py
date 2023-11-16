from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def hello_world():
    return 'Hello World!'


# CREATE
@app.route('/players', methods=['POST'])
def add_player():
    player = Players(name=request.json['name'], description=request.json['description'])
    db.session.add(player)
    db.session.commit()
    return {'id': player.id}

# READ
@app.route('/players')
def get_players():
    players = Players.query.all()

    output = []
    for player in players:
        player_data = {'name': player.name, 'description': player.description}

        output.append(player_data)

    return {"players": output}


@app.route('/players/<id>')
def get_player(id):
    player = Players.query.get_or_404(id)
    return {"name": player.name, "description": player.description}


# UPDATE
@app.route('/players/<id>', methods=['PUT'])
def update_player_description(id):
    description = request.json['description']

    player = Players.query.get(id)
    if player is None:
        return {"error": "not found"}
    player.description = description
    db.session.commit()
    return {"message": player.name + " description has been updated to " + player.description}


# DELETE
@app.route('/players/<id>', methods=['DELETE'])
def delete_player(id):
    player = Players.query.get(id)
    if player is None:
        return {"error": "not found"}
    db.session.delete(player)
    db.session.commit()
    return {"message": player.name + " has been deleted!"}


if __name__ == '__main__':
    app.run()
