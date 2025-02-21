import pandas as pd
import datetime as dt

def create_daily_orders_df(main_df):
    main_df['order_approved_at'] = pd.to_datetime(main_df['order_approved_at'])
    df = main_df.set_index('order_approved_at')  # Simpan perubahan dalam variabel df
    df = df.resample('D').agg({'customer_id': 'nunique'}).reset_index()
    df.rename(columns={'order_approved_at': 'date', 'customer_id': 'num_customers'}, inplace=True)

    return df

def create_monthly_orders_df(main_df):
    main_df['order_approved_at'] = pd.to_datetime(main_df['order_approved_at'])
    df = main_df.set_index('order_approved_at')  # Simpan perubahan dalam variabel df
    df = df.resample('M').agg({'customer_id': 'nunique'}).reset_index()
    df.rename(columns={'order_approved_at': 'date', 'customer_id': 'num_customers'}, inplace=True)

    return df

def create_yearly_orders_df(main_df):
    main_df['order_approved_at'] = pd.to_datetime(main_df['order_approved_at'])
    df = main_df.set_index('order_approved_at')  # Simpan perubahan dalam variabel df
    df = df.resample('Y').agg({'customer_id': 'nunique'}).reset_index()
    df.rename(columns={'order_approved_at': 'date', 'customer_id': 'num_customers'}, inplace=True)

    return df

    
def create_best_selling_products_df(main_df):
    df = (
    main_df.groupby(['product_category_name', 'product_category_name_english'])
    .agg(total_transactions=('order_id', 'count'))
    .sort_values(by='total_transactions', ascending=False)
    .reset_index()
    )

    return df

def create_customer_satisfaction(main_df):
    df = (
        main_df.groupby('review_score')
        .agg(review_count=('order_id', 'nunique'), avg_response_time=('review_response_time', 'mean'))
        .sort_values(by='review_count', ascending=False)
        .reset_index()
    )
    return df

def create_payments_df(main_df):
    df = (
        main_df.groupby('payment_type')
        .agg({
            'order_id': 'nunique',
            'payment_value' : ['mean', 'max', 'min']}
        )
        .rename(columns={'order_id' : 'total_transactions'})
        .sort_values(by=('total_transactions', 'nunique'), ascending=False)
        .reset_index()
    )
    return df

def create_city_users_df(main_df):
    df = (
        main_df.groupby('customer_state')
        .agg(total_users=('customer_id', 'nunique'))  
        .sort_values(by='total_users', ascending=False)
        .reset_index()
    )
    return df

def create_rfm_df(main_df):

    main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])
    reference_date = main_df['order_purchase_timestamp'].max() + dt.timedelta(days=1)

    # Calculate RFM
    rfm_df = main_df.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'price': 'sum'  # Monetary
    }).reset_index()

    # Change column names
    rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    return rfm_df

