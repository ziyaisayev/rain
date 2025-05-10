import csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def load_rain_data(filename):
    total_rain = 0.0
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_rain += float(row["RainCollected"])
    return total_rain

def load_village_data(filename):
    villages = []
    total_population = 0
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            village = {
                "name": row["village"],
                "population": int(row["population"])
            }
            villages.append(village)
            total_population += village["population"]
    return villages, total_population

def distribute_rain(total_rain, villages, total_population):
    water_needed = total_population * 60
    distribution = {}

    if total_rain > water_needed:
        for village in villages:
            distribution[village["name"]] = village["population"] * 60
        reserved = total_rain - water_needed
    else:
        reserved = total_rain * 0.10
        available_rain = total_rain - reserved
        for village in villages:
            proportion = village["population"] / total_population
            distribution[village["name"]] = round(proportion * available_rain, 2)

    return distribution, reserved

def open_files():
    rain_file = filedialog.askopenfilename(title="Select rain_data.csv", filetypes=[("CSV Files", "*.csv")])
    village_file = filedialog.askopenfilename(title="Select village_data.csv", filetypes=[("CSV Files", "*.csv")])
    
    if rain_file and village_file:
        try:
            total_rain = load_rain_data(rain_file)
            villages, total_population = load_village_data(village_file)
            distribution, reserved = distribute_rain(total_rain, villages, total_population)
            
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Water distribution to villages:\n\n")
            
            for village, litres in distribution.items():
                output_text.insert(tk.END, f"{village}: {litres} litres\n")
            output_text.insert(tk.END, f"\nReserved Water: {reserved} litres\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Warning", "No file selected.")

root = tk.Tk()
root.title("Rain Water Distribution")
root.geometry('800x700')
root.resizable(False, False)

root.configure(bg='#F4F8FF')

title_label = tk.Label(root, text="Rain Water Distribution App", font=("Helvetica", 24, 'bold'), bg='#F4F8FF', fg='#3E6A55')
title_label.pack(pady=20)

button_frame = tk.Frame(root, bg="#E1F5D6")
button_frame.pack(pady=20)

btn1 = tk.Button(button_frame, text="Load Data Files", command=open_files, bg="#A4C6B6", font=("Arial", 14, 'bold'), relief="raised", padx=20, pady=10)
btn1.pack()

output_text = scrolledtext.ScrolledText(root, width=90, height=20, font=("Arial", 12), wrap=tk.WORD, bg="#F9F9F9", fg="#333333", relief="solid")
output_text.pack(pady=20)

footer_label = tk.Label(root, text="© 2025 Rain Distribution App | All rights reserved", font=("Arial", 10), bg='#F4F8FF', fg='#3E6A55')
footer_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
