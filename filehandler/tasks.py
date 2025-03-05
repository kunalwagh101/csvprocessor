import pandas as pd
from celery import shared_task

@shared_task
def process_csv_task(file_path):
    results = {}
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {'error': f"Error reading CSV: {str(e)}"}


    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        return {'error': "No numeric columns found in CSV."}

    calculations = {}
    for col in numeric_cols:
        col_sum = float(df[col].sum())
        col_avg = float(df[col].mean())
        col_count = int(df[col].count())
        calculations[col] = {
            'sum': col_sum,
            'average': col_avg,
            'count': col_count
        }

    additional_metrics = {}
    if 'Sales' in df.columns:
        additional_metrics['total_revenue'] = float(df['Sales'].sum())
    if 'Discount' in df.columns:
        additional_metrics['average_discount'] = float(df['Discount'].mean())
    if 'Product' in df.columns and 'Quantity' in df.columns:
        product_sales = df.groupby('Product')['Quantity'].sum()
        additional_metrics['best_selling_product'] = product_sales.idxmax()
    if 'Product' in df.columns and 'Profit' in df.columns:
        product_profit = df.groupby('Product')['Profit'].sum()
        additional_metrics['most_profitable_product'] = product_profit.idxmax()
    if 'Product' in df.columns and 'Discount' in df.columns:
        max_discount_idx = df['Discount'].idxmax()
        additional_metrics['product_max_discount'] = df.loc[max_discount_idx, 'Product']

  
    data = []
    for record in df.to_dict(orient='records'):
        new_record = {}
        for key, value in record.items():
            # Convert numpy types to Python types
            if hasattr(value, 'item'):
                new_record[key] = value.item()
            else:
                new_record[key] = value
        data.append(new_record)

    results['calculations'] = calculations
    results['additional_metrics'] = additional_metrics
    results['data'] = data

    return results
