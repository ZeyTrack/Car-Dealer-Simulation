import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from main import InventorySimulator
from plotting import Plotting

class InventorySimulatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Simulator GUI")
        self.geometry("800x600")

        self.simulator = InventorySimulator(1)  # Initial setup with num_days=1

        # Create widgets
        self.label_num_days = ttk.Label(self, text="Enter number of days:")
        self.entry_num_days = ttk.Entry(self)
        self.button_run_simulation = ttk.Button(self, text="Run Simulation", command=self.run_simulation)
        self.label_output = ttk.Label(self, text="Simulation results will be displayed here.")

        # Layout widgets
        self.label_num_days.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_num_days.grid(row=0, column=1, padx=10, pady=10)
        self.button_run_simulation.grid(row=1, column=0, columnspan=2, pady=10)
        self.label_output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def run_simulation(self):
        try:
            num_days = int(self.entry_num_days.get())
            self.simulator = InventorySimulator(num_days)
            self.simulator.simulate()

             # Calculate requested metrics
            average_ending_inventory = np.mean(self.simulator.ending_inventory_list)
            average_ending_showroom = np.mean(self.simulator.ending_showroom_list)
            average_net_profit = np.mean(self.simulator.net_profit_list)
            total_net_profit = sum(self.simulator.net_profit_list)
            experimental_average_demand = np.mean(self.simulator.demand_list)
            experimental_average_lead_time = np.mean(self.simulator.order_lead_time_list)

            # Theoretical average demand and lead time
            theoretical_average_demand = 0.20 * 0 + 0.34 * 1 + 0.36 * 2 + 0.10 * 3
            theoretical_average_lead_time = 0.40 * 1 + 0.35 * 2 + 0.25 * 3

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

            # Display results in the GUI
            results = (
                f"Results:\n"
                f"1. Average Ending Units in Showroom: {average_ending_showroom:.2f}\n"
                f"   Average Ending Inventory: {average_ending_inventory:.2f}\n"
                f"2. Number of Days with Shortage Condition: {self.simulator.shortage_days}\n"
                f"3. Average Net Profit: {average_net_profit:.2f}\n"
                f"4. Theoretical Average Demand: {theoretical_average_demand:.2f}\n"
                f"   Experimental Average Demand: {experimental_average_demand:.2f}\n"
                f"   Theoretical average demand {'MATCHES' if theoretical_average_demand == experimental_average_demand else 'NOT MATCHES'} the experimental one\n"
                f"5. Theoretical Average Lead Time: {theoretical_average_lead_time:.2f}\n"
                f"   Experimental Average Lead Time: {experimental_average_lead_time:.2f}\n"
                f"   Theoretical average leadTime {'MATCHES' if theoretical_average_lead_time == experimental_average_lead_time else 'NOT MATCHES'} the experimental one\n"
                f"6. Sensitivity Analysis Results:\n"
                f"   Best Review Period Length: {best_review_period}\n"
                f"   Maximized Net Profit: {max_net_profit:.2f}"
            )

            self.label_output.config(text=results)

            # Plot histograms in GUI
            Plotting.plot_inventory_over_time(self.simulator)
            Plotting.plot_showroom_over_time(self.simulator)
            Plotting.plot_combined_over_time(self.simulator)
            Plotting.plot_inventory_showroom_levels(self.simulator)
            Plotting.plot_histogram_inventory(self.simulator)
            Plotting.plot_histogram_showroom(self.simulator)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of days.")


if __name__ == "__main__":
    app = InventorySimulatorGUI()
    app.mainloop()
