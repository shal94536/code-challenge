#This is to create all the Entities/Python classes as per the given use case in https://github.com/sflydwh/code-challenge

class customer:
    def __init__(self, key, verb, event_time, last_name, adr_city, adr_state):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.last_name = last_name
        self.adr_city = adr_city
        self.adr_state = adr_state
class siteVisit:
    def __init__(self, key, verb, event_time, customer_id, tags):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.tags = tags
class image:
    def __init__(self, key, verb, event_time, customer_id, camera_make, camera_model):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.camera_make = camera_make
        self.camera_model = camera_model
class order:
    def __init__(self, key, verb, event_time, customer_id, total_amount):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.total_amount = total_amount