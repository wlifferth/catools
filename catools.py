from collections import Counter
import matplotlib.pyplot as plt
import gender_guesser.detector as gender_detector
import numpy as np
import scipy.stats as stats

def purchase_frequency(customer_id, graph=True, text=True, bounds=None):
    customer_visits = Counter(customer_id).values()
    distribution = Counter(customer_visits)
    repeats = 1 - (distribution[1] / sum(distribution.values()))
    if text:
        print("{:.2f}% of transactions involve repeat customers".format(repeats * 100))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.hist(customer_visits, bins=[1,2,3,4,5,6,7,8,9,10])
        plt.title("Number of Orders per Customer", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Number of Orders")
        if bounds != None:
            plt.xlim(bounds)
        plt.show()

def gender_breakdown(names, graph=True, text=True):
    d = gender_detector.Detector()
    def get_first_name(x):
        try:
            fn = x.split()[0]
            return fn
        except:
            return '-' 

    def compress_gender(x):
        if x in ['female', 'mostly_female']:
            return 'Female'
        elif x in ['male', 'mostly_male']:
            return 'Male'
        else:
            return 'Andro/Unknown' 

    first_names = map(get_first_name, names)
    genders = map(d.get_gender, first_names)
    genders = map(compress_gender, genders)
    gender_dict = Counter(genders)
    
    if text:
        print("Out of {} total customers:".format(sum(gender_dict.values())))
        for key in gender_dict.keys():
            print("\t{} cusomters were {}".format(gender_dict[key], key))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.bar(range(len(gender_dict)), list(gender_dict.values()), align='center')
        plt.xticks(range(len(gender_dict)), gender_dict.keys())
        plt.title("Gender Breakdown of Customers", fontsize=24, fontname='Pier Sans')
        plt.show() 

def average_purchase(transaction_amounts, graph=True, text=True, bounds=None):
    if text:
        print(stats.describe(transaction_amounts))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.hist(transaction_amounts)
        plt.title("Individual Transaction Amounts", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Number of Orders")
        if bounds != None:
            plt.xlim(bounds)
        plt.show()

def lifetime_value(customer_ids, transaction_amounts, graph=True, text=True, bounds=None, **kwargs):
    totals = {}
    for cust, amount in zip(customer_ids, transaction_amounts):
        if cust not in totals:
            totals[cust] = 0
        totals[cust] += amount
    total_vals = list(totals.values())
    if text:
        print("Your avaerage customer is worth ${} over their lifetime.".format(np.mean(total_vals)))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.hist(total_vals, **kwargs)
        plt.title("Lifetime Value of Customers (to date)", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Lifetime Value")
        if bounds != None:
            plt.xlim(bounds)
        plt.show()
