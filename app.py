from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'secretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Upload CSV Route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard', filename=file.filename))
        else:
            flash('Invalid file. Please upload a CSV file.', 'danger')
    return render_template('upload.html')

# Dashboard Route
@app.route('/dashboard/<filename>', methods=['GET', 'POST'])
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    # Generate Summary and Data Preview
    summary = df.describe().to_html(classes="table table-striped")
    data_preview = df.head(20).to_html(classes="table table-hover")

    # Visualization with Plotly
    columns = df.columns.tolist()
    chart_html = None

    if request.method == 'POST':
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')
        if x_axis and y_axis:
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{x_axis} vs {y_axis}')
            chart_html = fig.to_html(full_html=False)

    return render_template('dashboard.html', filename=filename, summary=summary, data_preview=data_preview, columns=columns, chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
