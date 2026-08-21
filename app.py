import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Lab Master", layout="wide", page_icon="🔬")

# Custom spacing to look cleaner on mobile screens
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
    st.header("Experimental Data Plotter")
    
    # NEW: Let the user choose the type of physics graph
    st.write("##### ⚙️ Graph Settings")
    graph_type = st.radio(
        "Select the curve fit for your practical:", 
        ["Linear Fit (Straight line of best fit)", "Smooth Curve (Locally weighted fit)", "Connect Points (Raw data)"],
        horizontal=True
    )
    
    st.divider()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Enter Readings")
        st.info("Enter up to 20 readings. Empty rows will be ignored.")
        initial_data = pd.DataFrame({"X-Axis": [None]*20, "Y-Axis": [None]*20})
        edited_df = st.data_editor(initial_data, num_rows="fixed", use_container_width=True)
        
    with col2:
        st.subheader("Live Graph")
        clean_df = edited_df.dropna(subset=["X-Axis", "Y-Axis"])
        
        if not clean_df.empty:
            clean_df = clean_df.astype(float)
            
            # Sort values by X-axis so "Connect Points" doesn't draw chaotic spaghetti lines
            clean_df = clean_df.sort_values(by="X-Axis")
            
            if len(clean_df) > 1:
                if graph_type == "Linear Fit (Straight line of best fit)":
                    # Draws dots + a straight mathematical line of best fit (OLS)
                    fig = px.scatter(clean_df, x="X-Axis", y="Y-Axis", title="X vs Y Readings", trendline="ols")
                    fig.update_traces(mode='markers', marker=dict(size=8))
                    
                elif graph_type == "Smooth Curve (Locally weighted fit)":
                    # Draws dots + a smooth, curved trendline (LOWESS)
                    fig = px.scatter(clean_df, x="X-Axis", y="Y-Axis", title="X vs Y Readings", trendline="lowess")
                    fig.update_traces(mode='markers', marker=dict(size=8))
                    
                else:
                    # Just connects the raw data points directly
                    fig = px.scatter(clean_df, x="X-Axis", y="Y-Axis", title="X vs Y Readings")
                    fig.update_traces(mode='lines+markers', marker=dict(size=8))
            else:
                # If only 1 point is entered, just show the point
                fig = px.scatter(clean_df, x="X-Axis", y="Y-Axis", title="X vs Y Readings")
                fig.update_traces(mode='markers', marker=dict(size=8))
                
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Enter at least one valid X and Y reading to see the graph.")

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
