import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import create.createDF as cr

sns.set(style='darkgrid')

# Load data
main_df = pd.read_csv('dashboard/merged_data.csv')

min_date = main_df['order_approved_at'].min()
max_date = main_df['order_approved_at'].max()

# -- sidebar --
with st.sidebar:
    st.image('dashboard/image/olist_logo.png', width=250)
    date_selection = st.date_input(
        label='Date Filter :date:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    try:
        start_date, end_date = date_selection 
    except ValueError:
        st.error('Invalid date range')
        st.stop()

# Filter data based on date range
main_df = main_df[(main_df['order_approved_at'] >= str(start_date)) & 
                (main_df['order_approved_at'] <= str(end_date))]

st.title('Dashboard Brazil E-Commerce Public Dataset by Olist :rocket:') 
with st.expander('View dataframe'):
    st.dataframe(main_df)


customer_count = main_df['customer_id'].nunique()
categories_count = main_df['product_category_name_english'].nunique()
total_price = main_df['payment_value'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Customer Count :busts_in_silhouette:", value=customer_count)
with col2:
    st.metric("Categories Count :shopping_bags:", value=categories_count)
with col3:
    st.metric("Total Price :moneybag:", value=total_price)

tab1, tab2, tab3 = st.tabs(['Daily Orders', 'Monthly Orders', 'Yearly Orders'])
with tab1:
    # --- Daily Orders ---
    st.header('Daily Orders')
    daily_orders_df = cr.create_daily_orders_df(main_df)  
    st.metric('Average Daily Orders :bar_chart:', value=daily_orders_df['num_customers'].mean())
    fig = plt.figure(figsize=(12, 6))
    
    sns.lineplot(data=daily_orders_df, x='date', y='num_customers')
    plt.title('Daily Order Count')
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    # --- Monthly Orders ---
    st.header('Monthly Orders')
    monthly_orders_df = cr.create_monthly_orders_df(main_df)
    st.metric('Average Monthly Orders :bar_chart:', value=monthly_orders_df['num_customers'].mean())
    fig = plt.figure(figsize=(12, 6))

    sns.lineplot(data=monthly_orders_df, x='date', y='num_customers')
    plt.title('Monthly Order Count')
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab3:
    # --- Yearly Orders ---
    st.header('Yearly Orders')
    yearly_orders_df = cr.create_yearly_orders_df(main_df)
    st.metric('Average Yearly Orders :bar_chart:', value=yearly_orders_df['num_customers'].mean())
    fig = plt.figure(figsize=(12, 6))
    
    sns.lineplot(data=yearly_orders_df, x='date', y='num_customers')
    plt.title('Monthly Order Count')
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(rotation=45)
    st.pyplot(fig)



# --- Top 10 Best Selling Products Categoris ---
best_selling_products_df = cr.create_best_selling_products_df(main_df)
st.subheader('Top 10 Best Selling Product Categories :trophy:')
fig = plt.figure(figsize=(12,6))
sns.barplot(
    data=best_selling_products_df.sort_values(by='total_transactions', ascending=False).head(10), 
    x='total_transactions', y='product_category_name_english', hue='product_category_name_english', 
    legend=False, palette="BuPu_r_d")

plt.xlabel('Total Transactions')
plt.ylabel(None)
plt.title('Top 10 Best-Selling Product Categories')
st.pyplot(fig)


col1, col2 = st.columns([0.4, 0.6])
with col1:
    # --- Payment Methods ---
    payments_df = cr.create_payments_df(main_df)
    st.subheader('Payment Methods Distribution :pushpin:')
    df_filtered = payments_df[payments_df['payment_type'] != 'not_defined']

    payment_labels = df_filtered['payment_type']
    payment_counts = df_filtered[('total_transactions', 'nunique')]
    explode = (0.1, 0, 0, 0)

    fig = plt.figure(figsize=(7,6))
    plt.pie(
        payment_counts, explode=explode, labels=payment_labels, colors=sns.color_palette('deep'),
        autopct='%1.1f%%', wedgeprops={'edgecolor': 'white', 'linewidth': 1.2}, 
        shadow=True, pctdistance=0.5, radius=1.05
    )

    plt.title('Distribution of Payment Methods')
    st.pyplot(fig)

with col2:
    # --- Customer Satisfaction ---
    customer_satisfaction_df = cr.create_customer_satisfaction(main_df)
    st.subheader('Customer Satisfaction based On Review Score :smiley:')
    num_colors = customer_satisfaction_df['review_score'].nunique()
    colors = sns.color_palette('YlGnBu', n_colors=num_colors)  

    fig = plt.figure(figsize=(10,5))
    ax = sns.barplot(data=customer_satisfaction_df, x='review_score', y='review_count', hue='review_score', legend=False, palette=colors)

    plt.xlabel('Review Score')
    plt.ylabel('Number of Reviews')
    plt.title('Customer Review Score Distribution')

    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', 
                    (p.get_x() + p.get_width()/2, p.get_height()), 
                    xytext=(0,5), textcoords='offset points', 
                    ha='center', fontsize=10)

    st.pyplot(fig)

# Fix duplicate issue
main_df = main_df.drop_duplicates().reset_index(drop=True)

# --- Late Delivery Impact on Customer Satisfaction ---
st.subheader('Late Delivery Impact on Customer Satisfaction :truck: ')
fig = plt.figure(figsize=(10, 6 ))
sns.barplot(data=main_df, x='is_late', y='review_score', hue='is_late', legend=False, palette='rocket')
plt.xlabel('Late Delivery')
plt.ylabel('Average Review Score')
plt.title('Relationship Between Late Delivery and Customer Satisfaction')
plt.xticks([0,1], ['On Time', 'Late'])
plt.ylim(0, 5)
st.pyplot(fig)


# --- Total Customers by State ---
city_users_df = cr.create_city_users_df(main_df)
st.subheader('Total Customers by State :world_map:')
fig = plt.figure(figsize=(12,6))
sns.barplot(
    data=city_users_df.sort_values(by='total_users', ascending=True),
    x='customer_state', y='total_users', hue='customer_state', 
    legend=False, palette='viridis')
plt.title('Total Users by State')
plt.xlabel('State') 
plt.ylabel('Total Users')
st.pyplot(fig)


# --- RFM ---
rfm_df = cr.create_rfm_df(main_df)
st.subheader('RFM Analysis of Brazil E-Commerce Customers :chart_with_upwards_trend:')
col1, col2, col3 = st.columns(3)
# Setup plot size
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

with col1:
    sns.histplot(rfm_df['recency'], bins=30, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('Recency Distribution')
    axes[0].set_xlabel('Days Since Last Purchase')
    axes[0].set_ylabel('Number of Customers')

with col2:
    sns.histplot(rfm_df['frequency'], bins=30, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Frequency Distribution')
    axes[1].set_xlabel('Number of Purchases')
    axes[1].set_ylabel('Number of Customers')

with col3:
    sns.histplot(rfm_df['monetary'], bins=30, kde=True, ax=axes[2], color='red')
    axes[2].set_title('Monetary Distribution')
    axes[2].set_xlabel('Total Spend (in Currency)')
    axes[2].set_ylabel('Number of Customers')

plt.tight_layout()
st.pyplot(fig)