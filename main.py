import random
import matplotlib.pyplot as plt
import numpy as np


class InventorySimulator:
    def __init__(self, num_days):
        self.num_cycles = num_days / 3
        self.num_days = num_days
        self.max_inventory = 10
        self.max_showroom = 5
        self.max_total = self.max_inventory + self.max_showroom
        self.review_period_length = 3
        self.beginning_inventory = 3
        self.beginning_showroom = 4
        self.shortage = 0
        self.order_quantity = "-"
        self.order_lead_time = 2
        self.profit_per_car = 10000
        self.holding_cost_per_car = 1000
        self.order_cost = 20000
        self.initial_order_quantity = [5]
        self.shortage_days = 0
        self.ending_inventory_list = []
        self.ending_showroom_list = []
        self.shortage_days_list = []
        self.net_profit_list = []
        self.order_lead_time_list = []
        self.demand_list = []
        self.time_axis = []
        self.amount_axis = []
        self.amount_axis2 = []
        self.amount_axis3 = []

    def generate_demand(self, random_value):
        """Generate demand based on a random value."""
        if random_value < 0.20:
            return 0
        elif random_value < 0.54:
            return 1
        elif random_value < 0.90:
            return 2
        else:
            return 3

    def generate_lead_time(self, random_value):
        """Generate lead time based on a random value."""
        if random_value < 0.40:
            return 1
        elif random_value < 0.75:
            return 2
        else:
            return 3

    def simulate(self):
        """
        Run the simulation.
        Add your existing simulation logic here.
        """
        # Print table header
        print("{:<8} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
            "Cycle", "Day", "Begin Inv", "Begin Showroom", "Rand Demand", "Demand", "End Inv", "End Showroom",
            "Shortage", "Order", "Rand Lead Time", "Days to Arrive"
        ))
        for day in range(1, self.num_days + 1):
            # print(f"\nDay: {day}")
            # Generate a random demand for the day
            rand_demand = round(random.random(), 3)
            demand = self.generate_demand(rand_demand)
            self.demand_list.append(
                demand)  # Add the generated demand to the demand list for Experimental Average demand

            # Update inventory and showroom, calculate net profit for non-review days
            if demand > self.beginning_inventory and self.beginning_inventory + self.beginning_showroom >= demand:
                self.ending_inventory = 0
                self.ending_showroom = self.beginning_showroom - (demand - self.beginning_inventory)
            elif self.beginning_inventory + self.beginning_showroom < demand:
                self.ending_inventory = 0
                self.ending_showroom = 0
                self.shortage += demand - (self.beginning_inventory + self.beginning_showroom)
            elif demand < self.beginning_inventory and self.beginning_inventory + self.beginning_showroom > demand:
                self.ending_inventory = self.beginning_inventory - demand
                self.ending_showroom = self.beginning_showroom
            else:
                # Handle the remaining cases and define ending_inventory and ending_showroom
                self.ending_inventory = self.beginning_inventory - demand
                self.ending_showroom = self.beginning_showroom

            if day % self.review_period_length != 0:
                self.order_quantity = "-"
                rand_lead_time = "-"

                # Calculate net profit for non-review days
                net_profit = self.profit_per_car * min(demand,
                                                       self.beginning_showroom) - self.holding_cost_per_car * min(
                    demand, self.beginning_showroom)
                self.net_profit_list.append(net_profit)  # assuming net profit

            # Update order arrival time for non-review days
            if self.order_lead_time != "-" and self.order_lead_time > 0:
                self.order_lead_time -= 1

            # Review day logic
            if day % self.review_period_length == 0:
                # Calculate order quantity, generate lead time, and update order arrival time
                self.order_quantity = 15 - (self.ending_inventory + self.ending_showroom) + self.shortage
                self.initial_order_quantity.append(self.order_quantity)
                rand_lead_time = round(random.random(), 3)
                self.order_lead_time = self.generate_lead_time(rand_lead_time)  # order_lead_time means the lead time

                # Calculate net profit for review days, including order cost
                net_profit = self.profit_per_car * min(demand,
                                                       self.beginning_showroom) - self.holding_cost_per_car * min(
                    demand, self.beginning_showroom) - self.order_cost
                self.net_profit_list.append(net_profit)  # assuming net profit

                self.order_lead_time_list.append(self.order_lead_time)  # for Experimental Average Lead Time

            # Print table row (you may want to modify this part based on your specific output format)
            print("{:<8} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
                (day - 1) // self.review_period_length + 1, day, self.beginning_inventory, self.beginning_showroom,
                rand_demand, demand, self.ending_inventory, self.ending_showroom, self.shortage, self.order_quantity,
                rand_lead_time, self.order_lead_time
            ))

            # Store results for analysis
            self.ending_inventory_list.append(self.ending_inventory)
            self.ending_showroom_list.append(self.ending_showroom)
            if self.shortage > 0:
                self.shortage_days += 1

            # Calculate amount (ending_inventory - shortage)
            amount = self.ending_inventory - self.shortage
            amount2 = self.ending_showroom - self.shortage
            amount3 = self.ending_inventory + self.ending_showroom - self.shortage
            self.amount_axis.append(amount)
            self.amount_axis2.append(amount2)
            self.amount_axis3.append(amount3)
            self.time_axis.append(day)  # Store day for the x-axis

            # Process order arrival
            if self.order_lead_time == 0:
                self.order_quantity = self.initial_order_quantity.pop()
                self.initial_order_quantity = []
                self.order_quantity -= self.shortage
                self.shortage = 0
                self.beginning_showroom = self.ending_showroom + self.order_quantity
                if self.beginning_showroom > self.max_showroom:
                    self.beginning_inventory = self.ending_inventory + (self.beginning_showroom - self.max_showroom)
                    self.beginning_showroom = self.max_showroom
                self.order_lead_time = "-"
            else:
                self.beginning_inventory = self.ending_inventory
                self.beginning_showroom = self.ending_showroom

    def simulate_with_review_period(self, review_period_length):
        print(f"Review Period Length: {review_period_length}")
        self.review_period_length = review_period_length
        self.simulate()


if __name__ == "__main__":
    num_days = int(input("Enter number of days: "))
    simulator = InventorySimulator(num_days)  # num_days   num_cycles
    simulator.simulate()

    # Calculate requested metrics
    average_ending_inventory = np.mean(simulator.ending_inventory_list)
    average_ending_showroom = np.mean(simulator.ending_showroom_list)
    average_net_profit = np.mean(simulator.net_profit_list)
    total_net_profitt = sum(simulator.net_profit_list)  # Calculate net profit for the current review period
    experimental_average_demand = np.mean(simulator.demand_list)
    experimental_average_lead_time = np.mean(simulator.order_lead_time_list)

    # Theoretical average demand and lead time
    theoretical_average_demand = 0.20 * 0 + 0.34 * 1 + 0.36 * 2 + 0.10 * 3
    theoretical_average_lead_time = 0.40 * 1 + 0.35 * 2 + 0.25 * 3

    # Print results
    print("\nResults:")
    print(f"1. Average Ending Units in Showroom: {average_ending_showroom:.2f}")
    print(f"   Average Ending Inventory: {average_ending_inventory:.2f}")
    print(f"2. Number of Days with Shortage Condition: {simulator.shortage_days}")
    print(f"3. Average Net Profit: {average_net_profit:.2f}")
    # print(f"   Net Profit: {total_net_profitt:.2f}")
    print(f"4. Theoretical Average Demand: {theoretical_average_demand:.2f}")
    print(f"   Experimental Average Demand: {experimental_average_demand:.2f}")
    if theoretical_average_demand == experimental_average_demand:
        print("4. Theoretical average demand MATCHES the experimental one")
    else:
        print("4. Theoretical average demand NOT MATCHES the experimental one")
    print(f"5. Theoretical Average Lead Time: {theoretical_average_lead_time:.2f}")
    print(f"   Experimental Average Lead Time: {experimental_average_lead_time:.2f}")
    if theoretical_average_lead_time == experimental_average_lead_time:
        print("5. Theoretical average leadTime MATCHES the experimental one")
    else:
        print("5. Theoretical average leadTime NOT MATCHES the experimental one")

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(simulator.time_axis, simulator.amount_axis, marker='o', linestyle='-', color='b')
    plt.title('Ending Inventory - Shortage Over Time')
    plt.xlabel('Time (Days)')
    plt.ylabel('Amount')
    plt.grid(True)
    plt.show()

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(simulator.time_axis, simulator.amount_axis2, marker='o', linestyle='-', color='b')
    plt.title('Ending showroom - Shortage Over Time')
    plt.xlabel('Time (Days)')
    plt.ylabel('Amount')
    plt.grid(True)
    plt.show()

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(simulator.time_axis, simulator.amount_axis3, marker='o', linestyle='-', color='b')
    plt.title('Ending Inventory + Ending showroom - Shortage Over Time')
    plt.xlabel('Time (Days)')
    plt.ylabel('Amount')
    plt.grid(True)
    plt.show()

    # Inventory and Showroom Levels Over Time: Plot the ending inventory and ending showroom levels for each day.
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, simulator.num_days + 1), simulator.ending_inventory_list, label='Ending Inventory')
    plt.plot(range(1, simulator.num_days + 1), simulator.ending_showroom_list, label='Ending Showroom')
    plt.xlabel('Day')
    plt.ylabel('Inventory Level')
    plt.title('Inventory and Showroom Levels Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Plotting Histogram of Ending Inventory Levels
    plt.figure(figsize=(10, 5))
    plt.hist(simulator.ending_inventory_list, bins=20, color='blue', edgecolor='black')
    plt.title('Histogram of Ending Inventory Levels')
    plt.xlabel('Ending Inventory Level')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Plotting Histogram of Ending Showroom Levels
    plt.figure(figsize=(10, 5))
    plt.hist(simulator.ending_showroom_list, bins=20, color='green', edgecolor='black')
    plt.title('Histogram of Ending Showroom Levels')
    plt.xlabel('Ending Showroom Level')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    
    # Perform the optimization
    best_review_period = None
    max_net_profit = float('-inf')

    # Try different review period lengths within a specified range
    for review_period in range(1, 11):  # Adjust the range as needed
        simulator = InventorySimulator(num_days)
        simulator.simulate_with_review_period(review_period)

        # Calculate net profit for the current review period
        total_net_profit = sum(simulator.net_profit_list)

        # Update the best review period if the current one is more profitable
        if total_net_profit > max_net_profit:
            max_net_profit = total_net_profit
            best_review_period = review_period

    # Print the optimal review period
    print(f"The optimal review period for maximizing net profit is: {best_review_period}")
    # Print the results of the sensitivity analysis
    print("\ 6. nSensitivity Analysis Results:")
    print(f"Best Review Period Length: {best_review_period}")
    print(f"Maximized Net Profit: {max_net_profit:.2f}")