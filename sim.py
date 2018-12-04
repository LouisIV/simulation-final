import uuid
import math
import numpy as np
import random

# Resources
EMPLOYEES = "EMPLOYEES"
STATIONS = "STATIONS"
REGISTERS = "REGISTERS"
SANDWICH_INGREDIENTS = "SANDWICH_INGREDIENTS"

# Processes
DECIDE_ON_ORDER = "DECIDE_ON_ORDER"
WAIT_FOR_SANDWICH_RESOURCES = "WAIT_FOR_SANDWICH_RESOURCES"
GET_SANDWICH_INGREDIENTS = "GET_SANDWICH_INGREDIENTS"
MAKE_WRAP_SANDWICH = "MAKE_WRAP_SANDWICH"
WAIT_FOR_CASHIER = "WAIT_FOR_CASHIER"
CHECKING_OUT = "CHECKING_OUT"

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
simulationLength = 60 * 8
timeDelta = 1 # Move the simulation forward in minutes

# Store Details
employees = 4
sandwichStations = 4
registers = 1

customers = {

}

# Delays
customer_delays = {
    DECIDE_ON_ORDER: {
        "min": 1,
        "max": 5
    },
    MAKE_WRAP_SANDWICH: {
        "min": 1,
        "max": 2
    },
    CHECKING_OUT: {
        "min": 1,
        "max": 2
    }
}

# Seizures
customer_seizures = {
    GET_SANDWICH_INGREDIENTS: [
        (SANDWICH_INGREDIENTS, 1)
    ],
    WAIT_FOR_CASHIER: [
        (EMPLOYEES, 1)
    ]
}

# Resources
resources = {
    EMPLOYEES: {
        'available': 4,
        'release': True
    },
    STATIONS: {
        'available': 4,
        'release': True
    },
    REGISTERS: {
        'available': 1,
        'release': True
    },
    SANDWICH_INGREDIENTS: {
        'available': 15,
        'release': False
    }
}

# Represents a single customer
class Customer:
    def __init__(self):
        # Unique ID for each customer
        self.uuid = uuid.uuid1()

        # The number of sandwiches the customer wants
        self.sandwiches = random.choice([i for i in range(10)])

        # The current position the customer is in 
        self.process_position = DECIDE_ON_ORDER

        # Set inital position
        self.set_delay_process(DECIDE_ON_ORDER)

    # Delay the customer
    def set_delay_process(self, process_position):
        process = customer_delays[process_position]

        self.process_position = process_position
        self.process_position_end = currentTime + random.randint( process['min'], process['max'] )

# Get customers currently at a position
def get_customers_at_position(process_position):
    # List of customer UUIDs who are currently delayed at the position
    customers_at_position = []

    # For each customer
    for customer in customers.values():
       
        # If the customer is at the correct position, add them to customers_at_position array
        if (customer.process_position == process_position):
            customers_at_position.append( customer.uuid )

    return customers_at_position

# Gets all users that have been fully delayed
def get_delayed_customers(process_position):
    global currentTime

    delayed_customers = []

    if not process_position in customer_delays:
        print( "ERROR: Invaid delay process" )
        exit(1)

    # Customers at current position
    customers_at_position = get_customers_at_position(process_position)

    # For each customer at position
    for customer in customers_at_position:
        # Overwrite customer with object
        customer = customers[customer]

        # Determine if the customer has been fully delayed
        if customer.process_position_end == currentTime:
            delayed_customers.append( customer.uuid )

    return delayed_customers

# Simulate a single timestep
def simulateTimeStep():
    global customers, currentTime, timeDelta

    # TEMP: 1/6 chance of generating customer every minute
    if( random.randint(0, 6) == 0 ):
        customer = Customer()
        customers[customer.uuid] = customer

    customers_decided = get_delayed_customers(DECIDE_ON_ORDER)
    for customer in customers_decided:
        del customers[customer]

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

    # Update current time
    currentTime += timeDelta


while(currentTime <= simulationLength):
    simulateTimeStep()