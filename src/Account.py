import pandas as pd

accounts = pd.read_excel('/vehicle_data.xlsx')


def debit_toll_and_print_balance(vehicle_number, toll_amount):
    account = accounts.loc[accounts['vehicle_id'] == vehicle_number]

    if account.empty:
        print(f'No account found for vehicle {vehicle_number}')
        return

    current_balance = account['InitialBalance'].values[0]

    if current_balance < toll_amount:
        print('lesser')
    else:
        accounts.loc[accounts['vehicle_id'] == vehicle_number, 'InitialBalance'] -= toll_amount
        updated_balance = current_balance - toll_amount
        print(f'Vehicle {vehicle_number}: New balance = {updated_balance:.2f}')
