from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired


class PatientForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    code = PasswordField('Code', validators=[DataRequired()])
    submit = SubmitField('View Record')


class ViewMedicalRecordForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('View Record')


class AddMedicalRecordForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    predicaments = TextAreaField('Medications (name:amount per line)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add Record')


class EmergencyForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    special_password = PasswordField('Special Password', validators=[DataRequired()])
    decryption_key = StringField('Decryption Key', validators=[DataRequired()])
    submit = SubmitField('View Emergency Record')
