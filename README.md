# Data Dashboard with Flask, Pandas, and Plotly

This project is a simple data dashboard built using **Flask**, **Pandas**, and **Plotly**. It allows users to upload CSV files, clean the data, generate summary statistics, preview data, and visualize charts interactively.

## Features
- Upload CSV files
- Clean and preprocess data (e.g., convert to numeric, handle dates, fill missing values)
- Generate descriptive statistics
- Display data previews
- Create bar charts using Plotly
- Error handling with flash messages

## Requirements
Make sure you have Python installed. Then install the required packages using the following command:

```bash
pip install Flask pandas plotly
```

## Project Structure
```
csv_dashboard/
│
├── app.py                # Main Flask application
├── templates/
│   ├── index.html        # Home page
│   ├── upload.html       # Upload page
│   └── dashboard.html    # Dashboard view
├── uploads/              # Uploaded CSV files
└── README.md             # Project documentation
```

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/jasirck/CSV-dashboard.git
cd csv_dashboard
```

4. Start the application:
```bash
python app.py
```

5. Open your browser and go to:
```
http://127.0.0.1:5000/
```

## Usage
1. **Upload a CSV**: Navigate to the upload page and select a CSV file.
2. **Data Cleaning**: The application will clean the data by converting values to numeric, handling dates, and removing duplicates.
3. **Data Summary**: View basic statistical summaries and data previews.
4. **Visualize Data**: Select numeric and date columns to generate bar charts using Plotly.

## Error Handling
- Invalid file types are rejected.
- Incorrect data formats trigger an appropriate error message.
- Users receive feedback using flash messages.

## License
This project is licensed under the MIT License. Feel free to modify and adapt it for your own use.

