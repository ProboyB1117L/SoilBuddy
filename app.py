from flask import Flask, render_template, request
from utils.soilscan_logic import analyze_soil
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------- Routes -----------------

# Home Page
@app.route('/')
def home():
    return render_template('HomePage.html')

# Krishi Udaan (example)
@app.route('/krishiudaan')
def krishiudaan():
    return render_template('KrishiUdaanF.html')

# SoilScan input page
@app.route('/soilscan')
def soilscan():
    return render_template('soilscanF.html')  # Make sure filename matches

# SoilScan result page
@app.route('/soilscan/result', methods=['POST'])
def soilscan_result():
    if 'soil_image' not in request.files:
        return "No file uploaded", 400

    file = request.files['soil_image']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Analyze soil image and generate PDF + plot
    soil_params, plot_path, pdf_path = analyze_soil(image_path=file_path)

    return render_template(
        'SoilScanResult.html',
        soil_params=soil_params,
        plot_path=plot_path,
        pdf_path=pdf_path
    )

# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
