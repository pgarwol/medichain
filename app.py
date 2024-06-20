from flask import Flask, render_template, redirect, url_for, flash

from blockchain import Blockchain
from forms import PatientForm, EmergencyForm, ViewMedicalRecordForm, AddMedicalRecordForm
from smart_contract import SmartContract

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
blockchain = Blockchain(difficulty=5)

logged_doctor_id = "D456"


def create_smart_contract(patient_id, doctor_id):
    return SmartContract(
        patient_id=patient_id,
        doctor_id=doctor_id,
        read=(patient_id, doctor_id),
        write=(doctor_id,),
        edit=(doctor_id,),
        blockchain=blockchain
    )


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    view_form = ViewMedicalRecordForm()
    if view_form.validate_on_submit():
        # Process the form data for viewing medical records
        flash('Viewing medical records', 'success')
        return redirect(url_for('view_medical_record', record_id=view_form.record_id.data))
    return render_template('patient.html', form=form, view_form=view_form)


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    view_form = ViewMedicalRecordForm()
    add_form = AddMedicalRecordForm()
    if view_form.validate_on_submit():
        flash('Viewing medical records', 'success')
        return redirect(url_for('view_medical_record', record_id=view_form.record_id.data))
    elif add_form.validate_on_submit():
        date = add_form.date.data
        patient_id = add_form.patient_id.data
        comment = add_form.comment.data
        predicaments_raw = add_form.predicaments.data.split('\n')
        predicaments = [tuple(item.split(':')) for item in predicaments_raw]
        predicaments = [(name.strip(), int(amount.strip())) for name, amount in predicaments]

        smart_contract = create_smart_contract(patient_id, logged_doctor_id)

        try:
            mined_block = smart_contract.add_medical_record(date, patient_id, comment, predicaments)
            if mined_block:
                flash('Medical record added and saved to blockchain', 'success')
            else:
                flash('Failed to add medical record', 'danger')
        except PermissionError as e:
            flash(str(e), 'danger')

        return redirect(url_for('home'))

    return render_template('doctor.html', view_form=view_form, add_form=add_form)


@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    form = EmergencyForm()
    if form.validate_on_submit():
        # Process the form data for viewing patient medical records
        flash('Viewing patient medical records in emergency', 'success')
        return redirect(url_for('view_medical_record', record_id=form.patient_id.data))
    return render_template('emergency.html', form=form)


@app.route('/view_medical_record/<record_id>')
def view_medical_record(record_id):
    # Placeholder for retrieving and displaying the medical record
    medical_record = {"record_id": record_id, "data": "Sample medical record data"}
    return render_template('view_medical_record.html', medical_record=medical_record)


if __name__ == '__main__':
    app.run(debug=True)
