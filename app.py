import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Lab Master", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Lab Master")
st.markdown("**By Deep Patel** | *B.Sc. Physics Lab Companion*")
st.divider()

# 2. Create Tabs
tab1, tab2, tab3 = st.tabs(["📊 Data & Graph", "🔄 Unit Converter", "⚛️ Physics Constants"])

# --- TAB 1: GRAPHING ---
with tab1:
    st.header("Premium Data Plotter")
    
    # Custom Axis Labels for a professional look
    col_x, col_y = st.columns(2)
    x_label = col_x.text_input("X-Axis Name (e.g., Voltage (V))", "X-Axis")
    y_label = col_y.text_input("Y-Axis Name (e.g., Current (mA))", "Y-Axis")
    
    st.write("##### ⚙️ Curve Rendering")
    graph_type = st.radio(
        "Select mathematical treatment:", 
        [
            "Smooth Spline (Perfect curve through all points)", 
            "Linear Fit (Straight line of best fit / OLS)", 
            "Trend Curve (Weighted statistical curve / LOWESS)"
        ],
        horizontal=True
    )
    
    st.divider()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Experimental Data")
        st.info("Enter readings. Empty rows are ignored.")
        initial_data = pd.DataFrame({x_label: [None]*20, y_label: [None]*20})
        edited_df = st.data_editor(initial_data, num_rows="fixed", use_container_width=True)
        
    with col2:
        st.subheader("Live Graph")
        clean_df = edited_df.dropna(subset=[x_label, y_label])
        
        if not clean_df.empty:
            clean_df = clean_df.astype(float)
            clean_df = clean_df.sort_values(by=x_label)
            
            # --- GRAPH GENERATION ---
            if len(clean_df) > 1:
                if graph_type == "Linear Fit (Straight line of best fit / OLS)":
                    fig = px.scatter(clean_df, x=x_label, y=y_label, trendline="ols")
                elif graph_type == "Trend Curve (Weighted statistical curve / LOWESS)":
                    fig = px.scatter(clean_df, x=x_label, y=y_label, trendline="lowess")
                else:
                    # The Premium Spline Curve
                    fig = px.line(clean_df, x=x_label, y=y_label)
                    fig.update_traces(line_shape='spline', mode='lines+markers')
            else:
                fig = px.scatter(clean_df, x=x_label, y=y_label)

            # --- PREMIUM STYLING ENGINE ---
            # 1. Layout & Grid
            fig.update_layout(
                title=dict(text=f"<b>{y_label} vs {x_label}</b>", font=dict(size=22, color="#1E293B")),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(family="Arial, sans-serif", size=14, color="#475569"),
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#CBD5E1", zerolinewidth=2),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#CBD5E1", zerolinewidth=2),
                hovermode="x unified",
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            # 2. Style the Data Points (Deep Blue with White Border)
            fig.update_traces(
                marker=dict(size=14, color='#2563EB', line=dict(width=2.5, color='white')),
                selector=dict(mode='markers')
            )
            
            # 3. Style the Mathematical Curves (Vibrant Red/Pink)
            fig.update_traces(
                line=dict(color='#E11D48', width=3.5),
                selector=dict(mode='lines')
            )
            
            # 4. Style the Spline combination (Lines + Markers)
            fig.update_traces(
                marker=dict(size=14, color='#2563EB', line=dict(width=2.5, color='white')),
                line=dict(color='#E11D48', width=3.5),
                selector=dict(mode='lines+markers')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Enter at least one valid reading to render the graph.")

# --- TAB 2: UNIT CONVERTER ---
with tab2:
    st.header("Quick Unit Conversions")
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Length")
        length_val = st.number_input("Enter value:", value=1.0, key="len_val")
        length_units = ["Nanometers", "Micrometers", "Millimeters", "Centimeters", "Meters", "Kilometers"]
        len_from = st.selectbox("From:", length_units, index=4, key="len_from")
        len_to = st.selectbox("To:", length_units, index=3, key="len_to")
        
        len_factors = {
            "Nanometers": 1e-9, "Micrometers": 1e-6, "Millimeters": 1e-3, 
            "Centimeters": 1e-2, "Meters": 1, "Kilometers": 1000
        }
        result = (length_val * len_factors[len_from]) / len_factors[len_to]
        st.success(f"**Result:** {result:g} {len_to}")

    with col4:
        st.subheader("Mass")
        mass_val = st.number_input("Enter value:", value=1.0, key="mass_val")
        mass_from = st.selectbox("From:", ["Kilograms", "Grams", "Milligrams"], key="mass_from")
        mass_to = st.selectbox("To:", ["Kilograms", "Grams", "Milligrams"], key="mass_to")
        
        mass_factors = {"Kilograms": 1, "Grams": 0.001, "Milligrams": 0.000001}
        m_result = (mass_val * mass_factors[mass_from]) / mass_factors[mass_to]
        st.success(f"**Result:** {m_result:g} {mass_to}")

# --- TAB 3: CONSTANTS ---
with tab3:
    st.header("Standard Physics Constants")
    constants_data = {
        "Constant Name": [
            "Speed of Light in Vacuum (c)", "Planck Constant (h)", "Gravitational Constant (G)", 
            "Elementary Charge (e)", "Electron Mass (m_e)", "Proton Mass (m_p)", "Neutron Mass (m_n)",
            "Boltzmann Constant (k)", "Permittivity of Free Space (ε₀)", "Permeability of Free Space (μ₀)",
            "Avogadro's Number (N_A)", "Ideal Gas Constant (R)", "Stefan-Boltzmann Constant (σ)", "Rydberg Constant (R_∞)"
        ],
        "Value": [
            "2.9979 × 10⁸", "6.626 × 10⁻³⁴", "6.674 × 10⁻¹¹", "1.602 × 10⁻¹⁹", "9.109 × 10⁻³¹", 
            "1.672 × 10⁻²⁷", "1.674 × 10⁻²⁷", "1.380 × 10⁻²³", "8.854 × 10⁻¹²", "1.256 × 10⁻⁶",
            "6.022 × 10²³", "8.314", "5.670 × 10⁻⁸", "1.097 × 10⁷"
        ],
        "Unit": [
            "m/s", "J·s", "N·m²/kg²", "C", "kg", "kg", "kg", "J/K", "F/m", "N/A²", "mol⁻¹", "J/(mol·K)", "W/(m²·K⁴)", "m⁻¹"
        ]
    }
    st.dataframe(pd.DataFrame(constants_data), use_container_width=True, hide_index=True)
