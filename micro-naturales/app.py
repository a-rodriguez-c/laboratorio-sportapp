from flask import Flask, request, jsonify
from .models import db, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/events.db'
db.init_app(app)

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'name': event.name, 'location': event.location, 'severity': event.severity} for event in events])

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = Event(name=data['name'], location=data['location'], severity=data['severity'])
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
