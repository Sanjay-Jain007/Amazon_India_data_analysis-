import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Executive Strategy", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .page-title { font-size: 2rem; font-weight: 800; color: #232F3E; border-bottom: 3px solid #FF9900; padding-bottom: 10px; }
    .section-title { font-size: 1.3rem; font-weight: 700; color: #FF9900; margin-top: 20px; }
    .metric-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #FF9900; }
    .metric-label { font-size: 0.85rem; color: #666; }
    </style>
""", unsafe_allow_html=True)

# load data
@st.cache_data
def load_data():
    df = pd.read_csv('combined.csv', low_memory=False)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.markdown('<p class="page-title">📊 Executive Strategy Dashboard</p>', unsafe_allow_html=True)
st.markdown("Comprehensive business intelligence for strategic decision making.")

# ============================================================
# Q1 - Executive Summary
# ============================================================
st.markdown('<p class="section-title">Q1 — Executive Summary</p>', unsafe_allow_html=True)

total_revenue = df['final_amount_inr'].sum()
total_customers = df['customer_id'].nunique()
total_orders = df['transaction_id'].nunique()
avg_order_value = df['final_amount_inr'].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">₹{total_revenue/1e9:.1f}B</div><div class="metric-label">Total Revenue</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_customers:,}</div><div class="metric-label">Unique Customers</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_orders:,}</div><div class="metric-label">Total Orders</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">₹{avg_order_value:,.0f}</div><div class="metric-label">Avg Order Value</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# yearly revenue with YoY growth
yearly = df.groupby('order_year')['final_amount_inr'].sum().reset_index()
yearly.columns = ['year', 'revenue']
yearly['yoy_growth'] = yearly['revenue'].pct_change() * 100

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(yearly['year'], yearly['revenue']/1e9, color='#FF9900', alpha=0.8)
    ax.set_title('Yearly Revenue (2015-2025)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(yearly['year'][1:], yearly['yoy_growth'][1:], 'o-', color='#232F3E', linewidth=2, markersize=8)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.fill_between(yearly['year'][1:], yearly['yoy_growth'][1:], 0,
                   where=yearly['yoy_growth'][1:] > 0, alpha=0.3, color='green')
    ax.fill_between(yearly['year'][1:], yearly['yoy_growth'][1:], 0,
                   where=yearly['yoy_growth'][1:] < 0, alpha=0.3, color='red')
    ax.set_title('Year-over-Year Growth Rate (%)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Growth (%)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q2 - Business Performance Monitor
# ============================================================
st.markdown('<p class="section-title">Q2 — Business Performance Monitor</p>', unsafe_allow_html=True)

# monthly performance
monthly = df.groupby(['order_year', 'order_month']).agg(
    revenue=('final_amount_inr', 'sum'),
    orders=('transaction_id', 'count'),
    customers=('customer_id', 'nunique')
).reset_index()

latest_year = monthly[monthly['order_year'] == monthly['order_year'].max()]
prev_year = monthly[monthly['order_year'] == monthly['order_year'].max() - 1]

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(latest_year['order_month'], latest_year['revenue']/1e6, 'o-', color='#FF9900', label='2025', linewidth=2)
    ax.plot(prev_year['order_month'], prev_year['revenue']/1e6, 'o--', color='#232F3E', label='2024', linewidth=2)
    ax.set_title('Monthly Revenue: 2024 vs 2025', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (₹ Million)')
    ax.legend()
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(latest_year['order_month'], latest_year['customers'], color='#FF9900', alpha=0.8)
    ax.set_title('Monthly Active Customers (2025)', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Active Customers')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q3 - Strategic Overview
# ============================================================
st.markdown('<p class="section-title">Q3 — Strategic Overview</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # city wise revenue
    city_revenue = df.groupby('customer_city')['final_amount_inr'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    city_revenue.plot(kind='barh', ax=ax, color='#FF9900')
    ax.set_title('Top 10 Cities by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # tier wise revenue
    tier_revenue = df.groupby('customer_tier')['final_amount_inr'].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(tier_revenue, labels=tier_revenue.index, autopct='%1.1f%%',
           colors=['#FF9900', '#232F3E', '#f39c12', '#2ecc71'])
    ax.set_title('Revenue by Customer Tier', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q4 - Financial Performance
# ============================================================
st.markdown('<p class="section-title">Q4 — Financial Performance</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # subcategory revenue
    subcat_revenue = df.groupby('subcategory')['final_amount_inr'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_revenue.plot(kind='bar', ax=ax, color='#FF9900')
    ax.set_title('Revenue by Subcategory', fontweight='bold')
    ax.set_xlabel('Subcategory')
    ax.set_ylabel('Revenue (₹)')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # discount analysis
    discount_bins = pd.cut(df['discount_percent'], bins=[0, 10, 20, 30, 40, 50, 100],
                          labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])
    discount_revenue = df.groupby(discount_bins, observed=True)['final_amount_inr'].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    discount_revenue.plot(kind='bar', ax=ax, color='#232F3E')
    ax.set_title('Revenue by Discount Range', fontweight='bold')
    ax.set_xlabel('Discount Range')
    ax.set_ylabel('Revenue (₹)')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q5 - Growth Analytics
# ============================================================
st.markdown('<p class="section-title">Q5 — Growth Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # customer growth
    customer_growth = df.groupby('order_year')['customer_id'].nunique().reset_index()
    customer_growth.columns = ['year', 'customers']
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(customer_growth['year'], customer_growth['customers'], 'o-', color='#FF9900', linewidth=2, markersize=8)
    ax.fill_between(customer_growth['year'], customer_growth['customers'], alpha=0.3, color='#FF9900')
    ax.set_title('Customer Growth (2015-2025)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Unique Customers')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # spending tier growth
    spending_tier = df.groupby(['order_year', 'customer_spending_tier'])['final_amount_inr'].sum().reset_index()
    spending_pivot = spending_tier.pivot(index='order_year', columns='customer_spending_tier', values='final_amount_inr')/1e9
    fig, ax = plt.subplots(figsize=(8, 4))
    spending_pivot.plot(kind='area', ax=ax, alpha=0.7, colormap='Set2')
    ax.set_title('Revenue by Spending Tier (2015-2025)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.legend(title='Spending Tier', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.caption("📊 Executive Strategy Dashboard | Amazon India Sales Analytics")
