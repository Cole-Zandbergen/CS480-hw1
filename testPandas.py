import pandas as pd
import main

table = pd.read_csv("18and12.csv")

with open(main.outpath+"/test.csv", 'w') as file:
    file.write(table.to_csv())