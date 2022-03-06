import sys

import random
from random import randrange

def main(argv):
    if len(argv) != 6:
        print("Usage: python3", argv[0], "<number of different customers> <number of products> <lower bound of profit per product> <upper bound of profit per product> <number of customers showing>")
        sys.exit(1)
    num_customer = int(argv[1])
    num_products = int(argv[2])
    low_profit = int(argv[3])
    high_profit = int(argv[4])
    assert low_profit <= high_profit, "profit lower bound should not be greater than profit upper bound"
    customer_show_cnt = int(argv[5])

    random.seed(10)

    # build a list of length num_products, each member show a product's profit
    profit_l = []
    for i in range(num_products):
        profit_l.append(randrange(low_profit, high_profit))
    # build a dictionary showing the preference of a particular customer and the product he/she must buy if it shows
    customer_pref = {}
    for i in range(num_customer):
        customer_pref[i] = []
        upper_bound = num_products / 5  # assume on average, a customer would like around 20% of all products
        num_preferred_product = randrange(1, upper_bound)
        for j in range(num_preferred_product):
            prod_num = randrange(0, num_products - 1)
            if prod_num not in customer_pref[i]:
                customer_pref[i].append(prod_num)
    print("--------------database generation finishes----------------")

    # showing the recommendation system
    blacklist = {} #key: customer's name, val: [] of products the key customer dislikes
    whitelist = {} #key: customer's name, val: [] of products that the customer like
    for i in range(num_customer):
        blacklist[i] = []
        whitelist[i] = []
    # generate the number of customers who show up in the resturant
    show_customer_l = []
    product_to_buy_l = []
    for i in range(customer_show_cnt):
        cus = randrange(0, num_customer - 1)
        show_customer_l.append(cus)
        # each customer will randomly pick one food to buy
        random_idx = randint(0, len(customer_pref[i]) - 1)
        product = customer_pref[i][random_idx]
        product_to_buy_l.append(product)
    # Case1: optimal strategy
    for i in range(customer_show_cnt):
        # the recommendation system will recommend two more food
        #TODO: one from whitelist with maximum profit, one randomly from others whose profit is higher than the whitelist one
        # the customers will decide to whether to buy the recommended food or not
        # TODO: if the recommended is in their preference, the customer will buy it
        # the system will updates its information based on the customers behavior
    # Case2: randomly pick up one 
    # Case3: only recommend one
    print("profit_l =", profit_l)
    print("customer_pref =", customer_pref)

if __name__ == '__main__':
    main(sys.argv)
