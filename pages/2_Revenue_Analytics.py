import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Revenue Analytics", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .page-title { font-size: 2rem; font-weight: 800; color: #232F3E; border-bottom: 3px solid #FF9900; padding-bottom: 10px; }
    .section-title { font-size: 1.3rem; font-weight: 700; color: #FF9900; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('combined.csv', low_memory=False)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.markdown('<p class="page-title">💰 Revenue Analytics Dashboard</p>', unsafe_allow_html=True)

# ============================================================
# Q6 - Revenue Trend Analysis
# ============================================================
st.markdown('<p class="section-title">Q6 — Revenue Trend Analysis</p>', unsafe_allow_html=True)

# filter by year
years = sorted(df['order_year'].unique())
selected_years = st.multiselect('Select Years', years, default=years)
filtered = df[df['order_year'].isin(selected_years)]

col1, col2 = st.columns(2)
with col1:
    # monthly revenue trend
    monthly = filtered.groupby(['order_year', 'order_month'])['final_amount_inr'].sum().reset_index()
    pivot = monthly.pivot(index='order_month', columns='order_year', values='final_amount_inr')/1e6
    fig, ax = plt.subplots(figsize=(8, 4))
    pivot.plot(ax=ax, marker='o', linewidth=1.5)
    ax.set_title('Monthly Revenue by Year', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (₹ Million)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    ax.legend(title='Year', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # quarterly revenue
    quarterly = filtered.groupby(['order_year', 'order_quarter'])['final_amount_inr'].sum().reset_index()
    quarterly_pivot = quarterly.pivot(index='order_year', columns='order_quarter', values='final_amount_inr')/1e9
    quarterly_pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    fig, ax = plt.subplots(figsize=(8, 4))
    quarterly_pivot.plot(kind='bar', ax=ax, colormap='Set2')
    ax.set_title('Quarterly Revenue by Year', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Quarter')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q7 - Category Performance
# ============================================================
st.markdown('<p class="section-title">Q7 — Category Performance</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    subcat_revenue = df.groupby('subcategory')['final_amount_inr'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_revenue.plot(kind='barh', ax=ax, color='#FF9900')
    ax.set_title('Top 10 Subcategories by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # subcategory growth over years
    subcat_yearly = df.groupby(['order_year', 'subcategory'])['final_amount_inr'].sum().reset_index()
    top_subcats = subcat_revenue.head(5).index.tolist()
    subcat_top = subcat_yearly[subcat_yearly['subcategory'].isin(top_subcats)]
    subcat_pivot = subcat_top.pivot(index='order_year', columns='subcategory', values='final_amount_inr')/1e9
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_pivot.plot(ax=ax, marker='o', linewidth=2)
    ax.set_title('Top 5 Subcategory Revenue Trends', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q8 - Geographic Revenue Analysis
# ============================================================
st.markdown('<p class="section-title">Q8 — Geographic Revenue Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    city_revenue = df.groupby('customer_city')['final_amount_inr'].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 6))
    city_revenue.plot(kind='barh', ax=ax, color='#232F3E')
    ax.set_title('Top 15 Cities by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    state_revenue = df.groupby('customer_state')['final_amount_inr'].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 6))
    state_revenue.plot(kind='barh', ax=ax, color='#FF9900')
    ax.set_title('Top 15 States by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# tier wise
tier_revenue = df.groupby(['order_year', 'customer_tier'])['final_amount_inr'].sum().reset_index()
tier_pivot = tier_revenue.pivot(index='order_year', columns='customer_tier', values='final_amount_inr')/1e9
fig, ax = plt.subplots(figsize=(12, 4))
tier_pivot.plot(kind='area', ax=ax, alpha=0.7, colormap='Set1')
ax.set_title('Revenue by Customer Tier Over Years', fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Revenue (₹ Billion)')
ax.legend(title='Tier')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q9 - Festival Sales Analytics
# ============================================================
st.markdown('<p class="section-title">Q9 — Festival Sales Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    festival_revenue = df.groupby('festival_name').agg(
        total_revenue=('final_amount_inr', 'sum'),
        avg_order=('final_amount_inr', 'mean'),
        orders=('transaction_id', 'count')
    ).reset_index().sort_values('total_revenue', ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#e74c3c' if f != 'No Festival' else '#95a5a6' for f in festival_revenue['festival_name']]
    ax.barh(festival_revenue['festival_name'], festival_revenue['total_revenue']/1e9, color=colors)
    ax.set_title('Total Revenue by Festival', fontweight='bold')
    ax.set_xlabel('Revenue (₹ Billion)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    festival_only = festival_revenue[festival_revenue['festival_name'] != 'No Festival']
    no_festival_avg = festival_revenue[festival_revenue['festival_name'] == 'No Festival']['avg_order'].values[0]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(festival_only['festival_name'], festival_only['avg_order'], color='#FF9900')
    ax.axhline(y=no_festival_avg, color='red', linestyle='--', linewidth=2, label=f'No Festival Avg: ₹{no_festival_avg:.0f}')
    ax.set_title('Avg Order Value: Festival vs Non-Festival', fontweight='bold')
    ax.set_xlabel('Festival')
    ax.set_ylabel('Avg Order Value (₹)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q10 - Price Optimization
# ============================================================
st.markdown('<p class="section-title">Q10 — Price Optimization</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # discount vs revenue
    discount_bins = pd.cut(df['discount_percent'], bins=[0, 10, 20, 30, 40, 50, 100],
                          labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])
    discount_analysis = df.groupby(discount_bins, observed=True).agg(
        revenue=('final_amount_inr', 'sum'),
        orders=('transaction_id', 'count')
    ).reset_index()
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax2 = ax1.twinx()
    ax1.bar(discount_analysis['discount_percent'], discount_analysis['revenue']/1e9, color='#FF9900', alpha=0.7, label='Revenue')
    ax2.plot(discount_analysis['discount_percent'], discount_analysis['orders'], 'o-', color='#232F3E', linewidth=2, label='Orders')
    ax1.set_title('Discount Impact on Revenue & Orders', fontweight='bold')
    ax1.set_xlabel('Discount Range')
    ax1.set_ylabel('Revenue (₹ Billion)', color='#FF9900')
    ax2.set_ylabel('Number of Orders', color='#232F3E')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # price distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df['discounted_price_inr'], bins=50, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Price Distribution of Products', fontweight='bold')
    ax.set_xlabel('Discounted Price (₹)')
    ax.set_ylabel('Frequency')
    ax.axvline(df['discounted_price_inr'].median(), color='red', linestyle='--', label=f"Median: ₹{df['discounted_price_inr'].median():,.0f}")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.caption("💰 Revenue Analytics Dashboard | Amazon India Sales Analytics")
