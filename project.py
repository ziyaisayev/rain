import csv
import tkinter as tk 
from tkinter import filedialog,messagebox,scrolledtext
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
    rain_file = filedialog.askopenfilename(title="sellect rain_data.csv",filetypes=[("CSV Files","*.csv")])
    village_file = filedialog.askopenfilename(title="sellect village_data.csv",filetypes=[("CSV Files","*.csv")])
    if rain_file and village_file:
        try:
            total_rain = load_rain_data(rain_file)
            villages, total_population = load_village_data(village_file)
            distribution, reserved = distribute_rain(total_rain, villages, total_population)
            output_text.delete("1.0",tk.END)
            output_text.insert(tk.END,"water distribution to village")
            for village, litres in distribution.items():
                output_text.insert(tk.END, f"{village}: {litres} litres\n")
            output_text.insert(tk.END, f"\nReserved Water: {reserved} litres\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("warning","file is not choicen")
root = tk.Tk()
root.title("Rain Water Distribution")

root.geometry('600x500')
root.configure(bg='#E6F2FF')

title_label = tk.Label(root, text="Rain Water Distribution App", font=("Arial", 20, 'bold'), bg='#E6F2FF')
title_label.pack(pady=10)

button_frame=tk.Frame(root,bg="#3ba189")
button_frame.pack()

btn1=tk.Button(button_frame,text="datalari daxil edin",command=open_files,bg="#b8e0b8",font=("Arial",14))
btn1.pack()

output_text=scrolledtext.ScrolledText(root,width=70,height=20,font=("Arial",12))
output_text.pack()
root.mainloop()
