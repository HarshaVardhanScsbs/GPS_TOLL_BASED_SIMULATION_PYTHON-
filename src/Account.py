import pandas as pd

# Load account information from Excel file
accounts = pd.read_excel('/vehicle_data.xlsx')


# Function to debit toll amount and print balance
def debit_toll_and_print_balance(vehicle_number, toll_amount):
    # Find the account associated with the vehicle number
    account = accounts.loc[accounts['vehicle_id'] == vehicle_number]

    # Check if the account was found
    if account.empty:
        print(f'No account found for vehicle {vehicle_number}')
        return

    # Get the current balance
    current_balance = account['InitialBalance'].values[0]

    # Check if the initial balance is sufficient
    if current_balance < toll_amount:
        print('lesser')
    else:
        # Debit the toll amount from the account
        accounts.loc[accounts['vehicle_id'] == vehicle_number, 'InitialBalance'] -= toll_amount
        updated_balance = current_balance - toll_amount
        # Print the new balance
        print(f'Vehicle {vehicle_number}: New balance = {updated_balance:.2f}')
