from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.patient import Patient
from flask_app.models.user import User




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, patients=Patient.get_all())

@app.route('/new/patient')
def create_patient():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})

    return render_template('patient_new.html',user=user)

@app.route('/patients/new/process', methods=['POST'])
def process_patient():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Patient.validate_patient(request.form):
        return redirect('/new/patient')

    data = {
        'user_id': session['user_id'],
        'patient_name': request.form['patient_name'],
        'gender': request.form['gender'],
        'sympthoms': request.form['sympthoms'],
        'date': request.form['date'],
        'address': request.form['address'],
        'contact': request.form['contact'],
        'email': request.form['email'],
        'Insurance_Info': request.form['Insurance_Info']
    }
    Patient.save(data)
    return redirect('/dashboard')




@app.route('/patients/mypatients/<int:id>')
def mypatients(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')

    data = {
        "id":id
        }
    return render_template('mypatients.html', user=user, patients=Patient.get_allMyPatients(data))




@app.route('/show/<int:id>')
def view_patient(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})

    return render_template('patient_view.html',patient=Patient.get_by_id({'id': id}),user=user)

@app.route('/edit/<int:id>')
def edit_patient(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('patient_edit.html',patient=Patient.get_by_id({'id': id}),user=user)

@app.route('/patients/edit/process/<int:id>', methods=['POST'])
def process_edit_patient(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Patient.validate_patient(request.form):
        return redirect('/edit/{id}')

    data = {
        'id': id,
        'patient_name': request.form['patient_name'],
        'gender': request.form['gender'],
        'sympthoms': request.form['sympthoms'],
        'date': request.form['date'],
        'address': request.form['address'],
        'contact': request.form['contact'],
        'email': request.form['email'],
        'Insurance_Info': request.form['Insurance_Info']
    }
    Patient.update(data)
    return redirect('/dashboard')

@app.route('/patients/destroy/<int:id>')
def destroy_patient(id):
    # user = User.get_by_id({"id":session['user_id']})
    if 'user_id' not in session:
        return redirect('/user/login')
    # data = {
    #     "id":id
    #     }
    Patient.destroy({'id':id})
    # patients=Patient.get_allMyPatients(data)
    # return render_template('dashboard.html', user=user, patients=patients)
    return redirect('/dashboard')
