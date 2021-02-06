import json
from collections import defaultdict
from Entities import customer, siteVisit, image, order
from datetime import datetime, timedelta
from contextlib import redirect_stdout
def Ingest(data, dict):
    for i in data:
        if i['type'] == 'CUSTOMER':
            key = i['key']
            verb = i['verb']
            event_time = i['event_time']
            last_name = i['last_name']
            adr_city = i['adr_city']
            adr_state = i['adr_state']
            cust_details = customer(key, verb, event_time, last_name, adr_city, adr_state)
            if key not in dict:
                dict[key] = defaultdict(list)
            dict[key]['CUSTOMER'].append(cust_details)

        elif i['type'] == 'SITE_VISIT':
            key = i['key']
            verb = i['verb']
            event_time = i['event_time']
            customer_id = i['customer_id']
            tags = i['tags']
            site_details = siteVisit(key, verb, event_time, customer_id, tags)
            dict[customer_id]['SITE_VISIT'].append(site_details)

        elif i['type'] == 'IMAGE':
            key = i['key']
            verb = i['verb']
            event_time = i['event_time']
            customer_id = i['customer_id']
            camera_make = i['camera_make']
            camera_model = i['camera_model']
            image_details = image(key, verb, event_time, customer_id, camera_make, camera_model)
            dict[customer_id]['IMAGE'].append(image_details)

        elif i['type'] == 'ORDER':
            key = i['key']
            verb = i['verb']
            event_time = i['event_time']
            customer_id = i['customer_id']
            total_amount = i['total_amount']
            order_details = order(key, verb, event_time, customer_id, total_amount)
            dict[customer_id]['ORDER'].append(order_details)
        else:
            print('This entity Type is out of given classes')
            exit(1)
    return dict
# Function to get top X customers
def topXSimpleLTVCustomers(top_Customer, dict):
    cust_ltv = {}
    t = 10
    ltv = 0
    for c in dict.keys():

        no_of_visit = 0
        total_amount = 0
        # Expenditure of customer
        order = dict[c].get('ORDER', None)
        if order is not None:
            for o in order:
                total_amount = total_amount + float(o.total_amount.split(' ')[0].strip())

        # All visits

        visit = dict[c].get('SITE_VISIT', None)
        if visit is not None:
            no_of_visit = len(visit)

        curr = dict[c].get('CUSTOMER')[0].event_time
        curr = datetime.strptime(curr, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        first_week = curr - timedelta(
            days=curr.weekday())  # Assuming the given date in the file as start week and taking the starting week of the customer
        this_week = datetime.now().date() - timedelta(days=datetime.now().date().weekday())  # Current week
        total_weeks = int(abs((first_week - this_week).days)) / 7
        if total_weeks == 0:  # check if visit is current week
            total_weeks = 1
        if no_of_visit > 0:  # Divide-by-zero check
            avg_cust_amount = total_amount / no_of_visit
            site_visit_per_week = no_of_visit / total_weeks
            a = avg_cust_amount * site_visit_per_week
            ltv = 52 * a * t
        else:
            ltv = 0
        cust_ltv[c] = ltv
    result = []
    if top_Customer > len(dict):
        print ('Number of top customers that you want to see in the result are more than whatever you passed in input file.Hence printing all')
        top_Customer = len(dict)
    for i in sorted(cust_ltv, key=cust_ltv.get, reverse=True):
        result.append((i, cust_ltv.get(i)))
    with open('../output/output.txt', 'a') as f:
        f.truncate(0)
    for k in range(0, top_Customer):
        with open('../output/output.txt', 'a') as f:
            with redirect_stdout(f):
                #Write result to file
                print('Customer id is ' + str(result[k][0]) + ' and Lifetime Value of this customer is  ' + str(
                    result[k][1]))
      ## print to console
        print('Customer id is ' + str(result[k][0]) + ' and Lifetime Value of this customer is  ' + str(result[k][1]))


