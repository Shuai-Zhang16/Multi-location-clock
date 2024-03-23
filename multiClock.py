import tkinter as tk
from tkinter import ttk
from planet_time_calculation import PlanetTimeCalculator


def add_selected_planet_time():
    """Add the selected planet's time to the table when the "Add Planet" button is clicked.

    :return: None
    """

    # Get the planet selected by the user
    selected_planet = planet_combobox.get()

    if selected_planet:
        # Check if the selected planet is already displayed in the table
        existing_planets = [treeview.item(item)['values'][0] for item in treeview.get_children()]
        if selected_planet not in existing_planets:
            # Calculate and display the selected planet's time
            planet_time = planet_time_calculator.calculate_planet_time(selected_planet)
            treeview.insert('', 'end', values=(selected_planet, planet_time))
            # Update the planet combobox options to remove the planet that has been added
            update_planet_combobox_options()
            # Clear the selection in the planet combobox
            planet_combobox.set('')

    update_times()


def update_planet_combobox_options():
    """Update the planet combobox options to remove the planets that have already been added to the table.

    :return: None
    """

    # First get the planets that have already been added to the table
    existing_planets = [treeview.item(item)['values'][0] for item in treeview.get_children()]
    # Update the planet combobox options to remove the planets that have already been added
    available_planets = [planet for planet in planet_options if planet not in existing_planets]
    planet_combobox['values'] = available_planets


def update_times():
    """Update the planet time in the table every second.

    :return: None
    """
    for item in treeview.get_children():
        planet_name = treeview.item(item)['values'][0]
        # Recalculate time
        planet_time = planet_time_calculator.calculate_planet_time(planet_name)
        # Update the time in the table
        treeview.item(item, values=(planet_name, planet_time))
    # Set a timer to update times every certain interval
    root.after(1000, update_times)


if __name__ == "__main__":
    # Create an instance of PlanetTimeCalculator
    planet_time_calculator = PlanetTimeCalculator()

    # Set up the main window
    root = tk.Tk()
    root.title("Planet Time Calculator")

    # Set the window size and position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width / 1.5)
    window_height = int(screen_height / 2)
    position_x = int(screen_width / 4)
    position_y = int(screen_height / 4)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Configure the style for the Treeview widget
    style = ttk.Style(root)
    # Center-align the text in the Treeview
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'), foreground="blue")
    # Center-align the text in the Treeview columns
    style.configure("Treeview.Column", anchor="center")
    # Add a border to the Treeview
    style.configure("Treeview", borderwidth=2, relief="solid")

    # Create the Treeview widget to display the planet times in a table
    columns = ('Planet Name', 'Time')
    treeview = ttk.Treeview(root, columns=columns, show='headings')
    treeview.heading('Planet Name', text='Planet Name')
    treeview.heading('Time', text='Time in Year/Month/Day - Hour/Minutes/Seconds')
    treeview.column('Planet Name', anchor='center')
    treeview.column('Time', anchor='center')
    treeview.pack(expand=True, fill='both', padx=5, pady=5)

    # Create a frame to hold the control widgets for the buttons and combobox
    control_frame = tk.Frame(root)
    control_frame.pack(fill='x', padx=5, pady=5)

    # Create a label to explain the purpose of the combobox
    explanation_label = tk.Label(control_frame, text="Please Select the planet to you want to trace the time: ", font=('Arial', 14))
    explanation_label.grid(row=0, column=0, padx=(0, 10), sticky='w')

    # Remove Earth option and create a dropdown menu for the user to select a planet
    planet_options = list(planet_time_calculator.planet_day_lengths.keys())
    planet_options.remove('Earth')  # Remove Earth
    planet_combobox = ttk.Combobox(control_frame, values=planet_options, width=20)
    planet_combobox.grid(row=0, column=1, padx=(0, 10), pady=(5,0), sticky='ew')

    # Create a button that adds the selected planet's time when clicked
    add_button = tk.Button(control_frame, text="Add Planet", command=add_selected_planet_time)
    add_button.grid(row=0, column=2, padx=(10, 0))

    # Automatically display Earth's time at startup and begin updating in real-time
    display_earth_time_at_startup = lambda: treeview.insert('', 'end', values=('Earth', planet_time_calculator.calculate_planet_time('Earth')))
    display_earth_time_at_startup()
    update_times()  # Start updating times in real-time

    # Start the Tkinter event loop
    root.mainloop()
