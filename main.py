import streamlit as st
from streamlit.components.v1 import html

# Custom CSS for modern styling
st.markdown("""
    <style>
        :root {
            --primary: #2E86C1;
            --secondary: #85C1E9;
            --background: #F8F9F9;
        }
        
        .stApp {
            background: var(--background);
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            color: var(--primary);
            border-bottom: 3px solid var(--secondary);
            padding-bottom: 10px;
        }
        
        .stButton>button {
            background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            padding: 10px 20px;
            font-size: 1rem;
            border-radius: 8px;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(46, 134, 193, 0.4);
        }
        
        .result-box {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 2rem 0;
            text-align: center;
        }
        
        .history-item {
            padding: 1rem;
            margin: 0.5rem 0;
            background: #EBF5FB;
            border-radius: 5px;
        }
        
        footer {
            text-align: center;
            padding: 1rem;
            color: #666;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Font Awesome Icons
icons = {
    "Length": "📏",
    "Temperature": "🌡️",
    "Weight": "⚖️",
    "Volume": "🧴",
    "Area": "📐"
}

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Title with icon
st.markdown(f"<h1>📐 Universal Unit Converter Pro</h1>", unsafe_allow_html=True)
st.markdown("""
    *Your all-in-one solution for accurate unit conversions across various measurement systems.*
""")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    conversion_type = st.selectbox(
        "Conversion Type",
        list(icons.keys()),
        format_func=lambda x: f"{icons[x]} {x}"
    )
    
    unit_options = {
        "Length": ["Meters", "Kilometers", "Miles", "Feet", "Yards", "Inches", "Centimeters", "Millimeters"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
        "Weight": ["Kilograms", "Grams", "Pounds", "Ounces", "Stones", "Metric Tons"],
        "Volume": ["Liters", "Milliliters", "Cups", "Pints", "Gallons", "Tablespoons", "Teaspoons"],
        "Area": ["Square meters", "Square kilometers", "Square miles", "Square feet", "Square yards", "Hectares", "Acres"]
    }
    
    from_unit = st.selectbox("From Unit", unit_options[conversion_type])
    to_unit = st.selectbox("To Unit", unit_options[conversion_type])
    value = st.number_input("Enter Value", min_value=0.0, value=1.0, step=0.1)
    precision = st.slider("Decimal Precision", 0, 6, 2)

# Conversion function
def convert(value, from_unit, to_unit, conv_type):
    conversion_factors = {
        "Length": {
            "Meters": 1, "Kilometers": 1000, "Miles": 1609.344, "Feet": 0.3048,
            "Yards": 0.9144, "Inches": 0.0254, "Centimeters": 0.01, "Millimeters": 0.001
        },
        "Temperature": {
            "Celsius": lambda v, t: (v * 9/5) + 32 if t == "Fahrenheit" else v + 273.15,
            "Fahrenheit": lambda v, t: (v - 32) * 5/9 if t == "Celsius" else (v - 32) * 5/9 + 273.15,
            "Kelvin": lambda v, t: v - 273.15 if t == "Celsius" else (v - 273.15) * 9/5 + 32
        },
        "Weight": {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495, "Stones": 6.35029, "Metric Tons": 1000},
        "Volume": {"Liters": 1, "Milliliters": 0.001, "Cups": 0.236588, "Pints": 0.473176, "Gallons": 3.78541, "Tablespoons": 0.0147868, "Teaspoons": 0.00492892},
        "Area": {"Square meters": 1, "Square kilometers": 1e6, "Square miles": 2589988, "Square feet": 0.092903, "Square yards": 0.836127, "Hectares": 10000, "Acres": 4046.86}
    }
    
    if conv_type == "Temperature":
        return conversion_factors[conv_type][from_unit](value, to_unit)
    return value * conversion_factors[conv_type][from_unit] / conversion_factors[conv_type][to_unit]

if st.button("🚀 Convert"):
    result = convert(value, from_unit, to_unit, conversion_type)
    st.session_state.history.insert(0, f"{value} {from_unit} → {result:.{precision}f} {to_unit}")
    
    st.markdown(f"""
    <div class="result-box">
        <h3>🎯 Conversion Result</h3>
        <p style="font-size: 1.5rem;"><strong>{result:.{precision}f}</strong> {to_unit}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📜 Conversion History"):
        for item in st.session_state.history[:5]:
            st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

st.markdown("""
    <footer>
        <p>Developed by Shahzaib Ali | <a href="https://github.com/Shahzaib-68">GitHub</a> | <a href="https://www.linkedin.com/in/shahzaib-ali-99-frontend-developer/">LinkedIn</a></p>
    </footer>
""", unsafe_allow_html=True)
html('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
