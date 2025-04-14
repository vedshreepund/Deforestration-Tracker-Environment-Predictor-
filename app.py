from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    air_quality = db.Column(db.Integer)
    timestamp = db.Column(db.String(50))

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    new_entry = SensorData(
        temperature=data.get('temperature'),
        humidity=data.get('humidity'),
        air_quality=data.get('air_quality'),
        timestamp=data.get('timestamp')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/')
def index():
    records = SensorData.query.order_by(SensorData.id.desc()).limit(50).all()
    records.reverse()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
