'''
Fractional Reserve Banking
'''
import csv
import os
import click
import pandas as pd

def fill_data(row, bank_data):
    '''
    Fill and sort data inside the dictionnary
    '''
    return bank_data

def clean_row(row):
    '''
    Clean each row of any whitespace
    '''
    new_row = []
    for item in row:
        item = item.strip()
        new_row.append(item)
    del row
    return new_row

def init_data():
    '''
    Initialize a new Dictionnary containing informations on the Bank
    '''
    bank_data = {
        "bank_name": None,
        "deposits": None,
        "reserve_rate": None,
        "total_deposits": [],
        "money_created": [],
        "money_supply": []
    }
    return bank_data

def set_data(file):
    '''
    Open and read the data inside the CSV file
    '''
    bank_data = init_data()
    with open(file, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        try:
            for row in reader:
                row = clean_row(row)
                bank_data = fill_data(row, bank_data)
        except csv.Error:
            print("Unable to read the CSV file.")
            return None
        finally:
            del reader
    return bank_data

def builder(file):
    '''
    Build the final graph and display the results
    '''
    bank_data = set_data(file)
    if bank_data:
        pass

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
    Python Script which display datatables of the money created and the money supply by a bank
    '''

@cli.command('display')
@click.argument('file', type=click.Path(exists=True))
@click.argument('bank')
@click.argument('deposits')
def build_datatables(file):
    '''
    Build money created and money supply datatables
    '''
    if is_csv(file):
        builder(file)

if __name__ == '__main__':
    cli()
