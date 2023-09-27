from flask import Flask, jsonify ,request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import capture_message,capture_exception
from flask_sqlalchemy import SQLAlchemy
import os

sentry_sdk.init(
    dsn="https://32b1ead440a0ab13015fd695892b365b@o4505924687233024.ingest.sentry.io/4505924692738048",
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
app = Flask(__name__)

db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost:5433/persistencia_datos'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://'+db_user+':'+db_password+'@'+db_host+'/'+db_name
db=SQLAlchemy(app)
class Student(db.Model):
  __tablename__='students'
  id=db.Column(db.Integer,primary_key=True)
  fname=db.Column(db.String(40))
  lname=db.Column(db.String(40))
  email=db.Column(db.String(40))

  def __init__(self, fname, lname, email):
      self.fname = fname
      self.lname = lname
      self.email = email


@app.route('/')
def index():
    capture_message('Todo OK')
    return ("Todo OK2")

@app.route('/students', methods=['GET'])
def obtener_usuarios():
    try:
        students = Student.query.all()
        students_lista = []
        for student in students:
            student_dict = {
                'id': student.id,
                'nombre': student.fname,
                'email': student.email
            }
            students_lista.append(student_dict)
    except Exception as error_general:
        capture_exception(error_general)
    else:
        capture_message('200 - Consulta Exitosa')
        return jsonify({'usuarios': students_lista}), 200
    finally:
        print("OK")

@app.route('/insert', methods=['POST'])
def insertar_estudiante():
    try:
        if request.method == 'POST':
            data = request.get_json()

            nuevo_estudiante = Student(
                fname=data['fname'],
                lname=data['lname'],
                email=data['email']
            )

            db.session.add(nuevo_estudiante)
            db.session.commit()

    except Exception as error_general:
        capture_exception(error_general)
    else:
        capture_message('201 - Insercion Exitosa')
        return jsonify({'message': 'Estudiante insertado correctamente2'}), 201
    finally:
        print("OK")

# Start the Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
