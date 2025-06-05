import pandas as pd
import requests
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import seaborn as sns 
import yfinance as yf
import io
from uuid import uuid4

# BLS API endpoint
def fetch_data(): 
    load_dotenv()
    api = os.getenv('BLS_API_KEY')
    if not api:
        print("Error: BLS_API_KEY not found in .env file")
        exit()

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    current_year = datetime.now().year 


    # Parameters for BLS API (example: CES0000000001 for Total Nonfarm Employment, seasonally adjusted)
    series_id = "CES0000000001"  # Total Nonfarm Employment
    payload = {
        "seriesid": [series_id],
        "startyear": str(current_year - 10),
        "endyear": str(current_year),
        "registrationkey": api  # Replace with your key or remove if unregistered
    }

    # Make API request
    response = requests.post(url, json=payload)
    data = response.json()

    # Check API response status
    if data["status"] != "REQUEST_SUCCEEDED":
        print("Error:", data["message"])
        exit()

    # Extract data from response
    series_data = data["Results"]["series"][0]["data"]

    # Creating a dateframe
    year = []
    period = []
    month = []
    value = []
    date = []
    date_datetime = [] 

    for entry in series_data:
        year.append(int(entry["year"]))
        period.append(entry["period"])      # e.g., M01
        month.append(entry["periodName"])   # e.g., January
        value.append(float(entry["value"])) # Employment in thousands
    
        # Create date string (e.g., "2025-01")
        month_num = entry["period"].replace("M", "")  # Extract "01" from "M01"
        date_str = f"{entry['year']}-{month_num}"
        date.append(date_str)
    
        # Making a datetime object
        date_dt = datetime.strptime(date_str, "%Y-%m")
        date_datetime.append(date_dt)

    # Create DataFrame
    df = pd.DataFrame({
        'Date': date_datetime,
        "year": year,
        "period": period,
        "month": month,
        "value": value
    })

    # Getting SPY500 data
    today = datetime.now() 
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=10*365)).strftime("%Y-%m-%d")
    raw_data_sp500 = yf.download('^GSPC', start=start_date, end=end_date, interval='1mo')
    df_sp500 = pd.DataFrame(raw_data_sp500.values, columns=['Close', 'High', 'Low', 'Open', 'Volume'])
    dates = raw_data_sp500.index.strftime('%Y-%m-%d').tolist()
    datetime_dates = pd.to_datetime(dates)
    df_sp500.insert(0, 'Date', dates)
    df_sp500['Date'] = pd.to_datetime(df_sp500['Date']) 

    # Merge the two dataframe 
    df_merged = pd.merge(df, df_sp500, on='Date', how='inner')
    return df_merged 

def generate_plot(df_merged):
    # Create dual-axis basic line plot
    plt.figure(figsize=(12, 7))
    ax1 = plt.plot(df_merged["Date"], df_merged["value"], color="#00008B", label="Nonfarm Payroll")  # Dark blue line
    ax1 = plt.gca()  # Get current axis

    # Secondary y-axis for S&P 500
    ax2 = ax1.twinx()
    ax2.plot(df_merged["Date"], df_merged["Close"], color="#006400", label="S&P 500")  # Dark green line

    # Prepare legend entries for last two nonfarm payroll values
    legend_handles = []
    legend_labels = []
    if len(df_merged) >= 2:
        for i in [0, 1]:
            date = df_merged["Date"].iloc[i].strftime("%b %Y")  # e.g., "Jan 2025"
            value = df_merged["value"].iloc[i]
            legend_labels.append(f"{date}: Nofarm Payroll {value:,.0f}")
            legend_handles.append(mpatches.Patch(color='none'))  # No color patch

    # Combine line and payroll value legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend_handles = lines1 + lines2 + legend_handles
    legend_labels = labels1 + labels2 + legend_labels

    # Customize plot
    ax1.set_title("U.S. Nonfarm Payroll vs. S&P 500", fontsize=16, fontweight="bold")
    ax1.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Jobs (Thousands)", fontsize=12, fontweight="bold", color="#00008B")
    ax2.set_ylabel("S&P 500 Close", fontsize=12, fontweight="bold", color="#006400")
    ax1.tick_params(axis='x', rotation=45, labelsize=10)
    ax1.tick_params(axis='y', labelcolor="#00008B")
    ax2.tick_params(axis='y', labelcolor="#006400")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Create combined legend in top left
    plt.legend(legend_handles, legend_labels, loc="upper left", fontsize=10)

    plt.tight_layout()
    
    # Save plot
    static_dir = 'static'
    #if not os.path.exists(static_dir):
        #os.makedirs(static_dir)
        # Save plot to static directory
        #plot_path = os.path.join(static_dir, 'bls_jobs_plot.png')
        #plt.savefig(plot_path, format='png', dpi=300, bbox_inches="tight")
        #plt.close()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    plot_filename =  f'bls_jobs_plot.png'
    #plot_filename = f'bls_jobs_plot_{timestamp}.png'
    plot_path = os.path.join(static_dir, plot_filename)
    plt.savefig(plot_path, format='png', dpi=300, bbox_inches="tight")
   
    return plot_filename
    