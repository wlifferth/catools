from collections import Counter
import matplotlib.pyplot as plt
import gender_guesser.detector as gender_detector
import numpy as np
import scipy.stats as stats

def purchase_frequency(customer_id, graph=True, text=True, plot_options={}):
    customer_visits = list(Counter(customer_id).values())
    distribution = Counter(customer_visits)
    repeats = 1 - (distribution[1] / sum(distribution.values()))
    if text:
        print("{:.2f}% of transactions involve repeat customers".format(repeats * 100))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.hist(customer_visits, bins=[1,2,3,4,5,6,7,8,9,10], **plot_options)
        plt.title("Number of Orders per Customer", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Number of Orders")


class GenderEstimator:
    def __init__(self, estimator=None):
        estimator = gender_detector.Detector()
        self.d = estimator

    def estimate(self, x):
        fn = self.get_first_name(x)
        raw_gender = self.d.get_gender(fn)
        processed_gender = self.compress_gender(raw_gender)
        return processed_gender

    def get_first_name(self, x):
        try:
            fn = x.split()[0]
            return fn
        except:
            return '-' 
    
    def compress_gender(self, x):
        if x in ['female', 'mostly_female']:
            return 'Female'
        elif x in ['male', 'mostly_male']:
            return 'Male'
        else:
            return 'Andro/Unknown' 



def gender_breakdown(names, graph=True, text=True, plot_options={}):
    d = gender_detector.Detector()
    first_names = map(get_first_name, names)
    genders = map(d.get_gender, first_names)
    genders = map(compress_gender, genders)
    gender_dict = Counter(genders)
    total_names = sum(gender_dict.values())
    if text:
        print("Out of {} total customers:".format(total_names))
        for key in gender_dict.keys():
            print("\t{} ({:.2f}%) cusomters were {}".format(gender_dict[key], 100 * gender_dict[key]/total_names, key))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.bar(range(len(gender_dict)), [gender_dict['Female'], gender_dict['Male'], gender_dict['Andro/Unknown']], align='center', **plot_options)
        plt.xticks(range(len(gender_dict)), ['Female', 'Male', 'Andro/Unknown'])
        plt.title("Gender Breakdown of Customers", fontsize=24, fontname='Pier Sans')
        plt.xlabel("Gender")

def average_purchase(transaction_amounts, graph=True, text=True, plot_options={}):
    if text:
        print("Your avaerage purchase is ${}.".format(np.mean(transaction_amounts)))
    if graph:
        plt.style.use('ggplot')
        plt.figure(dpi=200)
        plt.hist(transaction_amounts, **plot_options)
        plt.title("Individual Transaction Amounts", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Number of Orders")

def lifetime_value(customer_ids, transaction_amounts, graph=True, text=True, plot_options={}):
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
        plt.hist(total_vals, **plot_options)
        plt.title("Lifetime Value of Customers (to date)", fontsize=24, fontname='Pier Sans')
        plt.ylabel("Frequency")
        plt.xlabel("Lifetime Value")
