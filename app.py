from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'secretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def clean_data(df):
    """Enhanced data cleaning function"""
    def safe_to_numeric(x):
        try:
            return pd.to_numeric(x.astype(str).str.replace(',', '', regex=True))
        except Exception:
            return x

    df = df.apply(safe_to_numeric)

    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            pass

    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    df = df.drop_duplicates()
    return df

def generate_summary(df):
    numeric_summary = df.select_dtypes(include=['number']).describe().round(2)
    non_numeric_summary = df.select_dtypes(exclude=['number']).describe().round(2)
    summary = pd.concat([numeric_summary, non_numeric_summary], axis=1, sort=False)
    return summary.to_html(classes="table-auto")

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/dashboard/<filename>', methods=['GET', 'POST'])
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        df = pd.read_csv(filepath)
        df = clean_data(df)
        
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_columns = df.select_dtypes(include=['datetime']).columns.tolist()
        
        summary = generate_summary(df)
        data_preview = df.head(20).to_html(classes="table-auto")
        
        chart_html = None
        error_message = None

        if request.method == 'POST':
            x_axis = request.form.get('x_axis')
            y_axis = request.form.get('y_axis')
            
            try:
                if x_axis and y_axis:
                    fig = px.bar(df, x=x_axis, y=y_axis)
                    fig.show()
                else:
                    raise ValueError('Please select valid X and Y axes.')
            except Exception as e:
                error_message = f"Chart error: {str(e)}"
                flash(error_message, 'danger')
        if chart_html is None:
            fig = px.bar(df, x=date_columns[0], y=numeric_columns[0])
            fig.show()
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        return render_template('dashboard.html', 
                               filename=filename, 
                               summary=summary, 
                               data_preview=data_preview, 
                               numeric_columns=numeric_columns,
                               categorical_columns=categorical_columns,
                               date_columns=date_columns,
                               chart_html=chart_html,
                               error_message=error_message)
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'danger')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
