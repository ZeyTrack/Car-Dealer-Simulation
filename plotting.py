import matplotlib.pyplot as plt

class Plotting:
    @staticmethod
    def plot_inventory_over_time(simulator):
        plt.figure(figsize=(10, 5))
        plt.plot(simulator.time_axis, simulator.amount_axis, marker='o', linestyle='-', color='b')
        plt.title('Ending Inventory - Shortage Over Time')
        plt.xlabel('Time (Days)')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_showroom_over_time(simulator):
        plt.figure(figsize=(10, 5))
        plt.plot(simulator.time_axis, simulator.amount_axis2, marker='o', linestyle='-', color='b')
        plt.title('Ending Showroom - Shortage Over Time')
        plt.xlabel('Time (Days)')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_combined_over_time(simulator):
        plt.figure(figsize=(10, 5))
        plt.plot(simulator.time_axis, simulator.amount_axis3, marker='o', linestyle='-', color='b')
        plt.title('Ending Inventory + Ending Showroom - Shortage Over Time')
        plt.xlabel('Time (Days)')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_inventory_showroom_levels(simulator):
        plt.figure(figsize=(12, 6))
        plt.plot(range(1, simulator.num_days + 1), simulator.ending_inventory_list, label='Ending Inventory')
        plt.plot(range(1, simulator.num_days + 1), simulator.ending_showroom_list, label='Ending Showroom')
        plt.xlabel('Day')
        plt.ylabel('Inventory Level')
        plt.title('Inventory and Showroom Levels Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_histogram_inventory(simulator):
        plt.figure(figsize=(10, 5))
        plt.hist(simulator.ending_inventory_list, bins=20, color='blue', edgecolor='black')
        plt.title('Histogram of Ending Inventory Levels')
        plt.xlabel('Ending Inventory Level')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_histogram_showroom(simulator):
        plt.figure(figsize=(10, 5))
        plt.hist(simulator.ending_showroom_list, bins=20, color='green', edgecolor='black')
        plt.title('Histogram of Ending Showroom Levels')
        plt.xlabel('Ending Showroom Level')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
