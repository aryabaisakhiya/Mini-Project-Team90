import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

def recommend(dataframe, _input, ingredients=[], params={'n_neighbors': 5}):
    extracted_data = dataframe[~dataframe['RecipeIngredientParts'].str.contains('|'.join(ingredients), regex=True, flags=re.IGNORECASE)]
    if len(extracted_data) >= params['n_neighbors']:
        prep_data = StandardScaler().fit_transform(extracted_data.iloc[:, 6:15])
        pipeline = Pipeline([('NN', FunctionTransformer(NearestNeighbors(metric='cosine').fit(prep_data).kneighbors, kw_args=params))])
        return extracted_data.iloc[pipeline.transform(np.array(_input).reshape(1, -1))[0]]
    return None
