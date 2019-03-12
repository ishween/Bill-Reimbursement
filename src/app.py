from flask import Flask, render_template
from src.db.database import Database

app = Flask(__name__)
app.secret_key = 'ishween'
app.config.from_object('config')

@app.before_first_request
def db_initialize():
    print("created")
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


from src.models.admins.views import admin_blueprint
from src.models.employees.views import employee_blueprint
from src.models.managers.views import manager_blueprint
from src.models.billTypes.views import billType_blueprint
from src.models.bills.views import bill_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(employee_blueprint)
app.register_blueprint(manager_blueprint)
app.register_blueprint(billType_blueprint, url_prefix='/billType')
app.register_blueprint(bill_blueprint, url_prefix='/bill')

# newlist = sorted(list_to_be_sorted, key=lambda k: k['name'])
