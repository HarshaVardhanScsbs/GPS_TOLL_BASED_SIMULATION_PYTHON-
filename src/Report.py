import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

def display_vehicle_report():
    vehicle_simulation_results = pd.read_excel('vehicle_simulation_results.xlsx', index_col='vehicle_id')
    vehicle_data = pd.read_excel('/vehicle_data.xlsx', index_col='vehicle_id')

    def display_vehicle_distance_chart():
        vehicle_numbers = vehicle_simulation_results.index.tolist()
        distances_covered = vehicle_simulation_results['distance_travelled'].tolist()

        fig, ax = plt.subplots(figsize=(7, 6))
        bars = ax.bar(vehicle_numbers, distances_covered, color='skyblue')
        ax.set_xlabel('Vehicle Number')
        ax.set_ylabel('Distance Covered')
        ax.set_title('Distance Covered by Each Vehicle')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', va='bottom')  # va: vertical alignment

        display_figure(fig)

    # Function to display bar chart for total amount spent
    def display_total_amount_spent_chart():
        vehicle_numbers = vehicle_simulation_results.index.tolist()
        total_amounts_spent = vehicle_simulation_results['total_toll_amount'].tolist()

        fig, ax = plt.subplots(figsize=(7, 6))
        bars = ax.bar(vehicle_numbers, total_amounts_spent, color='skyblue')
        ax.set_xlabel('Vehicle Number')
        ax.set_ylabel('Total Amount Spent')
        ax.set_title('Total Amount Spent by Each Vehicle')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Adding data labels
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', va='bottom')  # va: vertical alignment

        display_figure(fig)

    # Function to display donut chart for feature distribution
    def display_donut_chart():
        vehicle_types = vehicle_data['vehicle_type'].value_counts().index.tolist()
        vehicle_counts = vehicle_data['vehicle_type'].value_counts().tolist()

        fig, ax = plt.subplots(figsize=(7, 6), facecolor='lightyellow')
        wedges, texts, autotexts = ax.pie(vehicle_counts, labels=vehicle_types, autopct='%1.1f%%', startangle=140,
                                          colors=['skyblue', 'orange', 'green', 'red', 'purple', 'brown', 'pink'],
                                          wedgeprops=dict(width=0.7))

        for autotext in autotexts:
            autotext.set_color('white')

        ax.set_title('Feature Distribution')
        display_figure(fig)

    # Function to display the figure in the Tkinter window
    def display_figure(fig):
        for widget in frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Create the main window
    root = tk.Tk()
    root.title("Vehicle Report")
    root.geometry("1024x768")  # Set window size to 1024x768 pixels

    # Create the main frame for buttons and charts
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    # Create buttons
    button_donut = ttk.Button(button_frame, text="Analysis on vehicle type", command=display_donut_chart)
    button_vehicle_distance = ttk.Button(button_frame, text="Distance Calculation", command=display_vehicle_distance_chart)
    button_total_amount_spent = ttk.Button(button_frame, text="Toll Expenses", command=display_total_amount_spent_chart)

    # Pack buttons
    button_donut.pack(side=tk.LEFT, padx=5, pady=5)
    button_vehicle_distance.pack(side=tk.LEFT, padx=5, pady=5)
    button_total_amount_spent.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a frame for the plot
    frame = ttk.Frame(main_frame)
    frame.pack(fill=tk.BOTH, expand=True)

    # Start the Tkinter event loop
    root.mainloop()

# Function call to display the vehicle report GUI
if __name__ == "__main__":
    display_vehicle_report()
