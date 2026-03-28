import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Advanced Analytics", page_icon="🔮", layout="wide")

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

st.markdown('<p class="page-title">🔮 Advanced Analytics Dashboard</p>', unsafe_allow_html=True)

# ============================================================
# Q26 - Predictive Analytics
# ============================================================
st.markdown('<p class="section-title">Q26 — Predictive Analytics & Sales Forecasting</p>', unsafe_allow_html=True)

# yearly revenue forecasting
yearly = df.groupby('order_year')['final_amount_inr'].sum().reset_index()
yearly.columns = ['year', 'revenue']

X = yearly['year'].values.reshape(-1, 1)
y = yearly['revenue'].values
model = LinearRegression()
model.fit(X, y)

future_years = np.array([2026, 2027, 2028]).reshape(-1, 1)
future_revenue = model.predict(future_years)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(yearly['year'], yearly['revenue']/1e9, color='#FF9900', alpha=0.8, label='Actual')
    ax.bar(future_years.flatten(), future_revenue/1e9, color='#232F3E', alpha=0.6, label='Forecast')
    trend_years = np.array(list(yearly['year']) + list(future_years.flatten()))
    trend_revenue = model.predict(trend_years.reshape(-1, 1))
    ax.plot(trend_years, trend_revenue/1e9, 'r--', linewidth=2, label='Trend Line')
    ax.set_title('Revenue Forecast (2026-2028)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # monthly forecast
    monthly = df.groupby(['order_year', 'order_month'])['final_amount_inr'].sum().reset_index()
    monthly['time_index'] = (monthly['order_year'] - 2015) * 12 + monthly['order_month']
    X_m = monthly['time_index'].values.reshape(-1, 1)
    y_m = monthly['final_amount_inr'].values
    model_m = LinearRegression()
    model_m.fit(X_m, y_m)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly['time_index'], monthly['final_amount_inr']/1e6, alpha=0.6, color='#FF9900', label='Actual')
    ax.plot(monthly['time_index'], model_m.predict(X_m)/1e6, 'r--', linewidth=2, label='Trend')
    ax.set_title('Monthly Revenue Trend & Forecast', fontweight='bold')
    ax.set_xlabel('Time Index (months from 2015)')
    ax.set_ylabel('Revenue (₹ Million)')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# forecast table
st.markdown("**Revenue Forecast Table:**")
forecast_df = pd.DataFrame({
    'Year': future_years.flatten(),
    'Forecasted Revenue (₹ Billion)': (future_revenue/1e9).round(2)
})
st.dataframe(forecast_df, use_container_width=True)

st.markdown("---")

# ============================================================
# Q27 - Market Intelligence
# ============================================================
st.markdown('<p class="section-title">Q27 — Market Intelligence</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # subcategory market share evolution
    subcat_yearly = df.groupby(['order_year', 'subcategory'])['final_amount_inr'].sum().reset_index()
    top_subcats = df.groupby('subcategory')['final_amount_inr'].sum().nlargest(6).index.tolist()
    subcat_top = subcat_yearly[subcat_yearly['subcategory'].isin(top_subcats)]
    subcat_pivot = subcat_top.pivot(index='order_year', columns='subcategory', values='final_amount_inr')
    subcat_pct = subcat_pivot.divide(subcat_pivot.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    subcat_pct.plot(kind='area', ax=ax, alpha=0.7, colormap='Set2', stacked=True)
    ax.set_title('Subcategory Market Share Evolution', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Market Share (%)')
    ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # brand market share evolution
    top_brands = df.groupby('brand')['final_amount_inr'].sum().nlargest(6).index.tolist()
    brand_yearly = df[df['brand'].isin(top_brands)].groupby(['order_year', 'brand'])['final_amount_inr'].sum().reset_index()
    brand_pivot = brand_yearly.pivot(index='order_year', columns='brand', values='final_amount_inr')
    brand_pct = brand_pivot.divide(brand_pivot.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    brand_pct.plot(kind='area', ax=ax, alpha=0.7, colormap='Set1', stacked=True)
    ax.set_title('Brand Market Share Evolution', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Market Share (%)')
    ax.legend(title='Brand', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q28 - Cross-selling & Upselling
# ============================================================
st.markdown('<p class="section-title">Q28 — Cross-selling & Upselling Opportunities</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # customers who bought multiple subcategories
    customer_subcat = df.groupby('customer_id')['subcategory'].nunique().reset_index()
    customer_subcat.columns = ['customer_id', 'num_subcategories']
    fig, ax = plt.subplots(figsize=(8, 4))
    customer_subcat['num_subcategories'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#FF9900')
    ax.set_title('Customers by Number of Subcategories Purchased', fontweight='bold')
    ax.set_xlabel('Number of Subcategories')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # avg order value by number of subcategories
    customer_value = df.groupby('customer_id').agg(
        num_subcategories=('subcategory', 'nunique'),
        avg_order=('final_amount_inr', 'mean')
    ).reset_index()
    subcat_value = customer_value.groupby('num_subcategories')['avg_order'].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    subcat_value.plot(kind='bar', ax=ax, color='#232F3E')
    ax.set_title('Avg Order Value by Purchase Diversity', fontweight='bold')
    ax.set_xlabel('Number of Subcategories Purchased')
    ax.set_ylabel('Avg Order Value (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# subcategory correlation
subcat_customer = df.groupby(['customer_id', 'subcategory'])['transaction_id'].count().unstack(fill_value=0)
subcat_corr = subcat_customer.corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(subcat_corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax,
            linewidths=0.5, cbar_kws={'label': 'Correlation'})
ax.set_title('Subcategory Purchase Correlation (Cross-selling Opportunities)', fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q29 - Seasonal Planning
# ============================================================
st.markdown('<p class="section-title">Q29 — Seasonal Planning Dashboard</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # monthly heatmap
    monthly_pivot = df.groupby(['order_year', 'order_month'])['final_amount_inr'].sum().reset_index()
    heatmap_data = monthly_pivot.pivot(index='order_year', columns='order_month', values='final_amount_inr')/1e9
    heatmap_data.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
                linewidths=0.5, cbar_kws={'label': 'Revenue (₹ Billion)'})
    ax.set_title('Monthly Revenue Heatmap (₹ Billion)', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Year')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # festival calendar
    festival_monthly = df[df['festival_name'] != 'No Festival'].groupby(
        ['order_month', 'festival_name'])['final_amount_inr'].sum().reset_index()
    festival_pivot = festival_monthly.pivot(index='order_month', columns='festival_name', values='final_amount_inr').fillna(0)/1e9
    fig, ax = plt.subplots(figsize=(8, 6))
    festival_pivot.plot(kind='bar', ax=ax, colormap='Set2', stacked=True)
    ax.set_title('Festival Revenue by Month', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.set_xticks(range(12))
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=45)
    ax.legend(title='Festival', bbox_to_anchor=(1.05, 1), fontsize=7)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q30 - BI Command Center
# ============================================================
st.markdown('<p class="section-title">Q30 — Business Intelligence Command Center</p>', unsafe_allow_html=True)

# KPI metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Revenue", f"₹{df['final_amount_inr'].sum()/1e9:.1f}B",
              delta=f"+{((df[df['order_year']==2024]['final_amount_inr'].sum() / df[df['order_year']==2023]['final_amount_inr'].sum() - 1)*100):.1f}% YoY")
with col2:
    st.metric("Total Customers", f"{df['customer_id'].nunique():,}")
with col3:
    st.metric("Total Orders", f"{df['transaction_id'].nunique():,}")
with col4:
    st.metric("Avg Order Value", f"₹{df['final_amount_inr'].mean():,.0f}")
with col5:
    st.metric("Avg Delivery Days", f"{df['delivery_days'].mean():.1f}")

# combined dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. revenue trend
yearly = df.groupby('order_year')['final_amount_inr'].sum()
axes[0, 0].bar(yearly.index, yearly.values/1e9, color='#FF9900')
axes[0, 0].set_title('Yearly Revenue (₹B)', fontweight='bold')
axes[0, 0].set_xlabel('Year')

# 2. payment methods
payment = df['payment_method'].value_counts()
axes[0, 1].pie(payment, labels=payment.index, autopct='%1.0f%%',
               colors=['#FF9900', '#232F3E', '#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f39c12'])
axes[0, 1].set_title('Payment Methods', fontweight='bold')

# 3. top cities
city_rev = df.groupby('customer_city')['final_amount_inr'].sum().nlargest(8)
axes[0, 2].barh(city_rev.index, city_rev.values/1e9, color='#232F3E')
axes[0, 2].set_title('Top 8 Cities (₹B)', fontweight='bold')

# 4. festival impact
festival = df.groupby('festival_name')['final_amount_inr'].sum().sort_values(ascending=False).head(6)
axes[1, 0].bar(festival.index, festival.values/1e9, color='#e74c3c')
axes[1, 0].set_title('Festival Revenue (₹B)', fontweight='bold')
axes[1, 0].tick_params(axis='x', rotation=45)

# 5. customer tier
tier = df.groupby('customer_tier')['final_amount_inr'].sum()
axes[1, 1].pie(tier, labels=tier.index, autopct='%1.1f%%',
               colors=['#FF9900', '#232F3E', '#2ecc71', '#3498db'])
axes[1, 1].set_title('Revenue by Tier', fontweight='bold')

# 6. monthly pattern
monthly_avg = df.groupby('order_month')['final_amount_inr'].mean()
axes[1, 2].bar(monthly_avg.index, monthly_avg.values/1e6, color='#FF9900')
axes[1, 2].set_title('Avg Monthly Revenue (₹M)', fontweight='bold')
axes[1, 2].set_xticks(range(1, 13))
axes[1, 2].set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'])

plt.suptitle('Amazon India — BI Command Center', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.caption("🔮 Advanced Analytics Dashboard | Amazon India Sales Analytics")
