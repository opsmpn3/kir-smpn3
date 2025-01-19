from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, DateField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db = SQLAlchemy(app)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=True)

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(100), nullable=True)

class MaintenanceForm(FlaskForm):
    asset_name = StringField('Nama Aset', validators=[DataRequired()])
    maintenance_date = DateField('Tanggal Perawatan', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired()])
    description = TextAreaField('Keterangan', validators=[DataRequired()])
    photo = FileField('Foto')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    rooms = [
        "Kelas 9A", "Kelas 9B", "Kelas 9C", "Kelas 9D", "Kelas 9E", "Kelas 9F", "Kelas 9G", "Kelas 9H",
        "Kelas 8A", "Kelas 8B", "Kelas 8C", "Kelas 8D", "Kelas 8E", "Kelas 8F", "Kelas 8G", "Kelas 8H",
        "Kelas 7A", "Kelas 7B", "Kelas 7C", "Kelas 7D", "Kelas 7E", "Kelas 7F", "Kelas 7G", "Kelas 7H",
        "Ruang Kepala Sekolah", "Ruang Wakil/Staff", "Ruang Guru", "Ruang Tata Usaha", "Ruang Perpustakaan",
        "Ruang BK", "Ruang OSIS", "Ruang Pramuka", "Ruang Lab. IPA", "Ruang Lab. TIK", "Ruang Gudang 1",
        "Ruang Gudang 2", "Ruang Masjid", "Ruang Aula/Bangsal", "Ruang Kecil", "Ruang Piket"
    ]
    kir_info = "Menu KIR berisi daftar ruangan dan informasi terkait. Setiap ruangan memiliki file PDF yang bisa diunduh."
    perawatan_info = "Menu Perawatan Aset berisi form untuk mencatat kegiatan perawatan aset. Form ini mencakup nama aset, tanggal perawatan, keterangan, dan foto aset."
    form = MaintenanceForm()
    return render_template('index.html', rooms=rooms, kir_info=kir_info, perawatan_info=perawatan_info, form=form)

@app.route('/pdf/<path:filename>')
def download_file(filename):
    return send_from_directory('static/pdf', filename)

@app.route('/maintenance', methods=['POST'])
def maintenance():
    form = MaintenanceForm()
    if form.validate_on_submit():
        photo_file = form.photo.data
        filename = secure_filename(photo_file.filename) if photo_file else None
        if filename:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(photo_path)
        new_maintenance = Maintenance(
            asset_name=form.asset_name.data,
            maintenance_date=form.maintenance_date.data,
            description=form.description.data,
            photo=filename
        )
        db.session.add(new_maintenance)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)