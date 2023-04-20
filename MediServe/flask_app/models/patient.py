from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "medisave"
class Patient:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.patient_name = db_data['patient_name']
        self.gender = db_data['gender']
        self.sympthoms = db_data['sympthoms']
        self.date = db_data['date']
        self.address = db_data['address']
        self.contact = db_data['contact']
        self.email = db_data['email']
        self.Insurance_Info = db_data['Insurance_Info']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None







    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM patients
                JOIN users on patients.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        patients = []
        for row in results:
            this_patient = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_patient.creator = user.User(user_data)
            patients.append(this_patient)
        return patients


    @classmethod
    def get_allMyPatients(cls, data ):
        query = "SELECT * FROM patients JOIN users on patients.user_id = users.id where user_id=%(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        
        patients = []
        for row in results:
            this_patient = cls(row)
            y = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            
            this_patient.creator = user.User(y)
            patients.append(this_patient)
        return patients


    


    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM patients
                JOIN users on patients.user_id = users.id
                WHERE patients.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_patient = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_patient.creator = user.User(user_data)
        return this_patient
    


    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO patients (patient_name,gender,sympthoms,date,address,contact,email,Insurance_Info,user_id)
                VALUES (%(patient_name)s,%(gender)s,%(sympthoms)s,%(date)s,%(address)s,%(contact)s,%(email)s,%(Insurance_Info)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE patients
                SET patient_name = %(patient_name)s,
                gender = %(gender)s,
                sympthoms = %(sympthoms)s ,
                date = %(date)s,
                contact= %(contact)s,
                address= %(address)s,
                email= %(email)s,
                insurance_info= %(Insurance_Info)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM patients
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_patient(form_data):
        is_valid = True

        if len(form_data['patient_name']) < 5:
            flash("Name must be at least 5 characters long.")
            is_valid = False
        if len(form_data['gender']) < 2:
            flash("Description must be at least 2 characters long.")
            is_valid = False
        if len(form_data['sympthoms']) > 80:
            flash("Symptoms must be less than 50 characters long.")
            is_valid = False
        if form_data['date'] == '':
            flash("Please input a date.")
            is_valid = False

        return is_valid
        
