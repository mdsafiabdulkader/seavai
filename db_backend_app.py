from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sevai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------------- Models ---------------------- #
class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.String(50))
    site_location = db.Column(db.String(100))
    assigned_subcontractor_id = db.Column(db.String(50))
    status = db.Column(db.String(20))

class LaborLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.String(50))
    labor_type = db.Column(db.String(50))
    hours_worked = db.Column(db.Float)
    logged_by = db.Column(db.String(50))
    log_date = db.Column(db.String(20))

class MaterialIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.String(50))
    product_id = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    issued_by = db.Column(db.String(50))
    issue_date = db.Column(db.String(20))

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcontractor_id = db.Column(db.String(50))
    work_order_id = db.Column(db.String(50))
    description = db.Column(db.String(100))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
    due_date = db.Column(db.String(20))

# ---------------------- Routes ---------------------- #

@app.route('/')
def home():
    return "Welcome to SevAI Work Order API"

# WorkOrder
@app.route('/work-orders', methods=['POST'])
def create_work_order():
    data = request.get_json()
    work_order = WorkOrder(**data)
    db.session.add(work_order)
    db.session.commit()
    return jsonify({"message": "Work Order created", "id": work_order.id}), 201

@app.route('/work-orders', methods=['GET'])
def get_work_orders():
    work_orders = WorkOrder.query.all()
    return jsonify([{
        "id": wo.id,
        "purchase_order_id": wo.purchase_order_id,
        "site_location": wo.site_location,
        "assigned_subcontractor_id": wo.assigned_subcontractor_id,
        "status": wo.status
    } for wo in work_orders])

# LaborLog
@app.route('/labor-logs', methods=['POST'])
def create_labor_log():
    data = request.get_json()
    log = LaborLog(**data)
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Labor log created", "id": log.id}), 201

@app.route('/labor-logs', methods=['GET'])
def get_labor_logs():
    logs = LaborLog.query.all()
    return jsonify([{
        "id": l.id,
        "work_order_id": l.work_order_id,
        "labor_type": l.labor_type,
        "hours_worked": l.hours_worked,
        "logged_by": l.logged_by,
        "log_date": l.log_date
    } for l in logs])

# MaterialIssue
@app.route('/material-issues', methods=['POST'])
def create_material_issue():
    data = request.get_json()
    issue = MaterialIssue(**data)
    db.session.add(issue)
    db.session.commit()
    return jsonify({"message": "Material issue created", "id": issue.id}), 201

@app.route('/material-issues', methods=['GET'])
def get_material_issues():
    issues = MaterialIssue.query.all()
    return jsonify([{
        "id": i.id,
        "work_order_id": i.work_order_id,
        "product_id": i.product_id,
        "quantity": i.quantity,
        "issued_by": i.issued_by,
        "issue_date": i.issue_date
    } for i in issues])

# Milestone
@app.route('/milestones', methods=['POST'])
def create_milestone():
    data = request.get_json()
    milestone = Milestone(**data)
    db.session.add(milestone)
    db.session.commit()
    return jsonify({"message": "Milestone created", "id": milestone.id}), 201

@app.route('/milestones', methods=['GET'])
def get_milestones():
    milestones = Milestone.query.all()
    return jsonify([{
        "id": m.id,
        "subcontractor_id": m.subcontractor_id,
        "work_order_id": m.work_order_id,
        "description": m.description,
        "amount": m.amount,
        "status": m.status,
        "due_date": m.due_date
    } for m in milestones])


# ---------------------- Run ---------------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
