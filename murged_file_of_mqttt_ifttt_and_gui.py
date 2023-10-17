import paho.mqtt.client as mqtt
import requests
import tkinter as tk

# MQTT Functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("https://mqtt.com/ankit")
    else:
        print(f"Connection to MQTT broker failed with code {rc}")

def on_message(client, userdata, msg):
    if msg.topic == "mqtt/fall":
        message = msg.payload.decode("utf-8")
        print("your bike got accident :", message)
        # Replace the URL with your IFTTT webhook URL
        requests.post("https://maker.ifttt.com/trigger//6d554g/ankit/dk6s4/fCJ-e_x2TTfn-BQnYlvHzZ4Xk_CGgnQRd4jWLACG4AS", data={"value1": message})

# MQTT Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

mqtt_server = "198.168.43.32"  # Replace with the Raspberry Pi's IP address
mqtt_port = 1883

client.connect(mqtt_server, mqtt_port, 60)
client.loop_start()

# Tkinter Functions
def update_acceleration_limit():
    limit = acceleration_slider.get()
    acceleration_label.config(text=f"Acceleration Limit: {limit} m/s²")

def toggle_acceleration():
    is_enabled = acceleration_switch.get()
    acceleration_slider.config(state="normal" if is_enabled else "disabled")
    acceleration_label.config(state="normal" if is_enabled else "disabled")

def toggle_gyroscope(axis):
    is_enabled = gyroscope_switches[axis].get()
    slider = gyroscope_sliders[axis]
    label = gyroscope_labels[axis]
    if is_enabled:
        slider.config(state="normal")
        label.config(state="normal")
    else:
        slider.config(state="disabled")
        label.config(state="disabled")

def update_gyroscope_limit(axis):
    limit = gyroscope_sliders[axis].get()
    gyroscope_labels[axis].config(text=f"Gyroscope Limit ({axis} axis): {limit} deg/s")

# Create the main window
root = tk.Tk()
root.title("Sensor Limits")

# Create a frame for acceleration
acceleration_frame = tk.Frame(root)
acceleration_frame.pack(padx=10, pady=10)

# Load the image for acceleration
acceleration_image = tk.PhotoImage(file="acceleration.png")  # Replace "acceleration.png" with the path to your image
acceleration_label = tk.Label(acceleration_frame, text="Acceleration Limit: 0 m/s²", image=acceleration_image, compound="left", font=("Helvetica", 16))
acceleration_label.pack(side="left")

acceleration_slider = tk.Scale(acceleration_frame, from_=0, to=20, orient="horizontal", length=400, resolution=0.1, command=update_acceleration_limit, sliderlength=30)
acceleration_slider.set(10)  # Initial value
acceleration_slider.pack()

# Acceleration Switch
acceleration_switch = tk.IntVar()
acceleration_switch.set(1)  # Default to enabled
toggle_acceleration_button = tk.Checkbutton(acceleration_frame, text="Enable Acceleration", variable=acceleration_switch, command=toggle_acceleration, font=("Helvetica", 14))
toggle_acceleration_button.pack()

# Gyroscope Limits
gyroscope_axes = ["X", "Y", "Z"]
gyroscope_sliders = {}
gyroscope_labels = {}
gyroscope_switches = {}

for axis in gyroscope_axes:
    # Create a frame for each gyroscope axis with space between them
    axis_frame = tk.Frame(root)
    axis_frame.pack(padx=10, pady=10)

    # Load the image for the gyroscope axis
    gyroscope_image = tk.PhotoImage(file=f"{axis.lower()}_axis.png")  # Replace with appropriate image paths
    axis_label = tk.Label(axis_frame, text=f"Gyroscope Limit ({axis} axis): 0 deg/s", image=gyroscope_image, compound="left", font=("Helvetica", 16))
    axis_label.pack(side="left")

    slider = tk.Scale(axis_frame, from_=0, to=360, orient="horizontal", length=400, resolution=0.1, command=lambda a=axis: update_gyroscope_limit(a), sliderlength=30)
    slider.set(180)  # Initial value
    slider.pack()

    switch = tk.IntVar()
    switch.set(1)  # Default to enabled
    toggle_button = tk.Checkbutton(axis_frame, text=f"Enable {axis} axis", variable=switch, command=lambda a=axis: toggle_gyroscope(a), font=("Helvetica", 14))
    toggle_button.pack()

    gyroscope_sliders[axis] = slider
    gyroscope_labels[axis] = axis_label
    gyroscope_switches[axis] = switch

# Start the GUI application
root.mainloop()