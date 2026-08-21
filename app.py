
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Lab Master", layout="wide", page_icon="🔬")
st.title("🔬 Lab Master")
st.markdown("**By Deep Patel** | *B.Sc. Physics Lab Companion*")
st.divider()

# 2. Create Tabs for organization
tab1, tab2, tab3 = st.tabs(["📊 Data & Graphing", "🔄 Unit Converter", "⚛️ Physics Constants"])

# --- TAB 1: GRAPHING ---
with tab1:
    st.header("Experimental Data Plotter")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Enter Readings")
        st.info("Enter up to 20 readings. Empty rows will be ignored.")
        # Create a dataframe with 20 empty rows
        initial_data = pd.DataFrame({"X-Axis": [None]*20, "Y-Axis": [None]*20})
        
        # Interactive data editor
        edited_df = st.data_editor(initial_data, num_rows="fixed", use_container_width=True)
        
    with col2:
        st.subheader("Live Graph")
        # Clean data: drop rows that don't have both X and Y values
        clean_df = edited_df.dropna(subset=["X-Axis", "Y-Axis"])
        
        if not clean_df.empty:
            # Convert inputs to float just in case
            clean_df = clean_df.astype(float)
            
            # Plot using Plotly for a smooth, professional look
            fig = px.scatter(clean_df, x="X-Axis", y="Y-Axis", 
                             title="X vs Y Readings",
                             trendline="ols") if len(clean_df) > 1 else px.scatter(clean_df, x="X-Axis", y="Y-Axis")
            
            fig.update_traces(mode='lines+markers', marker=dict(size=8))
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
        len_from = st.selectbox("From:", ["Meters", "Centimeters", "Millimeters", "Kilometers"], key="len_from")
        len_to = st.selectbox("To:", ["Meters", "Centimeters", "Millimeters", "Kilometers"], key="len_to")
        
        # Simple conversion logic using meters as base
        len_factors = {"Meters": 1, "Centimeters": 0.01, "Millimeters": 0.001, "Kilometers": 1000}
        result = (length_val * len_factors[len_from]) / len_factors[len_to]
        st.success(f"**Result:** {result} {len_to}")

    with col4:
        st.subheader("Mass")
        mass_val = st.number_input("Enter value:", value=1.0, key="mass_val")
        mass_from = st.selectbox("From:", ["Kilograms", "Grams", "Milligrams"], key="mass_from")
        mass_to = st.selectbox("To:", ["Kilograms", "Grams", "Milligrams"], key="mass_to")
        
        mass_factors = {"Kilograms": 1, "Grams": 0.001, "Milligrams": 0.000001}
        m_result = (mass_val * mass_factors[mass_from]) / mass_factors[mass_to]
        st.success(f"**Result:** {m_result} {mass_to}")

# --- TAB 3: CONSTANTS ---
with tab3:
    st.header("Standard Physics Constants")
    constants_data = {
        "Constant Name": [
            "Speed of Light in Vacuum (c)", 
            "Planck Constant (h)", 
            "Gravitational Constant (G)", 
            "Elementary Charge (e)", 
            "Electron Mass (m_e)", 
            "Proton Mass (m_p)",
            "Boltzmann Constant (k)",
            "Permittivity of Free Space (ε₀)"
        ],
        "Value": [
            "299,792,458", 
            "6.62607015 × 10⁻³⁴", 
            "6.67430 × 10⁻¹¹", 
            "1.602176634 × 10⁻¹⁹", 
            "9.1093837 × 10⁻³¹", 
            "1.67262192 × 10⁻²⁷",
            "1.380649 × 10⁻²³",
            "8.85418781 × 10⁻¹²"
        ],
        "Unit": [
            "m/s", "J·s", "m³/(kg·s²)", "C", "kg", "kg", "J/K", "F/m"
        ]
    }
    st.table(pd.DataFrame(constants_data))
