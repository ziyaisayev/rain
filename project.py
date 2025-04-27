import csv

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

def main():
    rain_file = "rain_data.csv"
    village_file = "rain_data.csv" 
    total_rain = load_rain_data(rain_file)
    villages, total_population = load_village_data(village_file)
    distribution, reserved = distribute_rain(total_rain, villages, total_population)

    print("\n🌧️ Water Distribution Report 🌧️")
    print("-" * 40)
    for village, amount in distribution.items():
        print(f"{village:<20} ➔ {amount:>8.2f} L")
    print("-" * 40)
    print(f"\n💧 Reserved Rainwater: {reserved:.2f} L")

if __name__ == "__main__":
    main()
