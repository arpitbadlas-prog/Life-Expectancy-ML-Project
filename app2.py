import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Life Expectancy Dashboard", layout="wide", initial_sidebar_state="expanded")

# Modern CSS styling
st.markdown("""
    <style>
        /* Main container */
        [data-testid="stMainBlockContainer"] {
            padding-top: 0;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            color: white;
        }
        
        .header-title {
            font-size: 2.5em;
            font-weight: 700;
            margin: 0;
        }
        
        .header-subtitle {
            font-size: 1.1em;
            opacity: 0.9;
            margin: 10px 0 0 0;
        }
        
        /* Card styling */
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        
        /* Divider */
        hr {
            margin: 30px 0;
            border: none;
            border-top: 2px solid #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

def find_data_file(filename="Life Expectancy Data.csv"):
    candidates = [
        Path(__file__).resolve().parent.parent / filename,
        Path(__file__).resolve().parent / filename,
        Path.cwd() / filename,
    ]
    for c in candidates:
        if c.exists():
            return c
    for p in Path(__file__).resolve().parent.parent.rglob(filename):
        return p
    return None

DATA_PATH = find_data_file()
if DATA_PATH is None:
    st.error("❌ Dataset not found. Please place 'Life Expectancy Data.csv' in the project root.")
    st.stop()

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df

# Country flag mapping
country_flags = {
    'Afghanistan': '🇦🇫', 'Albania': '🇦🇱', 'Algeria': '🇩🇿', 'Andorra': '🇦🇩', 'Angola': '🇦🇴',
    'Antigua and Barbuda': '🇦🇬', 'Argentina': '🇦🇷', 'Armenia': '🇦🇲', 'Australia': '🇦🇺', 'Austria': '🇦🇹',
    'Azerbaijan': '🇦🇿', 'Bahamas': '🇧🇸', 'Bahrain': '🇧🇭', 'Bangladesh': '🇧🇩', 'Barbados': '🇧🇧',
    'Belarus': '🇧🇾', 'Belgium': '🇧🇪', 'Belize': '🇧🇿', 'Benin': '🇧🇯', 'Bhutan': '🇧🇹',
    'Bolivia': '🇧🇴', 'Bosnia and Herzegovina': '🇧🇦', 'Botswana': '🇧🇼', 'Brazil': '🇧🇷', 'Brunei': '🇧🇳',
    'Bulgaria': '🇧🇬', 'Burkina Faso': '🇧🇫', 'Burundi': '🇧🇮', 'Cambodia': '🇰🇭', 'Cameroon': '🇨🇲',
    'Canada': '🇨🇦', 'Cape Verde': '🇨🇻', 'Central African Republic': '🇨🇫', 'Chad': '🇹🇩', 'Chile': '🇨🇱',
    'China': '🇨🇳', 'Colombia': '🇨🇴', 'Comoros': '🇰🇲', 'Congo': '🇨🇬', 'Costa Rica': '🇨🇷',
    'Croatia': '🇭🇷', 'Cuba': '🇨🇺', 'Cyprus': '🇨🇾', 'Czech Republic': '🇨🇿', 'Czechia': '🇨🇿', 'Denmark': '🇩🇰',
    'Djibouti': '🇩🇯', 'Dominica': '🇩🇲', 'Dominican Republic': '🇩🇴', 'Ecuador': '🇪🇨', 'Egypt': '🇪🇬',
    'El Salvador': '🇸🇻', 'Equatorial Guinea': '🇬🇶', 'Eritrea': '🇪🇷', 'Estonia': '🇪🇪', 'Ethiopia': '🇪🇹',
    'Fiji': '🇫🇯', 'Finland': '🇫🇮', 'France': '🇫🇷', 'Gabon': '🇬🇦', 'Gambia': '🇬🇲',
    'Georgia': '🇬🇪', 'Germany': '🇩🇪', 'Ghana': '🇬🇭', 'Greece': '🇬🇷', 'Grenada': '🇬🇩',
    'Guatemala': '🇬🇹', 'Guinea': '🇬🇳', 'Guinea-Bissau': '🇬🇼', 'Guyana': '🇬🇾', 'Haiti': '🇭🇹',
    'Honduras': '🇭🇳', 'Hungary': '🇭🇺', 'Iceland': '🇮🇸', 'India': '🇮🇳', 'Indonesia': '🇮🇩',
    'Iran': '🇮🇷', 'Iraq': '🇮🇶', 'Ireland': '🇮🇪', 'Israel': '🇮🇱', 'Italy': '🇮🇹',
    'Jamaica': '🇯🇲', 'Japan': '🇯🇵', 'Jordan': '🇯🇴', 'Kazakhstan': '🇰🇿', 'Kenya': '🇰🇪',
    'Kiribati': '🇰🇮', 'Korea': '🇰🇷', 'Kosovo': '🇽🇰', 'Kuwait': '🇰🇼', 'Kyrgyzstan': '🇰🇬',
    'Laos': '🇱🇦', 'Latvia': '🇱🇻', 'Lebanon': '🇱🇧', 'Lesotho': '🇱🇸', 'Liberia': '🇱🇷',
    'Libya': '🇱🇾', 'Liechtenstein': '🇱🇮', 'Lithuania': '🇱🇹', 'Luxembourg': '🇱🇺', 'Madagascar': '🇲🇬',
    'Malawi': '🇲🇼', 'Malaysia': '🇲🇾', 'Maldives': '🇲🇻', 'Mali': '🇲🇱', 'Malta': '🇲🇹',
    'Marshall Islands': '🇲🇭', 'Mauritania': '🇲🇷', 'Mauritius': '🇲🇺', 'Mexico': '🇲🇽', 'Micronesia': '🇫🇲',
    'Moldova': '🇲🇩', 'Monaco': '🇲🇨', 'Mongolia': '🇲🇳', 'Montenegro': '🇲🇪', 'Morocco': '🇲🇦',
    'Mozambique': '🇲🇿', 'Myanmar': '🇲🇲', 'Namibia': '🇳🇦', 'Nauru': '🇳🇷', 'Nepal': '🇳🇵',
    'Netherlands': '🇳🇱', 'New Zealand': '🇳🇿', 'Nicaragua': '🇳🇮', 'Niger': '🇳🇪', 'Nigeria': '🇳🇬',
    'Norway': '🇳🇴', 'Oman': '🇴🇲', 'Pakistan': '🇵🇰', 'Palau': '🇵🇼', 'Palestine': '🇵🇸',
    'Panama': '🇵🇦', 'Papua New Guinea': '🇵🇬', 'Paraguay': '🇵🇾', 'Peru': '🇵🇪', 'Philippines': '🇵🇭',
    'Poland': '🇵🇱', 'Portugal': '🇵🇹', 'Qatar': '🇶🇦', 'Romania': '🇷🇴', 'Russian Federation': '🇷🇺', 'Russia': '🇷🇺',
    'Rwanda': '🇷🇼', 'Saint Kitts and Nevis': '🇰🇳', 'Saint Lucia': '🇱🇨', 'Saint Vincent and the Grenadines': '🇻🇨',
    'Samoa': '🇼🇸', 'San Marino': '🇸🇲', 'Sao Tome and Principe': '🇸🇹', 'Saudi Arabia': '🇸🇦', 'Senegal': '🇸🇳',
    'Serbia': '🇷🇸', 'Seychelles': '🇸🇨', 'Sierra Leone': '🇸🇱', 'Singapore': '🇸🇬', 'Slovakia': '🇸🇰',
    'Slovenia': '🇸🇮', 'Solomon Islands': '🇸🇧', 'Somalia': '🇸🇴', 'South Africa': '🇿🇦', 'South Sudan': '🇸🇸',
    'Spain': '🇪🇸', 'Sri Lanka': '🇱🇰', 'Sudan': '🇸🇩', 'Suriname': '🇸🇷', 'Sweden': '🇸🇪',
    'Switzerland': '🇨🇭', 'Syrian Arab Republic': '🇸🇾', 'Syria': '🇸🇾', 'Tajikistan': '🇹🇯', 'Thailand': '🇹🇭',
    'Timor-Leste': '🇹🇱', 'Togo': '🇹🇬', 'Tonga': '🇹🇴', 'Trinidad and Tobago': '🇹🇹', 'Tunisia': '🇹🇳',
    'Turkey': '🇹🇷', 'Turkmenistan': '🇹🇲', 'Tuvalu': '🇹🇻', 'Uganda': '🇺🇬', 'Ukraine': '🇺🇦',
    'United Arab Emirates': '🇦🇪', 'United Kingdom': '🇬🇧', 'United Republic of Tanzania': '🇹🇿', 'Tanzania': '🇹🇿',
    'United States': '🇺🇸', 'USA': '🇺🇸', 'Uruguay': '🇺🇾', 'Uzbekistan': '🇺🇿', 'Vanuatu': '🇻🇺',
    'Venezuela': '🇻🇪', 'Vietnam': '🇻🇳', 'Yemen': '🇾🇪', 'Zambia': '🇿🇲', 'Zimbabwe': '🇿🇼'
}

def get_flag(country):
    return country_flags.get(country, '🌍')

df = load_data(DATA_PATH)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📊 Life Expectancy Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Add small decorative images
col_img1, col_img2, col_img3 = st.columns(3)
with col_img1:
    st.markdown('<div style="text-align: center;"><span style="font-size: 3em;">🏥</span></div>', unsafe_allow_html=True)
with col_img2:
    st.markdown('<div style="text-align: center;"><span style="font-size: 3em;">🌍</span></div>', unsafe_allow_html=True)
with col_img3:
    st.markdown('<div style="text-align: center;"><span style="font-size: 3em;">❤️</span></div>', unsafe_allow_html=True)

# Sidebar filters
# Year filter with slider
years = sorted(df['Year'].dropna().unique()) if 'Year' in df.columns else []
if years:
    selected_year = st.sidebar.slider("📅 Select Year", min_value=int(min(years)), max_value=int(max(years)), value=int(max(years)))
else:
    selected_year = None

# Country filter
countries = sorted(df['Country'].dropna().unique()) if 'Country' in df.columns else []
selected_countries = st.sidebar.multiselect("🌍 Select Countries", countries, default=countries[:5] if countries else [])

# Apply filters
filtered = df.copy()

if selected_year is not None:
    filtered = filtered[filtered['Year'] == selected_year]

if selected_countries:
    filtered = filtered[filtered['Country'].isin(selected_countries)]

# Main content
if filtered.empty:
    st.warning("⚠️ No data matches your selection. Please adjust the filters.")
else:
    # Life Expectancy visualization
    st.markdown("### Life Expectancy Analysis")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Life Expectancy line graph by country for selected year
        if len(selected_countries) > 0 and selected_year:
            country_life_exp = filtered.groupby('Country')['Life expectancy'].mean().sort_values(ascending=False)
            country_with_flags = [f"{get_flag(country)} {country}" for country in country_life_exp.index]
            fig1 = px.line(
                x=country_with_flags,
                y=country_life_exp.values,
                markers=True,
                title=f"Life Expectancy by Country ({selected_year})",
                labels={'x': 'Country', 'y': 'Life Expectancy (years)'}
            )
            fig1.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=8))
            fig1.update_layout(
                template="plotly_white",
                height=450,
                hovermode='x unified',
                showlegend=False,
                xaxis_title="Country",
                yaxis_title="Life Expectancy (years)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Life Expectancy trend line over years for selected countries
        if len(selected_countries) > 0:
            trend_data = df[df['Country'].isin(selected_countries)].groupby(['Year', 'Country'])['Life expectancy'].mean().reset_index()
            fig2 = px.line(
                trend_data,
                x='Year',
                y='Life expectancy',
                color='Country',
                markers=True,
                title="Life Expectancy Trend Over Years",
                labels={'Life expectancy': 'Life Expectancy (years)', 'Year': 'Year'}
            )
            fig2.update_layout(
                template="plotly_white",
                height=450,
                hovermode='x unified',
                yaxis_title="Life Expectancy (years)",
                xaxis_title="Year"
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Summary stats in a clean layout
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">📈 Average Life Expectancy</h3>
                <p style="font-size: 2em; font-weight: 700; margin: 10px 0 0 0; color: #333;">
                    {:.1f} years
                </p>
            </div>
        """.format(filtered['Life expectancy'].mean()), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">🌍 Countries Selected</h3>
                <p style="font-size: 2em; font-weight: 700; margin: 10px 0 0 0; color: #333;">
                    {len(selected_countries)}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">📊 Total Records</h3>
                <p style="font-size: 2em; font-weight: 700; margin: 10px 0 0 0; color: #333;">
                    {len(filtered):,}
                </p>
            </div>
        """, unsafe_allow_html=True)

