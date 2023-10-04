from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Install Package with Country Codes
# pip install iso3166

# Upgrade Plotly
# pip install --upgrade plotly

# Import Statements
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta

# Notebook Presentation
pd.options.display.float_format = '{:,.2f}'.format

# Load the Data
df_data = pd.read_csv('mission_launches.csv')
# Remove NaN values
clean_df_data = df_data.dropna()

# Create a summary dictionary
data_info = {
    'Data Type': df_data.dtypes.to_dict(),
    'Non-Null Count': df_data.count().to_dict(),
}

# Create a summary dictionary
clean_df_data_info = {
    'Data Type': clean_df_data.dtypes.to_dict(),
    'Non-Null Count': clean_df_data.count().to_dict(),
}


# Create a chart that shows the number of space mission launches by organization
nbr_mission = clean_df_data['Organisation'].value_counts()
v_bar = px.bar(
    x=nbr_mission.index,
    y=nbr_mission.values,
    color=nbr_mission.values,
    color_continuous_scale='Aggrnyl',
    title='Num mission launches by organisation'
)

v_bar.update_layout(
    xaxis_title='Space mission launches by organisation',
    coloraxis_showscale=False,
    yaxis_title='Number of space mission launches',
    # Modify the title font properties including color
    title_font=dict(color='#9126E8', size=19),  # Change 'red' to your desired title color
    xaxis_title_font=dict(color='#FF5733'),  # Change the color of the x-axis title
    yaxis_title_font=dict(color='#2ECC71')  # Change the color of the y-axis title
)

# Convert the chart to HTML
chart_html = v_bar.to_html(full_html=False)


@app.route('/')
def index():
    return render_template('index.html', df_data=df_data, date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/data-exploration')
def data_exploration():
    return render_template('data-exploration.html', df_data=df_data, date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/data-cleaning')
def data_cleaning():
    return render_template('data-cleaning.html', df_data=df_data, data_info=data_info,
                           clean_df_data_info=clean_df_data_info, date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/data-description')
def data_description():
    return render_template('data-description.html', df_data=df_data, date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/nbr-launches-chart')
def nbr_launches_chart():
    return render_template('nbr-launches-chart.html', clean_df_data=clean_df_data, chart_html=chart_html,
                           date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/nbr-actives-vs-retired')
def nbr_actives_vs_retired():
    return render_template('nbr-actives-vs-retired.html', clean_df_data=clean_df_data,
                           date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/mission-status')
def mission_status():
    return render_template('mission-status.html', clean_df_data=clean_df_data,
                           date=datetime.now().strftime("%a %d %B %Y"))


@app.route('/error')
def error_():
    return render_template('error.html', date=datetime.now().strftime("%a %d %B %Y"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
