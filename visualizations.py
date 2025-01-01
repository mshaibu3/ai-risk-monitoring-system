import plotly.express as px
import pandas as pd

def generate_dashboard():
    data = {'Risk Level': ['Low', 'High'], 'Count': [50, 30]}
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Risk Level', y='Count', title='Risk Distribution')
    return fig.to_html(full_html=False)
