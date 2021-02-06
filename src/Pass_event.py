import sys
import json
from collections import defaultdict
from Entities import customer,siteVisit,image,order
from datetime import datetime, timedelta
import Cust_LTV
#Must pass the top number of customers and input file as argumenets
if len(sys.argv)!=3:
	print('Input arguments are not enough.Please read Runbook file for details to run this code. Exit with code 1')
	exit(1)
file_Name=sys.argv[2]
top_Customer=int(sys.argv[1])

dict={}

if top_Customer <0:
	print('Customer count can never be less than zero... Exit......')
	exit(1)
with open ('../input/'+file_Name) as file:
	data=json.load(file)
dict=Cust_LTV.Ingest(data,dict)
Cust_LTV.topXSimpleLTVCustomers(top_Customer,dict)