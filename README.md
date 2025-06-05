# Flask Application Installation and Usage Guide
This guide provides step-by-step instructions for installing and running a Flask web application that fetches data, generates plots, and serves them via Waitress, a production-ready WSGI server. The app includes two routes: a homepage (/) and a chart page (/chart).

Access Application: https://nonfarm-payroll.onrender.com 

## Installation Guide

### Prerequisites
- Python: Version 3.8 or higher (3.12 recommended).
- Operating System: Windows, macOS, or Linux.
- Dependencies: Ensure you have pip installed for package management.
- Internet Access: Required for fetching dependencies and (potentially) data in fetch_data().

### Step-by-Step Installation
1. Set Up a Virtual Environment (Recommended) Create a virtual environment to isolate dependencies:
  python -m venv venv

    Activate the virtual environment:
    
        On Windows:
        venv\Scripts\activate
    
        On macOS/Linux:
        source venv/bin/activate

2. Install Required PackagesCreate a requirements.txt file with the following content:
   
       flask==3.0.3
       waitress==3.0.0
       pandas

   Install the dependencies:

       pip install -r requirements.txt

   Note: Additional dependencies (e.g., for bls_jobs.py) such as requests, matplotlib, or plotly may be required depending on the implementation of fetch_data() and generate_plot(). Add them to requirements.txt if needed.

3. Set Up Application StructureEnsure your project directory is structured as follows:
<pre>
  project/
  ├── server.py
  ├── bls_jobs.py
  ├── static/
  │   └── (generated plot files, e.g., chart.png)
  ├── templates/
  │   ├── index.html
  │   └── chart.html
  └── requirements.txt
</pre>
  - server.py: The main Flask application (provided in the code).
  - bls_jobs.py: Contains fetch_data() and generate_plot() functions (not shown but assumed to handle data fetching and plot generation).
  - static/: Directory for generated plot files (e.g., images or JavaScript-based plots).
  - templates/: Directory containing index.html (homepage) and chart.html (chart display page).
    
4. Create Template FilesCreate the following files in the templates/ directory:

    - index.html:

          <!DOCTYPE html>
          <html>
          <head>
            <title>BLS Jobs App</title>
          </head>
          <body>
            <h1>Welcome to the BLS Jobs App</h1>
            <p><a href="/chart">View Jobs Chart</a></p>
          </body>
          </html>


    - chart.html:

           <!DOCTYPE html>
            <html>
            <head>
              <title>BLS Jobs Chart</title>
            </head>
            <body>
              <h1>BLS Jobs Data Chart</h1>
              <img src="/static/chart.png" alt="Jobs Chart">
              <p><a href="/">Back to Home</a></p>
            </body>
            </html>

      Note: Adjust chart.html based on the output of generate_plot() (e.g., if it generates a plotly interactive chart, you may need to include JavaScript or modify the template).



5. Verify bls_jobs.py Ensure bls_jobs.py exists and contains working fetch_data() and generate_plot() functions. For example:
      - fetch_data(): Should return a pandas DataFrame (e.g., df_merged).
      - generate_plot(): Should save a plot to static/ (e.g., static/chart.png). If these functions rely on external APIs (e.g., BLS API), ensure you have configured API keys or environment variables.

6. Environment ConfigurationIf fetch_data() requires API keys or other configurations, set them as environment variables:

      - On macOS/Linux:

            export BLS_API_KEY="your-api-key"



     - On Windows:

            set BLS_API_KEY=your-api-key

        Alternatively, use a .env file with python-dotenv (add python-dotenv to requirements.txt and load it in bls_jobs.py).


## Usage Guide

### Running the Application Locally
1. Start the ServerWith the virtual environment activated, run:

        python app.py

    Waitress will start the server, and you’ll see output like:

        Serving on http://0.0.0.0:8080

2. Access the Application
   - Open a browser and navigate to http://localhost:8080 to view the homepage.
   - Click the link or go to http://localhost:8080/chart to view the chart page.
   - The /chart route fetches data, saves it as bls_jobs_data.csv (optional), generates a plot, and renders chart.html with the plot.
   - 
3. Expected Behavior
   - Homepage (/): Displays a simple welcome page with a link to the chart.
   - Chart Page (/chart): Fetches data using fetch_data(), generates a plot with generate_plot(), and displays it. If an error occurs, a 500 error with a message is returned.
   - Logs: Errors are logged to the console (or a file if configured) for debugging.

## Example Output
- Homepage: A simple page with a "View Jobs Chart" link.
- Chart Page: Displays a plot (e.g., a PNG image) based on the data fetched by fetch_data().
- Error Handling: If an error occurs in /chart, you’ll see a message like Error: Failed to fetch data in the browser, with details logged to the console.

