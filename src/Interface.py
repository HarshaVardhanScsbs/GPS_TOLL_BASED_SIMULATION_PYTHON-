import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Import Pillow for image handling
import matplotlib.pyplot as plt
import pandas as pd
import threading
import queue
from Simulation import run_simulation  # Import the run_simulation function
from plotly.offline import plot

# Create a queue for thread-safe communication
result_queue = queue.Queue()
log_queue = queue.Queue()
# Colors
PRIMARY_COLOR = "#1E90FF"  # DodgerBlue
SECONDARY_COLOR = "#FFFFFF"  # White
TEXT_COLOR = "#000000"  # Black

def login():
    user = username_entry.get()
    pw = password_entry.get()
    if user == "admin" and pw == "password":  # simple check, replace with actual logic
        show_main_window()
        login_window.destroy()
    else:
        messagebox.showerror("Error", "Incorrect Username or Password")

def show_main_window():
    root.configure(bg=PRIMARY_COLOR)
    root.deiconify()

def add_vehicle():
    vehicle_id = vehicle_id_entry.get()
    vehicle_type = vehicle_type_entry.get()
    start_index = start_index_entry.get()
    stop_index = stop_index_entry.get()
    route_index = route_index_entry.get()

    if not all([vehicle_id, vehicle_type, start_index, stop_index, route_index]):
        messagebox.showwarning("Input Error", "All fields must be filled out")
        return

    # Add data to the Excel file
    try:
        new_data = pd.DataFrame({
            'vehicle_id': [vehicle_id],
            'vehicle_type': [vehicle_type],
            'start_index': [int(start_index)],
            'stop_index': [int(stop_index)],
            'route_index': [int(route_index)]
        })
        with pd.ExcelWriter('/Users/apple/Desktop/PythonProjects/Final/vehicle_data.xlsx', engine='openpyxl',
                            mode='a', if_sheet_exists='overlay') as writer:
            new_data.to_excel(writer, sheet_name='Sheet1', index=False, header=False,
                              startrow=writer.sheets['Sheet1'].max_row)
        messagebox.showinfo("Success", "Vehicle data added successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_simulation_and_display():
    try:
        results, logs, fig = run_simulation(output_text) # Call the function from Simulation.py
        result_queue.put(results)  # Put results and logs in the queue
        log_queue.put(logs)
        root.after(100,check_simulation_thread)
    except Exception as e:
        print("Error in run_simulation:", e)
        result_queue.put(e)  # Put the exception in the queue for error handling


def run_simulation_thread():
    thread = threading.Thread(target=run_simulation_and_display)
    thread.start()
    root.after(100, check_simulation_thread)  # Schedule the first check

def check_simulation_thread():
    try:
        results, logs, fig = result_queue.get_nowait()  # Check if the simulation is done
        logs = log_queue.get_nowait()
        # If an exception occurred, re-raise it

        # Clear previous content
        for row in result_tree.get_children():
            result_tree.delete(row)
        log_text_display.config(state=tk.NORMAL)
        log_text_display.delete(1.0, tk.END)
        log_text_display.config(state=tk.DISABLED)

        # Insert new results into the Treeview
        for result, log in zip(results, logs):
            try:
                vehicle_id = result['vehicle_id']
                tolls_crossed = str(result['tolls_crossed'])
                total_toll_amount = f"{result['total_toll_amount']:.2f} units"
                total_distance_travelled = f"{result['total_distance_travelled']:.2f} km"
            except KeyError as e:
                messagebox.showerror("Error", f"Missing key in result: {e}")
                continue

            result_tree.insert('', tk.END, values=(
                vehicle_id,
                tolls_crossed,
                total_toll_amount,
                total_distance_travelled
            ))

            log_text_display.config(state=tk.NORMAL)
            log_text_display.insert(tk.END, f"Vehicle ID: {vehicle_id} Log:\n")
            for line in log:
                log_text_display.insert(tk.END, line + "\n")
            log_text_display.insert(tk.END, "\n")
            log_text_display.config(state=tk.DISABLED)

        messagebox.showinfo("Simulation Completed", "Simulation and logs have been updated.")
    except queue.Empty:
        root.after(100, check_simulation_thread)
        return # Re-schedule the check if not done yet
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_plotly_figure(fig):
    plotly_frame = tk.Frame(root)
    plotly_frame.pack(fill=tk.BOTH, expand=True)

    plotly_fig_html = plot(fig, output_type='div')

    plotly_label = tk.Label(plotly_frame, text="Plotly Figure", bg=PRIMARY_COLOR, fg=TEXT_COLOR)
    plotly_label.pack(pady=10)

    plotly_canvas = tk.Canvas(plotly_frame, width=1000, height=600)
    plotly_canvas.pack()

    plotly_html_label = tk.Label(plotly_canvas, text=plotly_fig_html, bg=PRIMARY_COLOR, fg=TEXT_COLOR, wraplength=1000)
    plotly_canvas.create_window((0, 0), window=plotly_html_label, anchor=tk.NW)

def display_vehicle_report():
    # Read data from Excel files
    vehicle_simulation_results = pd.read_excel('/Users/apple/Desktop/PythonProjects/Final/vehicle_data.xlsx', index_col='vehicle_id')
    vehicle_data = pd.read_excel('/Users/apple/Desktop/PythonProjects/Final/vehicle_data.xlsx', index_col='vehicle_id')

    # Function to display bar chart for distance calculation
    def display_vehicle_distance_chart():
        vehicle_numbers = vehicle_simulation_results.index.tolist()
        distances_covered = vehicle_simulation_results['total_distance_travelled'].tolist()

        fig, ax = plt.subplots(figsize=(7, 6))
        bars = ax.bar(vehicle_numbers, distances_covered, color='skyblue')
        ax.set_xlabel('Vehicle Number')
        ax.set_ylabel('Distance Covered')
        ax.set_title('Distance Covered by Each Vehicle')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Adding data labels
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

    # Create the main window for the report
    report_window = tk.Toplevel(root)
    report_window.title("Vehicle Report")
    report_window.geometry("1024x768")  # Set window size to 1024x768 pixels

    # Create the main frame for buttons and charts
    main_frame = ttk.Frame(report_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    # Create buttons
    button_donut = ttk.Button(button_frame, text="Analysis on Vehicle Type", command=display_donut_chart)
    button_vehicle_distance = ttk.Button(button_frame, text="Distance Calculation", command=display_vehicle_distance_chart)
    button_total_amount_spent = ttk.Button(button_frame, text="Toll Expenses", command=display_total_amount_spent_chart)

    # Pack buttons
    button_donut.pack(side=tk.LEFT, padx=5, pady=5)
    button_vehicle_distance.pack(side=tk.LEFT, padx=5, pady=5)
    button_total_amount_spent.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a frame for the plot
    frame = ttk.Frame(main_frame)
    frame.pack(fill=tk.BOTH, expand=True)



# Main application window
root = tk.Tk()
root.withdraw()  # Hide main window initially
root.title("GPS Toll Simulation")
root.geometry("1200x768")
root.configure(bg=PRIMARY_COLOR)  # Set background color




fullscreen = False  # Start in windowed mode

# Set the window to full screen
root.attributes("-fullscreen", fullscreen)

# Add a logo image to the login page
logo_image = Image.open('../symtoll.jpg')  # Replace with the path to your logo
logo_photo = ImageTk.PhotoImage(logo_image)

# Create the login window
login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("500x500")
login_window.configure(bg=PRIMARY_COLOR)

# Add logo to the login frame
logo_label = ttk.Label(login_window, image=logo_photo)
logo_label.pack(pady=10)


tk.Label(login_window, text="Username:", bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:", bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=5)
password_entry = tk.Entry(login_window, show='*')
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login, bg=SECONDARY_COLOR, fg=TEXT_COLOR)
login_button.pack(pady=20)

# Create the content frame for the main window
content_frame = ttk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True)

# Create a Text widget to display the output
output_text = tk.Text(content_frame, wrap=tk.WORD, height=15, width=45)
output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
# Create widgets for the main window
tk.Label(content_frame, text="Vehicle ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
vehicle_id_entry = tk.Entry(content_frame)
vehicle_id_entry.grid(row=0, column=0, padx=80, pady=5, sticky='w')

tk.Label(content_frame, text="Vehicle Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
vehicle_type_entry = tk.Entry(content_frame)
vehicle_type_entry.grid(row=1, column=0, padx=80, pady=5, sticky='w')

tk.Label(content_frame, text="Start Index:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
start_index_entry = tk.Entry(content_frame)
start_index_entry.grid(row=2, column=0, padx=80, pady=5, sticky='w')

tk.Label(content_frame, text="Stop Index:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
stop_index_entry = tk.Entry(content_frame)
stop_index_entry.grid(row=3, column=0, padx=80, pady=5, sticky='w')

tk.Label(content_frame, text="Route Index:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
route_index_entry = tk.Entry(content_frame)
route_index_entry.grid(row=4, column=0, padx=80, pady=5, sticky='w')

add_vehicle_button = tk.Button(content_frame, text="Add Vehicle", command=add_vehicle)
add_vehicle_button.grid(row=6, column=0, columnspan=1, pady=10, padx=80)

# Button to run simulation
run_simulation_button = tk.Button(content_frame, text="Run Simulation", command=run_simulation_thread)
run_simulation_button.grid(row=7, column=0, columnspan=1, pady=10, padx=80)

# Button to display the vehicle report
simulation_report_button = tk.Button(content_frame, text="Simulation Report", command=display_vehicle_report)
simulation_report_button.grid(row=6, column=1, columnspan=1, pady=10, padx=50)

# Button to display Plotly visualization
plotly_button = tk.Button(content_frame, text="Show Plotly Visualization", command=run_simulation_thread)
plotly_button.grid(row=7, column=1, columnspan=1, pady=10, padx=50)


# Create the Treeview widget to display simulation results
result_tree = ttk.Treeview(content_frame, columns=("Vehicle ID", "Tolls Crossed", "Total Toll Amount", "Total Distance"), show='headings')
result_tree.heading("Vehicle ID", text="Vehicle ID")
result_tree.heading("Tolls Crossed", text="Tolls Crossed")
result_tree.heading("Total Toll Amount", text="Total Toll Amount")
result_tree.heading("Total Distance", text="Total Distance")
result_tree.grid(row=8, column=0, columnspan=2, pady=5,padx=10, sticky='nsew')

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=result_tree.yview)
scrollbar.grid(row=8, column=0, sticky='nw')
result_tree.configure(yscrollcommand=scrollbar.set)

# Create a Text widget to display logs
tk.Label(content_frame, text="Logs:").grid(row=7, column=2, padx=10, pady=5, sticky='w')
log_text_display = tk.Text(content_frame, wrap=tk.WORD, height=15,width=45, state=tk.DISABLED)
log_text_display.grid(row=8, column=2, padx=10, pady=5, sticky='nsew')

# Configure row and column weights
content_frame.grid_rowconfigure(9, weight=1)
content_frame.grid_columnconfigure(1, weight=1)

# Start the Tkinter event loop

root.mainloop()
