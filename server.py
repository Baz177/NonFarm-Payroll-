from flask import Flask, render_template
from bls_jobs import fetch_data, generate_plot
import logging
from waitress import serve

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart')
def chart():
    try:
        df_merged, change = fetch_data()
        # Save DataFrame to CSV (optional, for debugging or download)
        df_merged.to_csv("bls_jobs_data.csv", index=False)
        # Generate and save the plot to static directory, get the filename
        generate_plot(df_merged, change)
        return render_template('chart.html')
    except Exception as e:
        logger.error(f"Error in /chart route: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)