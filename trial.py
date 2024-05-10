import pickle
import pandas as pd
from extractor import get_averages_combined
df = get_averages_combined("ATL","BOS")
with open('Artificats\model.pkl', 'rb') as file:  
    model = pickle.load(file)

# evaluate model 
predicted = model.predict(df)
print(predicted)