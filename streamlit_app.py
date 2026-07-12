import streamlit as st
import plotly.graph_objects as go
import math
import numpy as np

# Overskrift i appen
st.title("Effekttrekant for Vekselstrøm")

# Input-felter i venstre side (sidebar)
st.sidebar.header("Indtast data")
p = st.sidebar.number_input("Aktiv effekt P (MW)", value=3.0, step=0.1)
q = st.sidebar.number_input("Reaktiv effekt Q (MVar)", value=2.0, step=0.1)

# Automatiske beregninger
s = math.sqrt(p**2 + q**2)
vinkel_rad = math.atan2(q, p)
vinkel_grader = math.degrees(vinkel_rad)
cos_phi = p / s if s > 0 else 1.0

# Vis resultater med pæne tal under overskriften
st.write("### Resultater")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Aktiv (P)", f"{p:.2f} MW")
col2.metric("Reaktiv (Q)", f"{q:.2f} MVar")
col3.metric("Tilsyneladende (S)", f"{s:.2f} MVA")
col4.metric("Effektfaktor (cos φ)", f"{cos_phi:.2f}")

# Byg interaktiv graf med Plotly
fig = go.Figure()

# 1. Aktiv effekt P (Vandret rød linje)
fig.add_trace(go.Scatter(
    x=[0, p], y=[0, 0],
    mode='lines+markers',
    name=f'P = {p:.2f} MW',
    line=dict(color='red', width=4),
    hoverinfo='text',
    text=[f'Start (0,0)', f'P = {p:.2f} MW']
))

# 2. Reaktiv effekt Q (Lodret blå linje)
fig.add_trace(go.Scatter(
    x=[p, p], y=[0, q],
    mode='lines+markers',
    name=f'Q = {q:.2f} MVar',
    line=dict(color='blue', width=4),
    hoverinfo='text',
    text=[f'P-ende', f'Q = {q:.2f} MVar']
))

# 3. Tilsyneladende effekt S (Skrå grøn linje)
fig.add_trace(go.Scatter(
    x=[0, p], y=[0, q],
    mode='lines+markers',
    name=f'S = {s:.2f} MVA',
    line=dict(color='green', width=4),
    hoverinfo='text',
    text=[f'Start (0,0)', f'S = {s:.2f} MVA']
))

# 4. Tegn vinkelbuen (Sort, tynd og krydser linjerne en smule)
bue_radius = p * 0.20 if p > 0 else 0.6  # Gjort en smule større
vinkler = np.linspace(-0.02, vinkel_rad + 0.1, 40)  # Går lidt under 0 og lidt over vinkel_rad for at krydse
bue_x = bue_radius * np.cos(vinkler)
bue_y = bue_radius * np.sin(vinkler)

fig.add_trace(go.Scatter(
    x=list(bue_x), y=list(bue_y),
    mode='lines',
    name='Vinkel φ',
    line=dict(color='black', width=1.5),
    hoverinfo='skip'
))

# Layout-opsætning og tilføjelse af tekst inde i grafen
fig.update_layout(
    title='Visuel Interaktiv Effekttrekant med Vinkel',
    xaxis_title='Aktiv effekt (MW)',
    yaxis_title='Reaktiv effekt (MVar)',
    xaxis=dict(range=[-0.5, p + 0.5], gridcolor='lightgray'),
    yaxis=dict(range=[-0.5, q + 0.5], gridcolor='lightgray'),
    plot_bgcolor='white',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.15),
    margin=dict(l=40, r=40, t=40, b=40),
    
    # Her tilføjer vi teksten for vinklen lige over buen
    annotations=[
        dict(
            x=bue_radius * 1.5 * math.cos(vinkel_rad / 2.5),
            y=bue_radius * 1.1 * math.sin(vinkel_rad / 2.5),
            text=f"φ = {vinkel_grader:.1f}°",
            showarrow=False,
            font=dict(size=14, color="black", family="Arial Black")
        )
    ]
)

# Vis grafen i Streamlit
st.plotly_chart(fig, use_container_width=True)
# Lav en pæn afstand under grafen
st.write("")
st.write("")

# Opret to kolonner, hvor den første er bred (4 dele) og den næste er smal (1 del)
col_tom, col_logo = st.columns([4, 1])

with col_logo:
    # Viser logoet i en større version helt ude til højre
    st.image("Logo.png", width=300)
    
