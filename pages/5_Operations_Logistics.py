import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Operations & Logistics", page_icon="🚚", layout="wide")

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

st.markdown('<p class="page-title">🚚 Operations & Logistics Dashboard</p>', unsafe_allow_html=True)

# ============================================================
# Q21 - Delivery Performance
# ============================================================
st.markdown('<p class="section-title">Q21 — Delivery Performance</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    avg_delivery = df['delivery_days'].mean()
    st.metric("Avg Delivery Days", f"{avg_delivery:.1f} days")
with col2:
    same_day = (df['delivery_days'] == 0).sum()
    st.metric("Same Day Deliveries", f"{same_day:,}")
with col3:
    express = (df['delivery_days'] <= 1).sum()
    st.metric("Express Deliveries (≤1 day)", f"{express:,}")

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df['delivery_days'], bins=20, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Delivery Days Distribution', fontweight='bold')
    ax.set_xlabel('Delivery Days')
    ax.set_ylabel('Frequency')
    ax.axvline(df['delivery_days'].mean(), color='red', linestyle='--',
               label=f"Mean: {df['delivery_days'].mean():.1f} days")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    delivery_type = df['delivery_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(delivery_type, labels=delivery_type.index, autopct='%1.1f%%',
           colors=['#FF9900', '#232F3E', '#2ecc71'])
    ax.set_title('Delivery Type Distribution', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# delivery days by city
city_delivery = df.groupby('customer_city')['delivery_days'].mean().sort_values(ascending=False).head(15)
fig, ax = plt.subplots(figsize=(12, 4))
city_delivery.plot(kind='bar', ax=ax, color='#FF9900')
ax.set_title('Avg Delivery Days by City', fontweight='bold')
ax.set_xlabel('City')
ax.set_ylabel('Avg Delivery Days')
ax.tick_params(axis='x', rotation=45)
ax.axhline(y=df['delivery_days'].mean(), color='red', linestyle='--', label='Overall Avg')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

# delivery days vs rating
col1, col2 = st.columns(2)
with col1:
    delivery_rating = df.groupby('delivery_days').agg(
        avg_rating=('customer_rating', 'mean'),
        orders=('transaction_id', 'count')
    ).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(delivery_rating['delivery_days'], delivery_rating['avg_rating'],
               s=delivery_rating['orders']/100, alpha=0.6, color='#FF9900')
    ax.set_title('Delivery Days vs Customer Rating', fontweight='bold')
    ax.set_xlabel('Delivery Days')
    ax.set_ylabel('Avg Customer Rating')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    tier_delivery = df.groupby('customer_tier')['delivery_days'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(tier_delivery.index, tier_delivery.values, color=['#FF9900', '#232F3E', '#2ecc71', '#e74c3c'])
    ax.set_title('Avg Delivery Days by Customer Tier', fontweight='bold')
    ax.set_xlabel('Customer Tier')
    ax.set_ylabel('Avg Delivery Days')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q22 - Payment Analytics
# ============================================================
st.markdown('<p class="section-title">Q22 — Payment Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    payment_counts = df['payment_method'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%',
           colors=['#FF9900', '#232F3E', '#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f39c12'])
    ax.set_title('Payment Method Distribution', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    payment_yearly = df.groupby(['order_year', 'payment_method'])['transaction_id'].count().reset_index()
    payment_pivot = payment_yearly.pivot(index='order_year', columns='payment_method', values='transaction_id')
    payment_pct = payment_pivot.divide(payment_pivot.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    payment_pct.plot(kind='area', ax=ax, alpha=0.7, colormap='Set2', stacked=True)
    ax.set_title('Payment Method Evolution (2015-2025)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Market Share (%)')
    ax.legend(title='Payment Method', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# payment method avg order value
payment_avg = df.groupby('payment_method')['final_amount_inr'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 3))
ax.bar(payment_avg.index, payment_avg.values, color='#FF9900')
ax.set_title('Avg Order Value by Payment Method', fontweight='bold')
ax.set_xlabel('Payment Method')
ax.set_ylabel('Avg Order Value (₹)')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q23 - Return & Cancellation
# ============================================================
st.markdown('<p class="section-title">Q23 — Return & Cancellation Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    return_status = df['return_status'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(return_status, labels=return_status.index, autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c', '#f39c12'])
    ax.set_title('Return Status Distribution', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    return_by_subcat = df.groupby(['subcategory', 'return_status'])['transaction_id'].count().reset_index()
    return_pivot = return_by_subcat.pivot(index='subcategory', columns='return_status', values='transaction_id').fillna(0)
    if 'Returned' in return_pivot.columns:
        return_pivot['return_rate'] = return_pivot['Returned'] / return_pivot.sum(axis=1) * 100
        top_return = return_pivot['return_rate'].sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        top_return.plot(kind='barh', ax=ax, color='#e74c3c')
        ax.set_title('Return Rate by Subcategory (%)', fontweight='bold')
        ax.set_xlabel('Return Rate (%)')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Return status data not available for detailed analysis")

st.markdown("---")

# ============================================================
# Q24 - Customer Service
# ============================================================
st.markdown('<p class="section-title">Q24 — Customer Service Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # customer rating distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df['customer_rating'], bins=20, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Customer Rating Distribution', fontweight='bold')
    ax.set_xlabel('Customer Rating')
    ax.set_ylabel('Frequency')
    ax.axvline(df['customer_rating'].mean(), color='red', linestyle='--',
               label=f"Mean: {df['customer_rating'].mean():.2f}")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # customer rating by city
    city_rating = df.groupby('customer_city')['customer_rating'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    city_rating.plot(kind='barh', ax=ax, color='#232F3E')
    ax.set_title('Avg Customer Rating by City', fontweight='bold')
    ax.set_xlabel('Avg Rating')
    ax.axvline(df['customer_rating'].mean(), color='red', linestyle='--', label='Overall Avg')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q25 - Supply Chain
# ============================================================
st.markdown('<p class="section-title">Q25 — Supply Chain Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # brand delivery performance
    brand_delivery = df.groupby('brand')['delivery_days'].mean().sort_values().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    brand_delivery.plot(kind='barh', ax=ax, color='#2ecc71')
    ax.set_title('Top 10 Brands - Fastest Delivery', fontweight='bold')
    ax.set_xlabel('Avg Delivery Days')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # subcategory delivery days
    subcat_delivery = df.groupby('subcategory')['delivery_days'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_delivery.plot(kind='barh', ax=ax, color='#e74c3c')
    ax.set_title('Subcategories with Longest Delivery', fontweight='bold')
    ax.set_xlabel('Avg Delivery Days')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.caption("🚚 Operations & Logistics Dashboard | Amazon India Sales Analytics")
