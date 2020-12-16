import csv
import pandas as pd

UFC = pd.read_csv("ufc scrapping data.csv", encoding = "mac_roman")     
UFC = UFC[UFC["Weight"].str.len() > 2]
UFC["weight number"] = UFC["Weight"].str[:3]
UFC["weight number"] = pd.to_numeric(UFC["weight number"])


# Convert percentage stats into float 
UFC['Str. Acc.'] = UFC['Str. Acc.'].str.rstrip('%').astype('float') / 100.0
UFC['Str. Def'] = UFC['Str. Def'].str.rstrip('%').astype('float') / 100.0
UFC['TD Acc.'] = UFC['TD Acc.'].str.rstrip('%').astype('float') / 100.0
UFC['TD Def.'] = UFC['TD Def.'].str.rstrip('%').astype('float') / 100.0



# Add Weight Class
WeightClass = []
for row in UFC["weight number"]:
    if row < 116: WeightClass.append("Strawweight")
    elif row < 126: WeightClass.append("Flyweight")
    elif row < 136: WeightClass.append("Bantamweight")
    elif row < 146: WeightClass.append("Featherweight")
    elif row < 156: WeightClass.append("Lightweight")
    elif row < 176: WeightClass.append("Welterweight")
    elif row < 186: WeightClass.append("Middleweight")
    elif row < 206: WeightClass.append("Lightheavyweight")
    elif row < 1000: WeightClass.append("Heavyweight")
    else: WeightClass.append("NAN")
        
UFC["WeightClass"] = WeightClass
UFC.to_csv("UFC Data.csv")




