import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.set_page_config(page_title="Product & Inventory", page_icon="📦", layout="wide")

st.markdown("""
    <style>
    .page-title { font-size: 2rem; font-weight: 800; color: #232F3E; border-bottom: 3px solid #FF9900; padding-bottom: 10px; }
    .section-title { font-size: 1.3rem; font-weight: 700; color: #FF9900; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'combined.csv'), low_memory=False)
    df['order_date'] = pd.to_datetime(df['order_date'])
    products = pd.read_csv(os.path.join(BASE_DIR, 'products.csv'), low_memory=False)
    return df, products

df, products = load_data()

st.markdown('<p class="page-title">📦 Product & Inventory Analytics Dashboard</p>', unsafe_allow_html=True)

# ============================================================
# Q16 - Product Performance
# ============================================================
st.markdown('<p class="section-title">Q16 — Product Performance</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # top products by revenue
    product_revenue = df.groupby('product_name')['final_amount_inr'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    product_revenue.plot(kind='barh', ax=ax, color='#FF9900')
    ax.set_title('Top 10 Products by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # top products by units sold
    product_units = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    product_units.plot(kind='barh', ax=ax, color='#232F3E')
    ax.set_title('Top 10 Products by Units Sold', fontweight='bold')
    ax.set_xlabel('Units Sold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# product rating vs revenue scatter
product_analysis = df.groupby('product_name').agg(
    revenue=('final_amount_inr', 'sum'),
    rating=('product_rating', 'mean'),
    units=('quantity', 'sum')
).reset_index()

fig, ax = plt.subplots(figsize=(12, 4))
scatter = ax.scatter(product_analysis['rating'], product_analysis['revenue']/1e6,
                    s=product_analysis['units']*2, alpha=0.5, c='#FF9900')
ax.set_title('Product Rating vs Revenue (bubble size = units sold)', fontweight='bold')
ax.set_xlabel('Avg Product Rating')
ax.set_ylabel('Revenue (₹ Million)')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q17 - Brand Analytics
# ============================================================
st.markdown('<p class="section-title">Q17 — Brand Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    brand_revenue = df.groupby('brand')['final_amount_inr'].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 6))
    brand_revenue.plot(kind='barh', ax=ax, color='#FF9900')
    ax.set_title('Top 15 Brands by Revenue', fontweight='bold')
    ax.set_xlabel('Revenue (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # brand market share
    top_brands = brand_revenue.head(8).index.tolist()
    brand_share = df[df['brand'].isin(top_brands)].groupby('brand')['final_amount_inr'].sum()
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(brand_share)))
    ax.pie(brand_share, labels=brand_share.index, autopct='%1.1f%%', colors=colors)
    ax.set_title('Top 8 Brands Market Share', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# brand trend over years
brand_yearly = df[df['brand'].isin(top_brands[:5])].groupby(['order_year', 'brand'])['final_amount_inr'].sum().reset_index()
brand_pivot = brand_yearly.pivot(index='order_year', columns='brand', values='final_amount_inr')/1e9
fig, ax = plt.subplots(figsize=(12, 4))
brand_pivot.plot(ax=ax, marker='o', linewidth=2)
ax.set_title('Top 5 Brand Revenue Trends (2015-2025)', fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Revenue (₹ Billion)')
ax.legend(title='Brand', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q18 - Inventory Optimization
# ============================================================
st.markdown('<p class="section-title">Q18 — Inventory Optimization</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # monthly demand patterns
    monthly_demand = df.groupby(['order_month', 'subcategory'])['quantity'].sum().reset_index()
    top_subcats = df.groupby('subcategory')['quantity'].sum().nlargest(5).index.tolist()
    monthly_top = monthly_demand[monthly_demand['subcategory'].isin(top_subcats)]
    demand_pivot = monthly_top.pivot(index='order_month', columns='subcategory', values='quantity')
    fig, ax = plt.subplots(figsize=(8, 5))
    demand_pivot.plot(ax=ax, marker='o', linewidth=2)
    ax.set_title('Monthly Demand by Top Subcategories', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Units Sold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # product weight distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(products['product_weight_kg'], bins=30, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Product Weight Distribution', fontweight='bold')
    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Number of Products')
    ax.axvline(products['product_weight_kg'].median(), color='red', linestyle='--',
               label=f"Median: {products['product_weight_kg'].median():.2f} kg")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q19 - Product Rating & Review
# ============================================================
st.markdown('<p class="section-title">Q19 — Product Rating & Review</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df['product_rating'], bins=20, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Product Rating Distribution', fontweight='bold')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    ax.axvline(df['product_rating'].mean(), color='red', linestyle='--',
               label=f"Mean: {df['product_rating'].mean():.2f}")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # rating vs subcategory
    subcat_rating = df.groupby('subcategory')['product_rating'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    subcat_rating.plot(kind='barh', ax=ax, color='#232F3E')
    ax.set_title('Avg Rating by Subcategory', fontweight='bold')
    ax.set_xlabel('Avg Rating')
    ax.axvline(df['product_rating'].mean(), color='red', linestyle='--', label='Overall Avg')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# rating vs revenue heatmap by subcategory
rating_revenue = df.groupby(['subcategory', 'order_year']).agg(
    avg_rating=('product_rating', 'mean'),
    revenue=('final_amount_inr', 'sum')
).reset_index()

st.markdown("**Rating vs Revenue Correlation by Subcategory:**")
fig, ax = plt.subplots(figsize=(12, 4))
for subcat in top_subcats:
    mask = rating_revenue['subcategory'] == subcat
    ax.scatter(rating_revenue[mask]['avg_rating'], rating_revenue[mask]['revenue']/1e6,
               label=subcat, s=100, alpha=0.7)
ax.set_title('Rating vs Revenue by Subcategory', fontweight='bold')
ax.set_xlabel('Avg Rating')
ax.set_ylabel('Revenue (₹ Million)')
ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q20 - New Product Launch
# ============================================================
st.markdown('<p class="section-title">Q20 — New Product Launch Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # subcategory revenue over time (product lifecycle)
    subcat_yearly = df.groupby(['order_year', 'subcategory'])['final_amount_inr'].sum().reset_index()
    subcat_top5 = subcat_yearly[subcat_yearly['subcategory'].isin(top_subcats)]
    subcat_pivot = subcat_top5.pivot(index='order_year', columns='subcategory', values='final_amount_inr')/1e9
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_pivot.plot(kind='area', ax=ax, alpha=0.6, colormap='Set2')
    ax.set_title('Subcategory Revenue Evolution (2015-2025)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # prime eligible products performance
    prime_products = products.groupby('is_prime_eligible').agg(
        count=('product_id', 'count'),
        avg_rating=('product_rating', 'mean'),
        avg_price=('discounted_price_inr', 'mean')
    ).reset_index()
    prime_products['is_prime_eligible'] = prime_products['is_prime_eligible'].map({True: 'Prime', False: 'Non-Prime'})
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(prime_products['is_prime_eligible'], prime_products['count'], color=['#FF9900', '#232F3E'])
    ax.set_title('Prime vs Non-Prime Product Count', fontweight='bold')
    ax.set_xlabel('Prime Status')
    ax.set_ylabel('Number of Products')
    for bar, val in zip(bars, prime_products['count']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, str(val), ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.caption("📦 Product & Inventory Dashboard | Amazon India Sales Analytics")
