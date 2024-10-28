import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
nutrition_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
if 'generated' not in st.session_state: st.session_state = {'generated': False, 'recommendations': None}

class Recommendation:
    def __init__(self, nutrition_list, nb_recommendations, ingredient_txt):
        self.nutrition_list = nutrition_list; self.nb_recommendations = nb_recommendations; self.ingredient_txt = ingredient_txt
    def generate(self):
        ingredients = self.ingredient_txt.split(';')
        recommendations = Generator(self.nutrition_list, ingredients, {'n_neighbors': self.nb_recommendations}).generate().json()['output']
        for recipe in recommendations: recipe['image_link'] = find_image(recipe['Name'])
        return recommendations

if st.form_submit_button("Generate"):
    recommendation = Recommendation([st.slider(val, 0, 2000) for val in nutrition_values], st.slider('Number of recommendations', 5, 20, step=5), st.text_input('Ingredients:'))
    st.session_state.recommendations = recommendation.generate()

if st.session_state.generated:
    for recipe in st.session_state.recommendations:
        st.expander(recipe['Name']).markdown(f"<img src={recipe['image_link']}><h5>Nutritional Values:</h5>{pd.DataFrame({val: recipe[val] for val in nutrition_values}).to_html(escape=False)}")
