from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('View Record')


class ViewMedicalRecordForm(FlaskForm):
    record_id = StringField('Record ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    decryption_key = StringField('Decryption Key', validators=[DataRequired()])
    submit = SubmitField('View Record')


class AddMedicalRecordForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    information = StringField('Information', validators=[DataRequired()])
    submit = SubmitField('Add Record')


class EmergencyForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    special_password = PasswordField('Special Password', validators=[DataRequired()])
    decryption_key = StringField('Decryption Key', validators=[DataRequired()])
    submit = SubmitField('View Emergency Record')
