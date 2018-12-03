import uuid
import math
import numpy as np
import random

# Process positions
CHOOSING_ORDER = "Choosing Order"
WAITING_TO_ORDER = "Waiting to Order"
ORDERING_SANDWICH = "Ordering Sandwich"

WAIT_FOR_FLIP_RESOURCES = "Waiting for Flip Resources"
FLIP_STATION = "Stations being flipped"

# PROCESS 1
# DECIDE_ON_ORDER (Delay)
# WAIT_FOR_SANDWICH_RESOURCES (Seize Employee & Sandwich Station)
# for: each sandwich
# GET_SANDWICH_INGREDIENTS (Seize Sandwich ingredients)
# MAKE_WRAP_SANDWICH
# end for
# RELEASE_SANDWICH_MAKER_STATION (Release Employee and Sandwich Station )
# WAIT_FOR_CASHIER (Seize Employee)
# CHECKING_OUT
# RELEASE_CASHIER (Release Employee)
# <Customer Served>


# PROCESS 2
# WAIT_FOR_FLIP_RESOURCES (Seize Employee & 2 Sandwich Stations)
# FLIP_STATION
# RELEASE_FLIP_RESOURCES (Release Employee and Sandwich Stations )

# PROCESS 3
# If sandwichIngredients - 2 <= 0
# WAIT_FOR_REFILL_EMPLOYEE (Seize Employee)
# WAIT_FOR_INGREDIENTS
# RELEASE_REFILL_EMPLOYEE (Release Employee)

# Each loop is in minutes
currentTime = 0
currentTimeDelta = 0

SANDWICH_STATION_CLEANING_TIME = XXX

# Store Details
employees = availableEmployees = 4
sandwichStations = availableSandwichStations = 4
registers = availableRegisters = 1
sandwichIngredients = 15  # 1 is all the ingredients needed for a sandwich

customer_delays = {
    CHOOSING_ORDER: (min, max),
    WAITING_TO_ORDER: (min, max),
    ORDERING_SANDWICH: (min, max)
}

customer_seizures = {
    WAIT_FOR_FLIP_RESOURCES: [('EMPLOYEES', 1), ('STATIONS', 2), ('SANDWICH_INGREDIENTS', -1)],
    WAITING_TO_ORDER: [],
    ORDERING_SANDWICH: []
}

resources = {
    EMPLOYEES: 4,
    STATIONS: 4
}


def switch(option, tree):
    if option in tree:
        return tree[option]
    elif "default" in tree:
        return tree["default"]
    else:
        raise ValueError("NO DEFAULT ON TREE")


class Customer:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.sandwiches = random.choice([i for i in range(10)])
        self.process_position = CHOOSING_ORDER

    def get_process_position(self):
        return self.process_position

    def update_position(self, new_position):
        self.process_position = new_position


def customer_seizure(process_position, customer):
    seizures = switch(process_position, customer_seizures)
    for seizure in seizures:
        # Check the resource for sufficient
        # -- on the resource until customer has seized enough

    customer.seizures = seizures


def delay_customers(customers, process_position):
    for customer in customers:
        delay = switch(process_position, customer_delays)


def get_delayed_customers(process_position, waiting_since):
    returned_customers = []
    for customer in customers:
        if customer.get_process_position() == process_position and customer.waiting_since > waiting_since:
            if len(customer.seizures) > 0:
                release()
            returned_customers.append(customer)
    return returned_customers


def simulate_timestep():
    # Get the number of customers entering the shop
    num_customers_arriving = customer_arrivals.pop(0)

    # Create new customers
    new_customers = []
    for i in range(num_customers_arriving):
        new_customers.append(Customer())

    customers_ready_to_order = get_delayed_customers(
        WAITING_TO_ORDER, currentTime)

    # Decide on order


print(Customer().sandwiches)
