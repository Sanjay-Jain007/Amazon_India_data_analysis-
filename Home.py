import streamlit as st

st.set_page_config(
    page_title="Amazon India Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .title { font-size: 3rem; font-weight: 800; color: #FF9900; text-align: center; }
    .subtitle { font-size: 1.2rem; color: #232F3E; text-align: center; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #FF9900; }
    .metric-label { font-size: 0.9rem; color: #666; }
    .section-header { font-size: 1.5rem; font-weight: 700; color: #232F3E; border-left: 4px solid #FF9900; padding-left: 10px; }
    </style>
""", unsafe_allow_html=True)

# header
st.markdown('<p class="title">🛒 Amazon India Sales Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">A Decade of E-Commerce Intelligence | 2015-2025</p>', unsafe_allow_html=True)
st.markdown("---")

# about amazon india
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<p class="section-header">About Amazon India</p>', unsafe_allow_html=True)
    st.markdown("""
    Amazon India launched in **June 2013** and has grown to become one of India's largest e-commerce platforms. 
    Over the past decade, it has transformed the way Indians shop online — from metros to rural areas.
    
    **Key Milestones:**
    - 🚀 **2013** — Amazon India launched with 10,000+ products
    - 📦 **2015** — Introduced Prime membership in India
    - 🎉 **2016** — First Great Indian Festival sale crossed ₹1,000 Crore
    - 📱 **2018** — Reached 100 million registered users
    - 🌍 **2020** — COVID-19 drove unprecedented online shopping growth
    - 💡 **2023** — Expanded to 100+ cities across India
    - 🏆 **2025** — Serving 500+ million customers across India
    """)

with col2:
    st.markdown('<p class="section-header">Dataset Overview</p>', unsafe_allow_html=True)
    st.markdown("""
    📊 **Total Transactions:** 1.1 Million+
    
    📅 **Time Period:** 2015-2025
    
    🏙️ **Cities Covered:** 30+
    
    📦 **Products:** 2000+
    
    🏷️ **Brands:** 100+
    
    🗂️ **Categories:** 8 Major
    """)

st.markdown("---")

# key metrics
st.markdown('<p class="section-header">Platform Highlights</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">₹79B+</div>
        <div class="metric-label">Total Revenue (2015-2025)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">354K+</div>
        <div class="metric-label">Unique Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">1.1M+</div>
        <div class="metric-label">Total Transactions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">₹64K</div>
        <div class="metric-label">Avg Order Value</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# dashboard sections
st.markdown('<p class="section-header">Dashboard Sections</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📊 Executive Strategy**
    - Executive Summary
    - Business Performance
    - Strategic Overview
    - Financial Performance
    - Growth Analytics
    """)

    st.success("""
    **👥 Customer Analytics**
    - Customer Segmentation (RFM)
    - Customer Journey
    - Prime Membership
    - Customer Retention
    - Demographics & Behavior
    """)

with col2:
    st.warning("""
    **💰 Revenue Analytics**
    - Revenue Trends
    - Category Performance
    - Geographic Revenue
    - Festival Sales
    - Price Optimization
    """)

    st.error("""
    **📦 Product & Inventory**
    - Product Performance
    - Brand Analytics
    - Inventory Optimization
    - Product Ratings
    - New Product Launch
    """)

with col3:
    st.info("""
    **🚚 Operations & Logistics**
    - Delivery Performance
    - Payment Analytics
    - Returns & Cancellations
    - Customer Service
    - Supply Chain
    """)

    st.success("""
    **🔮 Advanced Analytics**
    - Predictive Analytics
    - Market Intelligence
    - Cross-selling & Upselling
    - Seasonal Planning
    - BI Command Center
    """)

st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#666;'>
Built with ❤️ using Python, Streamlit, MySQL | GUVI x HCL Project | Amazon India: A Decade of Sales Analytics
</p>
""", unsafe_allow_html=True)
