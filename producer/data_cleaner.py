def clean_data(row: dict):
    cleaned_row = {
        'description': row['description'].lower(),
        'amount': float(row['amount'])
    }
    return cleaned_row