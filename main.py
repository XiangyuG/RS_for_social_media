import sys

import random
from random import randrange

def gen_recommend(curr_product, curr_customer, whitelist, blacklist, profit_l):
    ret_l = []
    if len(whitelist[curr_customer]) == 0:
        for i in range(len(profit_l)):
           if i == curr_product or i in blacklist[curr_customer]:
               continue
           else:
               if len(ret_l) == 0:
                   ret_l.append(i)
               elif len(ret_l) == 1:
                   if profit_l[i] > profit_l[ret_l[0]]:
                       ret_l.insert(0, i)
                   else:
                       ret_l.append(i)
               else:
                   if profit_l[i] > profit_l[ret_l[0]]:
                       ret_l.insert(0, i)
                       ret_l.pop()
                   elif profit_l[i] > profit_l[ret_l[1]]:
                       ret_l[1] = i
        return ret_l
    if len(whitelist[curr_customer]) == 1:
        ret_l.append(whitelist[curr_customer][0])
    else:
        for i in range(len(whitelist[curr_customer])):
            if len(ret_l) == 0:
                ret_l.append(whitelist[curr_customer][i])
            elif profit_l[whitelist[curr_customer][i]] > profit_l[ret_l[0]]:
                ret_l[0] = whitelist[curr_customer][i]
    ret_l.append(-1)
    curr_max = 0
    for i in range(len(profit_l)):
        if i == curr_product or i in blacklist[curr_customer]:
            continue
        else:
            if profit_l[i] > curr_max:
                curr_max = profit_l[i]
                ret_l[1] = i
    if ret_l[1] == -1:
        ret_l.pop()
    return ret_l

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
        num_preferred_product = randrange(2, upper_bound)
        cnt = 0
        while cnt < num_preferred_product:
            prod_num = randrange(0, num_products - 1)
            if prod_num not in customer_pref[i]:
                customer_pref[i].append(prod_num)
                cnt += 1
    print("profit_l =", profit_l)
    print("customer_pref =", customer_pref)
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
        random_idx = randrange(0, len(customer_pref[cus]) - 1)
        product = customer_pref[cus][random_idx]
        product_to_buy_l.append(product)
    # Case1: optimal strategy
    case1_profit = 0
    for i in range(customer_show_cnt):
        curr_product = product_to_buy_l[i]
        curr_customer = show_customer_l[i]
        # the recommendation system will recommend two more food
        #TODO: one from whitelist with maximum profit, one randomly from others whose profit is higher than the whitelist one
        # the customers will decide to whether to buy the recommended food or not
        # if the recommended is in their preference, the customer will buy it
        recommend_l = gen_recommend(curr_product, curr_customer, whitelist, blacklist, profit_l) #TODO: get recommended
        profit_this_turn = 0
        profit_this_turn += profit_l[curr_product]
        for mem in recommend_l:
           if mem in customer_pref[curr_customer]:
               profit_this_turn += profit_l[mem]
               if mem not in whitelist[curr_customer]:
                   whitelist[curr_customer].append(curr_product)
           else:
               if mem not in blacklist[curr_customer]:
                   blacklist[curr_customer].append(curr_product)
        # the system will updates its information based on the customers behavior
        if curr_product not in whitelist[curr_customer]:
            whitelist[curr_customer].append(curr_product)
        case1_profit += profit_this_turn
    print("case1_profit =", case1_profit)
    # Case2: randomly pick up one 
    case2_profit = 0
    recommend_l = []
    while len(recommend_l) < 2:
        rv = randrange(0, num_products - 1)
        if rv not in recommend_l:
            recommend_l.append(rv)
    for i in range(customer_show_cnt):
        curr_product = product_to_buy_l[i]
        curr_customer = show_customer_l[i]
        profit_this_turn = 0
        profit_this_turn += profit_l[curr_product]
        for mem in recommend_l:
           if mem in customer_pref[curr_customer]:
               profit_this_turn += profit_l[mem]
        case2_profit += profit_this_turn
    print("case2_profit =", case2_profit)
    
    # Case3: quickly stop
    case3_profit = 0
    '''
    for i in range(customer_show_cnt):
        curr_product = product_to_buy_l[i]
        curr_customer = show_customer_l[i]
        profit_this_turn = 0
        profit_this_turn += profit_l[curr_product]
        rec_l = one_recommend()
        case3_profit += profit_this_turn
    '''
if __name__ == '__main__':
    main(sys.argv)
