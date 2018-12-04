import uuid
import math
import numpy as np
import random

# Statistics
statistics = {
    'customersServed': 0
}

# Resources
EMPLOYEES = "EMPLOYEES"
STATIONS = "STATIONS"
REGISTERS = "REGISTERS"
SANDWICH_INGREDIENTS = "SANDWICH_INGREDIENTS"

# Processes
DECIDE_ON_ORDER = "DECIDE_ON_ORDER"
WAIT_FOR_SANDWICH_RESOURCES = "WAIT_FOR_SANDWICH_RESOURCES"
WAIT_FOR_SANDWICH_INGREDIENTS = "WAIT_FOR_SANDWICH_INGREDIENTS"
MAKE_WRAP_SANDWICH = "MAKE_WRAP_SANDWICH"
WAIT_FOR_CASHIER = "WAIT_FOR_CASHIER"
CHECKING_OUT = "CHECKING_OUT"

# PROCESS 1
# DECIDE_ON_ORDER (Delay)
# WAIT_FOR_SANDWICH_RESOURCES (Seize Employee & Sandwich Station)
# for: each sandwich
# WAIT_FOR_SANDWICH_INGREDIENTS (Seize Sandwich ingredients)
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
    WAIT_FOR_SANDWICH_RESOURCES: [
        (EMPLOYEES, 1),
        (STATIONS, 1)
    ],
    WAIT_FOR_SANDWICH_INGREDIENTS: [
        (SANDWICH_INGREDIENTS, 1)
    ],
    WAIT_FOR_CASHIER: [
        (EMPLOYEES, 1),
        (REGISTERS, 1)
    ]
}

# Resources
resources = {
    EMPLOYEES: {
        'available': 4,
        'return': True
    },
    STATIONS: {
        'available': 4,
        'return': True
    },
    REGISTERS: {
        'available': 1,
        'return': True
    },
    SANDWICH_INGREDIENTS: {
        'available': 15,
        'return': False
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

    # Customer attempts to seize 
    def set_seize_process(self, process_position):

        self.process_position = process_position
        self.seized = False

    def attempt_seize(self):
        process = customer_seizures[self.process_position]

        # Print error if seized isn't false
        if self.seized != False:
            print("ERROR: Already seized")
            return

        # Determines if resources are available
        resourcesAvailable = True

        # For each resource this seizure requires
        for requiredResource in process:
            # Get resource details
            resource = requiredResource[0]
            quantity = requiredResource[1]

            # If not enough of the resource exists
            if resources[resource]['available'] < quantity:
                # Update resourcesAvailable flag
                resourcesAvailable = False
                break

        # Set the self.seized variable and update global resources
        if resourcesAvailable:

            # Update customers position when resources are seized
            self.seized = True

            for requiredResource in process:
                # Get resource details
                resource = requiredResource[0]
                quantity = requiredResource[1]

                print("[" + str(self.uuid) +  "] is removing resource(" + resource + ") by " + str(quantity) + " for process " + self.process_position)
                resources[resource]['available'] -= quantity

        

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

# Gets users that have been fully delayed as process_position
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
        if customer.process_position_end <= currentTime:
            delayed_customers.append( customer.uuid )

    return delayed_customers

# Gets users based on seizure status at process_position 
def get_seizure_customers(process_position, seizureStatus):
    global currentTime

    customers_waiting_on_seizure = []

    if not process_position in customer_seizures:
        print( "ERROR: Invaid seizure process" )
        exit(1)

    # Customers at current position
    customers_at_position = get_customers_at_position(process_position)

    # For each customer at position
    for customer in customers_at_position:
        # Overwrite customer with object
        customer = customers[customer]

        # Determine if the customer has been fully delayed
        if customer.seized == seizureStatus:
            customers_waiting_on_seizure.append( customer.uuid )

    return customers_waiting_on_seizure

# Returns resources based on a seize process
def return_resources(process_position):
    process = customer_seizures[process_position]

    # Return each resource that should be returned
    for requiredResource in process:
        # Get resource details
        resource = requiredResource[0]
        quantity = requiredResource[1]

        # Get global resource
        globalResource = resources[resource]

        # Skip non returnable resources
        if globalResource['return'] == False:
            continue

        globalResource['available'] += quantity

# Test 1 customer
customer = Customer()
customers[customer.uuid] = customer

# Simulate a single timestep
def simulateTimeStep():
    global statistics, customers, currentTime, timeDelta
    print("TIME=" + str(currentTime))

    # TEMP: 1/6 chance of generating customer every minute
    #if( random.randint(0, 25) == 0 ):
    #    customer = Customer()
    #    customers[customer.uuid] = customer

    # For each customer that has decided: Attempt to seize resources to make sandwich
    for customer in get_delayed_customers(DECIDE_ON_ORDER):
        customer = customers[customer]

        # Attempt to set customer in seize process
        customer.set_seize_process(WAIT_FOR_SANDWICH_RESOURCES)

    # For each customer that is waiting for sandwich resources: Attempt to seize resources to make sandwich
    for customer in get_seizure_customers(WAIT_FOR_SANDWICH_RESOURCES, False): 
        customer = customers[customer]

        customer.attempt_seize()

    # For each customer that has seized sandwich resources: Attempt to seize sandwich ingredients
    for customer in get_seizure_customers(WAIT_FOR_SANDWICH_RESOURCES, True): 
        customer = customers[customer]

        customer.set_seize_process(WAIT_FOR_SANDWICH_INGREDIENTS)

    # For each customer that is waiting for sandwich ingredients: Attempt to seize sandwich ingredients
    for customer in get_seizure_customers(WAIT_FOR_SANDWICH_INGREDIENTS, False): 
        customer = customers[customer]
        
        customer.attempt_seize()

    # For each customer that has seized sandwich ingredients: Begin sandwich making delay
    for customer in get_seizure_customers(WAIT_FOR_SANDWICH_INGREDIENTS, True): 
        customer = customers[customer]

        customer.set_delay_process(MAKE_WRAP_SANDWICH)

    # For each customer that has sandwich made: Get in checkout line or wait for next sandwich
    for customer in get_delayed_customers(MAKE_WRAP_SANDWICH):
        customer = customers[customer]

        # Update sandwich count
        customer.sandwiches -= 1

        # If all sandwiches are made, wait for checkout
        if customer.sandwiches <= 0:
            return_resources(WAIT_FOR_SANDWICH_RESOURCES)
            customer.set_seize_process(WAIT_FOR_CASHIER)
        else:
            customer.set_seize_process(WAIT_FOR_SANDWICH_INGREDIENTS)

    # For each customer that is waiting for a cashier: Attempt to seize cashier and register
    for customer in get_seizure_customers(WAIT_FOR_CASHIER, False): 
        customer = customers[customer]
        
        customer.attempt_seize()

    # Delete customers that are done.
    for customer in get_seizure_customers(WAIT_FOR_CASHIER, True):
        statistics['customersServed'] += 1
        del customers[customer]

    # PROCESS 1
    # DECIDE_ON_ORDER (Delay)
    # WAIT_FOR_SANDWICH_RESOURCES (Seize Employee & Sandwich Station)
    # for: each sandwich
    # WAIT_FOR_SANDWICH_INGREDIENTS (Seize Sandwich ingredients)
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

print( resources )
print( 'Customers Served: ' + str(statistics['customersServed']) )
print( 'Customers Deciding on order: ' + str(get_delayed_customers(DECIDE_ON_ORDER)) )
print( 'Customers Waiting for sandwich resources: ' + str(get_seizure_customers(WAIT_FOR_SANDWICH_RESOURCES, True)) )
print( 'Customers waiting for sandwich ingredients: ' + str(get_seizure_customers(WAIT_FOR_SANDWICH_INGREDIENTS, True)) )
print( 'Customers waiting on sandwich making: ' + str(get_delayed_customers(MAKE_WRAP_SANDWICH)) )
print( 'Customers waiting on cashier: ' + str(get_seizure_customers(WAIT_FOR_CASHIER, False)) )