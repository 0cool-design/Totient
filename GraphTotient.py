#!/usr/bin/env python3
import csv, os, sys, glob, threading, time, itertools
import pandas as pd
import plotly.express as px
from sortedcontainers import SortedDict
from csv import writer
#from tqdm import tqdm #for i in tqdm(range(number+1)):


fieldnames = ['phi_y', 'Number_x']
filename = ''
done = False

def phi(n):
    result = n
    p = 2
    while(p * p <= n):
        if (n % p == 0):
            while (n % p == 0):
                n = int(n / p)
            result -= int(result / p)
        p += 1
    if (n > 1):
        result -= int(result / n)
    return result

def animate_loading():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done==True:
            break

        sys.stdout.write('\r['+c+'] Loading ')
        sys.stdout.flush()
        time.sleep(0.1)

def create_csv(number):
    global fieldnames, filename
    # check if file already exists
    if os.path.exists(filename):
        return 1
    else:
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # write columns
                writer.writeheader()
                csvfile.close()
                return 0
        except AttributeError:
            sys.exit()

def write_phi_csv(number, phi):
    global fieldnames, filename
    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'phi_y': phi, 'Number_x': number})
        csvfile.close()
def loop_csv(number):
    for i in range(number+1):
        write_phi_csv(i, phi(i))

def data_Table(number):
    global filename
    df = pd.read_csv(filename)
    print("\n"+"="*5,number,"="*5)
    print(" "*5,phi(number)," "*5)
    print ("\n", df)


def graph_phi(number):
    global filename
    try:
        df = pd.read_csv(filename)
        fig = px.line(df, y = 'phi_y', x = 'Number_x', title='Totient Function ( '+str(number)+' )')
        fig.show()

    except pd.errors.ParserError:
        sys.exit()
def clear():
    if os.name == 'posix': # Check os
        os.system('clear')
    else:
        os.system('cls')

def main():
    global filename, done
    number = int(input("Number> "))
    filename = 'phi_'+str(number)+'_.csv'
    file_State = create_csv(number)
    if file_State == 0:
        loading_T = threading.Thread(target=animate_loading)
        loading_T.start()
        loop_T = threading.Thread(target=loop_csv(number))
        loop_T.start()

    done = True
    clear()

    dataT = threading.Thread(target=data_Table(number))
    graph_Phi = threading.Thread(target=graph_phi(number))
    graph_Phi.start()
    dataT.start()

    sys.exit()

if __name__ == "__main__":
    main()
