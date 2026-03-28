import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Customer Analytics", page_icon="👥", layout="wide")

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

st.markdown('<p class="page-title">👥 Customer Analytics Dashboard</p>', unsafe_allow_html=True)

# ============================================================
# Q11 - Customer Segmentation (RFM)
# ============================================================
st.markdown('<p class="section-title">Q11 — Customer Segmentation (RFM)</p>', unsafe_allow_html=True)

@st.cache_data
def compute_rfm(df):
    reference_date = df['order_date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('customer_id').agg(
        recency=('order_date', lambda x: (reference_date - x.max()).days),
        frequency=('transaction_id', 'count'),
        monetary=('final_amount_inr', 'sum')
    ).reset_index()
    rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
    rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

    def segment(row):
        r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
        if r >= 4 and f >= 4 and m >= 4: return 'Champions'
        elif r >= 3 and f >= 3 and m >= 3: return 'Loyal Customers'
        elif r >= 4 and f <= 2: return 'New Customers'
        elif r <= 2 and f >= 3 and m >= 3: return 'At Risk'
        elif r <= 2 and f <= 2 and m <= 2: return 'Lost Customers'
        else: return 'Potential Loyalists'

    rfm['segment'] = rfm.apply(segment, axis=1)
    return rfm

rfm = compute_rfm(df)

colors_map = {
    'Champions': '#2ecc71', 'Loyal Customers': '#3498db',
    'New Customers': '#1abc9c', 'At Risk': '#f39c12',
    'Lost Customers': '#e74c3c', 'Potential Loyalists': '#9b59b6'
}

col1, col2, col3 = st.columns(3)
with col1:
    segment_counts = rfm['segment'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%',
           colors=[colors_map[s] for s in segment_counts.index])
    ax.set_title('Customer Segment Distribution', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(6, 5))
    for segment, color in colors_map.items():
        mask = rfm['segment'] == segment
        ax.scatter(rfm[mask]['recency'], rfm[mask]['frequency'], c=color, label=segment, alpha=0.5, s=10)
    ax.set_title('Recency vs Frequency', fontweight='bold')
    ax.set_xlabel('Recency (days)')
    ax.set_ylabel('Frequency')
    ax.legend(markerscale=3, fontsize=7)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col3:
    avg_monetary = rfm.groupby('segment')['monetary'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(avg_monetary.index, avg_monetary/1000, color=[colors_map[s] for s in avg_monetary.index])
    ax.set_title('Avg Spending by Segment (₹K)', fontweight='bold')
    ax.set_xlabel('Segment')
    ax.set_ylabel('Avg Spending (₹ Thousands)')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q12 - Customer Journey
# ============================================================
st.markdown('<p class="section-title">Q12 — Customer Journey Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # purchase frequency distribution
    purchase_freq = df.groupby('customer_id')['transaction_id'].count()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(purchase_freq, bins=30, color='#FF9900', alpha=0.7, edgecolor='black')
    ax.set_title('Purchase Frequency Distribution', fontweight='bold')
    ax.set_xlabel('Number of Purchases')
    ax.set_ylabel('Number of Customers')
    ax.axvline(purchase_freq.median(), color='red', linestyle='--', label=f'Median: {purchase_freq.median():.0f}')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # first purchase year distribution
    first_purchase = df.groupby('customer_id')['order_year'].min().reset_index()
    first_purchase.columns = ['customer_id', 'first_year']
    year_counts = first_purchase['first_year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(year_counts.index, year_counts.values, color='#232F3E')
    ax.set_title('New Customer Acquisition by Year', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('New Customers')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q13 - Prime Membership Analytics
# ============================================================
st.markdown('<p class="section-title">Q13 — Prime Membership Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # prime eligible vs revenue
    prime_revenue = df.groupby('is_prime_eligible')['final_amount_inr'].agg(['sum', 'mean', 'count']).reset_index()
    prime_revenue['is_prime_eligible'] = prime_revenue['is_prime_eligible'].map({True: 'Prime Eligible', False: 'Not Prime Eligible'})
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(prime_revenue['is_prime_eligible'], prime_revenue['sum']/1e9, color=['#FF9900', '#232F3E'])
    ax.set_title('Total Revenue: Prime vs Non-Prime Eligible', fontweight='bold')
    ax.set_xlabel('Prime Status')
    ax.set_ylabel('Revenue (₹ Billion)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # prime eligible avg order value
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(prime_revenue['is_prime_eligible'], prime_revenue['mean'], color=['#2ecc71', '#e74c3c'])
    ax.set_title('Avg Order Value: Prime vs Non-Prime Eligible', fontweight='bold')
    ax.set_xlabel('Prime Status')
    ax.set_ylabel('Avg Order Value (₹)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================
# Q14 - Customer Retention (Cohort Analysis)
# ============================================================
st.markdown('<p class="section-title">Q14 — Customer Retention (Cohort Analysis)</p>', unsafe_allow_html=True)

@st.cache_data
def compute_cohort(df):
    df['first_year'] = df.groupby('customer_id')['order_year'].transform('min')
    cohort = df.groupby(['first_year', 'order_year'])['customer_id'].nunique().reset_index()
    cohort.columns = ['cohort_year', 'order_year', 'customers']
    cohort_pivot = cohort.pivot(index='cohort_year', columns='order_year', values='customers')
    cohort_pct = cohort_pivot.divide(cohort_pivot.iloc[:, 0], axis=0) * 100
    return cohort_pct

cohort_pct = compute_cohort(df)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(cohort_pct, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax,
            cbar_kws={'label': 'Retention %'}, linewidths=0.5)
ax.set_title('Customer Retention Cohort Analysis (%)', fontweight='bold')
ax.set_xlabel('Order Year')
ax.set_ylabel('Cohort Year (First Purchase)')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ============================================================
# Q15 - Demographics & Behavior
# ============================================================
st.markdown('<p class="section-title">Q15 — Demographics & Behavior</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age_revenue = df.groupby('customer_age_group')['final_amount_inr'].agg(['sum', 'mean']).reset_index()
    age_order = ['18-25', '26-35', '36-45', '46-55', '55+']
    age_revenue['customer_age_group'] = pd.Categorical(age_revenue['customer_age_group'], categories=age_order, ordered=True)
    age_revenue = age_revenue.sort_values('customer_age_group')
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(age_revenue['customer_age_group'], age_revenue['sum']/1e9, color='#FF9900')
    ax.set_title('Total Revenue by Age Group', fontweight='bold')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Revenue (₹ Billion)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    age_subcat = df.groupby(['customer_age_group', 'subcategory'])['final_amount_inr'].sum().reset_index()
    top_subcats = df.groupby('subcategory')['final_amount_inr'].sum().nlargest(5).index.tolist()
    age_subcat_top = age_subcat[age_subcat['subcategory'].isin(top_subcats)]
    age_pivot = age_subcat_top.pivot(index='customer_age_group', columns='subcategory', values='final_amount_inr')/1e9
    fig, ax = plt.subplots(figsize=(8, 4))
    age_pivot.plot(kind='bar', ax=ax, colormap='Set2')
    ax.set_title('Top Subcategory Preferences by Age Group', fontweight='bold')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Revenue (₹ Billion)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.caption("👥 Customer Analytics Dashboard | Amazon India Sales Analytics")
