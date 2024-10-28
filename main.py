from fastapi import FastAPI
from pydantic import BaseModel, conlist
app = FastAPI()
dataset = pd.read_csv('../Data/dataset.csv', compression='gzip')

class PredictionIn(BaseModel):
    nutrition_input: conlist(float, min_items=9, max_items=9); ingredients: list[str] = []; params: Optional[dict] = {}

class Recipe(BaseModel):
@app.post("/predict/")
def predict(input: PredictionIn): return {"output": output_recommended_recipes(recommend(dataset, input.nutrition_input, input.ingredients, input.params))}

