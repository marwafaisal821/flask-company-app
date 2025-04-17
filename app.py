from flask import Flask, render_template, request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)  

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    employees_count = db.Column(db.Integer)
    location = db.Column(db.String(100))

    def __repr__(self):
        return f"Company('{self.name}', '{self.location}', Employees: {self.employees_count})"

@app.route('/companies')
def list_companies():
    companies = Company.query.all()
    return render_template('home.html', companies=companies)

@app.route('/create_company', methods=['POST'])
def create_company():
    name = request.form.get('name')
    description = request.form.get('description')
    employees_count = request.form.get('employees_count')
    location = request.form.get('location')
   
    new_company = Company(name=name, description=description, employees_count=employees_count, location=location)
    db.session.add(new_company)
    db.session.commit()
    
    return "Company created successfully!"

@app.route('/update_company/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    company.name = request.form.get('name')
    company.description = request.form.get('description')
    company.employees_count = request.form.get('employees_count')
    company.location = request.form.get('location')
    db.session.commit()
    
    return "Company updated successfully!"

@app.route('/company/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get_or_404(id)
    return jsonify({
        'id': company.id,
        'name': company.name,
        'description': company.description,
        'employees_count': company.employees_count,
        'location': company.location
    })




class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    description = StringField('Description')
    employees_count = StringField('Number of Employees')
    location = StringField('Location')
    submit = SubmitField('Submit')

@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()
    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
            description=form.description.data,
            employees_count=form.employees_count.data,
            location=form.location.data
        )
        db.session.add(new_company)
        db.session.commit()
        return "Company added successfully!"
    
    return render_template('form.html', form=form)







if __name__ == "__main__":
    app.run(debug=True)
