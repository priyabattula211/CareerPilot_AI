import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def draw_language_pie_chart(languages_dict):
    """Draws a pie chart for GitHub languages."""
    df = pd.DataFrame(list(languages_dict.items()), columns=['Language', 'Usage'])
    fig = px.pie(df, values='Usage', names='Language', hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    return fig

def draw_readiness_radar_chart(categories_dict):
    """Draws a radar chart for interview readiness categories."""
    categories = list(categories_dict.keys())
    values = list(categories_dict.values())
    
    # Close the loop for radar chart
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      line_color='#4F46E5',
      fillcolor='rgba(79, 70, 229, 0.4)'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 100],
          gridcolor='#334155'
        ),
        angularaxis=dict(
            gridcolor='#334155'
        ),
        bgcolor='rgba(0,0,0,0)'
      ),
      showlegend=False,
      paper_bgcolor='rgba(0,0,0,0)',
      font=dict(color='#F8FAFC')
    )
    return fig
