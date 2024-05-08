from averages import get_averages_combined
import pickle
import pandas as pd
df = get_averages_combined('IND','MIN')

with open('model.pkl', 'rb') as file:  
    model = pickle.load(file)
# evaluate model 
predicted = model.predict(df)
print(predicted)