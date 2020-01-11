'''
Fractional Reserve Banking
'''
import os
import click
import pandas as pd

INTEREST_RATE = 0.1

def display_datatables(bank_data):
    '''
    Display datatables in the CLI showing statistics about money deposited,
    money created and money supply annualy by each bank
    '''
    frame_deposits = pd.DataFrame(bank_data['deposits'], columns=bank_data['categories'],\
                              index=bank_data['bank_names'], dtype=float)
    frame_money_created = pd.DataFrame(bank_data['money_created'], columns=bank_data['categories'],\
                              index=bank_data['bank_names'], dtype=float)
    frame_money_supply = pd.DataFrame(bank_data['money_supply'], columns=bank_data['categories'],\
                              index=bank_data['bank_names'], dtype=float)
    print("{}\n\n{}\n\n{}".format(frame_deposits, frame_money_created, frame_money_supply))

def init_tmp():
    '''
    Initialize a temporary Dictionnary requiered to compute and copy results
    '''
    tmp = {
        "deposit": [],
        "money_created": [],
        "money_supply": []
    }
    return tmp

def set_bank_names(reader, bank_data):
    '''
    Save all bank names
    '''
    bank_names = list(reader['Bank Name'])
    for name in bank_names:
        if name and name != '….':
            bank_data["bank_names"].append(name)

def set_data(file, bank_data):
    '''
    Read and then compute the data of the CSV file
    '''
    reader = pd.read_csv(file)
    bank_data['categories'] = list(reader.columns[1:])
    set_bank_names(reader, bank_data)
    for column in bank_data['categories']:
        values = reader.loc[0:, column]
        tmp = init_tmp()
        for item in values:
            if item and item != '….':
                try:
                    money = round((float(item) * (1 - INTEREST_RATE))\
                                   / INTEREST_RATE, 2)
                    tmp['deposit'].append(float(item))
                    tmp['money_created'].append(money)
                    tmp['money_supply'].append(float(item) + money)
                    bank_data["deposits"][column] = tmp['deposit'].copy()
                    bank_data["money_created"][column] = tmp['money_created'].copy()
                    bank_data["money_supply"][column] = tmp['money_supply'].copy()
                except ValueError as error:
                    print("Please, insert only float numbers.\n{}".format(error))
    del tmp
    return bank_data

def init_data():
    '''
    Initialize a new Dictionnary which will contain results
    '''
    bank_data = {
        "deposits": {},
        "money_created": {},
        "money_supply": {},
        "bank_names": [],
        "categories": []
    }
    return bank_data

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv') or os.path.getsize(file) <= 0:
        print("Insert a correct CSV file please.")
        return False
    return True

@click.group()
def cli():
    '''
    Python Script which compute money created and supplied by bank
    '''

@cli.command('display')
@click.argument('file', type=click.Path(exists=True))
def build_datatables(file):
    '''
    Build money deposited, money created, money supply datatables
    '''
    if is_csv(file):
        bank_data = init_data()
        set_data(file, bank_data)
        display_datatables(bank_data)

if __name__ == '__main__':
    cli()
