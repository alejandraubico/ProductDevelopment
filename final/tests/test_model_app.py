import streamlit as st
import pandas as pd 
from pycaret.regression import load_model
from pycaret.regression import predict_model
import mlflow
import requests
from PIL import Image

im = Image.open('../car.png')
st.set_page_config(page_title="Car Price Prediction", page_icon = im)
st.title("Predicción del precio de carros")

data_path = '../data/raw/car_price_prediction.csv'
dataset = pd.read_csv(data_path)

def obtener_resultados(url):
    response = requests.get(url)
    data = response.json()
    return data

url_modelo_1 = "http://127.0.0.1:5000/predictA"
url_modelo_2 = "http://127.0.0.1:5000/predictB"
url_modelo_3 = "http://127.0.0.1:5000/predictC"
url_todos = "http://127.0.0.1:5000/predictAll"

tabs = ["Modelo 1", "Modelo 2", "Modelo 3", "Todos los modelos"]
selected_tab = st.sidebar.radio("Selecciona el modelo:", tabs)
content_container = st.container()

with content_container:
    # Contenido de cada pestaña
    if selected_tab == "Modelo 1":
        st.markdown("### Modelo 1 - LGBM")
        
        left, right = st.columns(2)   
        with left:     
            Levy = st.selectbox('Impuesto', options=list(dataset['Levy'].unique()))
            Manufacturer = st.selectbox('Fabricante', options=list(dataset['Manufacturer'].unique()))
            Model = st.selectbox('Línea', options=list(dataset['Model'].unique()))
            Prod_year = st.slider("Año", 
                    min_value=dataset['Prod_year'].min(),
                    max_value=dataset['Prod_year'].max())
            Category = st.selectbox('Categoría', options=list(dataset['Category'].unique()))
            Leather_interior = st.selectbox('Cuero (interior)', options=list(dataset['Leather_interior'].unique()))
            Fuel_type = st.selectbox('Tipo de combustible', options=list(dataset['Fuel_type'].unique()))
            Engine_volume = st.selectbox('Motor', options=list(dataset['Category'].unique()))
        with right:     
            Mileage = st.selectbox('Millaje', options=list(dataset['Mileage'].unique()))
            Cylinders = st.slider("Cilindraje", 
                    min_value=dataset['Cylinders'].min(),
                    max_value=dataset['Cylinders'].max())
            Gear_box_type = st.selectbox('Caja', options=list(dataset['Gear_box_type'].unique()))
            Drive_wheels = st.selectbox('Tracción', options=list(dataset['Drive_wheels'].unique()))
            Doors = st.selectbox('Puertas', options=list(dataset['Doors'].unique()))
            Wheel = st.selectbox('Volante', options=list(dataset['Wheel'].unique()))
            Color = st.selectbox('Color', options=list(dataset['Color'].unique()))
            Airbags = st.slider("Bolsas de aire", 
                    min_value=dataset['Airbags'].min(),
                    max_value=dataset['Airbags'].max())

        get_pred = st.button('Predecir el precio')
        if(get_pred):
            response = requests.post(url_modelo_1, 
                                    json={'Levy':Levy, 
                                            'Manufacturer':Manufacturer,
                                            'Model':Model, 
                                            'Prod_year': Prod_year,
                                            'Category':Category, 
                                            'Leather_interior':Leather_interior,
                                            'Fuel_type':Fuel_type,
                                            'Engine_volume':Engine_volume,
                                            'Mileage':Mileage,
                                            'Cylinders':Cylinders,
                                            'Gear_box_type':Gear_box_type,
                                            'Drive_wheels':Drive_wheels,
                                            'Doors':Doors,
                                            'Wheel':Wheel,
                                            'Color':Color,
                                            'Airbags':Airbags,
                                            })
            

            if response.status_code == 200:
                data = response.json()
                if 'Prediccion' in data:
                    st.success(f"Predicción exitosa. Precio $: {data['Prediccion']}")
                else:
                    st.error("Error en la predicción. Mensaje: {}".format(data.get('mensaje', 'No hay mensaje de error.')))
                    if 'error' in data:
                        st.error(f"Detalles del error: {data['error']}")
            else:
                st.error(f"Error en la solicitud al servidor. Código de estado: {response.status_code}")

    if selected_tab == "Modelo 2":
        st.markdown("### Modelo 2 - ET")

        left, right = st.columns(2)   
        with left:     
            Levy = st.selectbox('Impuesto', options=list(dataset['Levy'].unique()))
            Manufacturer = st.selectbox('Fabricante', options=list(dataset['Manufacturer'].unique()))
            Model = st.selectbox('Línea', options=list(dataset['Model'].unique()))
            Prod_year = st.slider("Año", 
                    min_value=dataset['Prod_year'].min(),
                    max_value=dataset['Prod_year'].max())
            Category = st.selectbox('Categoría', options=list(dataset['Category'].unique()))
            Leather_interior = st.selectbox('Cuero (interior)', options=list(dataset['Leather_interior'].unique()))
            Fuel_type = st.selectbox('Tipo de combustible', options=list(dataset['Fuel_type'].unique()))
            Engine_volume = st.selectbox('Motor', options=list(dataset['Category'].unique()))
        with right:     
            Mileage = st.selectbox('Millaje', options=list(dataset['Mileage'].unique()))
            Cylinders = st.slider("Cilindraje", 
                    min_value=dataset['Cylinders'].min(),
                    max_value=dataset['Cylinders'].max())
            Gear_box_type = st.selectbox('Caja', options=list(dataset['Gear_box_type'].unique()))
            Drive_wheels = st.selectbox('Tracción', options=list(dataset['Drive_wheels'].unique()))
            Doors = st.selectbox('Puertas', options=list(dataset['Doors'].unique()))
            Wheel = st.selectbox('Volante', options=list(dataset['Wheel'].unique()))
            Color = st.selectbox('Color', options=list(dataset['Color'].unique()))
            Airbags = st.slider("Bolsas de aire", 
                    min_value=dataset['Airbags'].min(),
                    max_value=dataset['Airbags'].max())

        get_pred = st.button('Predecir el precio')
        if(get_pred):
            response = requests.post(url_modelo_2, 
                                    json={'Levy':Levy, 
                                            'Manufacturer':Manufacturer,
                                            'Model':Model, 
                                            'Prod_year': Prod_year,
                                            'Category':Category, 
                                            'Leather_interior':Leather_interior,
                                            'Fuel_type':Fuel_type,
                                            'Engine_volume':Engine_volume,
                                            'Mileage':Mileage,
                                            'Cylinders':Cylinders,
                                            'Gear_box_type':Gear_box_type,
                                            'Drive_wheels':Drive_wheels,
                                            'Doors':Doors,
                                            'Wheel':Wheel,
                                            'Color':Color,
                                            'Airbags':Airbags,
                                            })
            

            if response.status_code == 200:
                data = response.json()
                if 'Prediccion' in data:
                    st.success(f"Predicción exitosa. Precio $: {data['Prediccion']}")
                else:
                    st.error("Error en la predicción. Mensaje: {}".format(data.get('mensaje', 'No hay mensaje de error.')))
                    if 'error' in data:
                        st.error(f"Detalles del error: {data['error']}")
            else:
                st.error(f"Error en la solicitud al servidor. Código de estado: {response.status_code}")


    if selected_tab == "Modelo 3":
        st.markdown("### Modelo 3 - KNN")
    
        left, right = st.columns(2)   
        with left:     
            Levy = st.selectbox('Impuesto', options=list(dataset['Levy'].unique()))
            Manufacturer = st.selectbox('Fabricante', options=list(dataset['Manufacturer'].unique()))
            Model = st.selectbox('Línea', options=list(dataset['Model'].unique()))
            Prod_year = st.slider("Año", 
                    min_value=dataset['Prod_year'].min(),
                    max_value=dataset['Prod_year'].max())
            Category = st.selectbox('Categoría', options=list(dataset['Category'].unique()))
            Leather_interior = st.selectbox('Cuero (interior)', options=list(dataset['Leather_interior'].unique()))
            Fuel_type = st.selectbox('Tipo de combustible', options=list(dataset['Fuel_type'].unique()))
            Engine_volume = st.selectbox('Motor', options=list(dataset['Category'].unique()))
        with right:     
            Mileage = st.selectbox('Millaje', options=list(dataset['Mileage'].unique()))
            Cylinders = st.slider("Cilindraje", 
                    min_value=dataset['Cylinders'].min(),
                    max_value=dataset['Cylinders'].max())
            Gear_box_type = st.selectbox('Caja', options=list(dataset['Gear_box_type'].unique()))
            Drive_wheels = st.selectbox('Tracción', options=list(dataset['Drive_wheels'].unique()))
            Doors = st.selectbox('Puertas', options=list(dataset['Doors'].unique()))
            Wheel = st.selectbox('Volante', options=list(dataset['Wheel'].unique()))
            Color = st.selectbox('Color', options=list(dataset['Color'].unique()))
            Airbags = st.slider("Bolsas de aire", 
                    min_value=dataset['Airbags'].min(),
                    max_value=dataset['Airbags'].max())

        get_pred = st.button('Predecir el precio')
        if(get_pred):
            response = requests.post(url_modelo_3, 
                                    json={'Levy':Levy, 
                                            'Manufacturer':Manufacturer,
                                            'Model':Model, 
                                            'Prod_year': Prod_year,
                                            'Category':Category, 
                                            'Leather_interior':Leather_interior,
                                            'Fuel_type':Fuel_type,
                                            'Engine_volume':Engine_volume,
                                            'Mileage':Mileage,
                                            'Cylinders':Cylinders,
                                            'Gear_box_type':Gear_box_type,
                                            'Drive_wheels':Drive_wheels,
                                            'Doors':Doors,
                                            'Wheel':Wheel,
                                            'Color':Color,
                                            'Airbags':Airbags,
                                            })
            

            if response.status_code == 200:
                data = response.json()
                if 'Prediccion' in data:
                    st.success(f"Predicción exitosa. Precio $: {data['Prediccion']}")
                else:
                    st.error("Error en la predicción. Mensaje: {}".format(data.get('mensaje', 'No hay mensaje de error.')))
                    if 'error' in data:
                        st.error(f"Detalles del error: {data['error']}")
            else:
                st.error(f"Error en la solicitud al servidor. Código de estado: {response.status_code}")

    if selected_tab == "Todos los modelos":
        st.markdown("### LGBM, ET y KNN")
    
        left, right = st.columns(2)   
        with left:     
            Levy = st.selectbox('Impuesto', options=list(dataset['Levy'].unique()))
            Manufacturer = st.selectbox('Fabricante', options=list(dataset['Manufacturer'].unique()))
            Model = st.selectbox('Línea', options=list(dataset['Model'].unique()))
            Prod_year = st.slider("Año", 
                    min_value=dataset['Prod_year'].min(),
                    max_value=dataset['Prod_year'].max())
            Category = st.selectbox('Categoría', options=list(dataset['Category'].unique()))
            Leather_interior = st.selectbox('Cuero (interior)', options=list(dataset['Leather_interior'].unique()))
            Fuel_type = st.selectbox('Tipo de combustible', options=list(dataset['Fuel_type'].unique()))
            Engine_volume = st.selectbox('Motor', options=list(dataset['Category'].unique()))
        with right:     
            Mileage = st.selectbox('Millaje', options=list(dataset['Mileage'].unique()))
            Cylinders = st.slider("Cilindraje", 
                    min_value=dataset['Cylinders'].min(),
                    max_value=dataset['Cylinders'].max())
            Gear_box_type = st.selectbox('Caja', options=list(dataset['Gear_box_type'].unique()))
            Drive_wheels = st.selectbox('Tracción', options=list(dataset['Drive_wheels'].unique()))
            Doors = st.selectbox('Puertas', options=list(dataset['Doors'].unique()))
            Wheel = st.selectbox('Volante', options=list(dataset['Wheel'].unique()))
            Color = st.selectbox('Color', options=list(dataset['Color'].unique()))
            Airbags = st.slider("Bolsas de aire", 
                    min_value=dataset['Airbags'].min(),
                    max_value=dataset['Airbags'].max())

        get_pred = st.button('Predecir el precio')
        if(get_pred):
            response = requests.post(url_todos, 
                                    json={'Levy':Levy, 
                                            'Manufacturer':Manufacturer,
                                            'Model':Model, 
                                            'Prod_year': Prod_year,
                                            'Category':Category, 
                                            'Leather_interior':Leather_interior,
                                            'Fuel_type':Fuel_type,
                                            'Engine_volume':Engine_volume,
                                            'Mileage':Mileage,
                                            'Cylinders':Cylinders,
                                            'Gear_box_type':Gear_box_type,
                                            'Drive_wheels':Drive_wheels,
                                            'Doors':Doors,
                                            'Wheel':Wheel,
                                            'Color':Color,
                                            'Airbags':Airbags,
                                            })
            

            if response.status_code == 200:
                data = response.json()
                
                if 'Prediccion lightgbm' in data:
                    data = {'Modelo': ['LGBM','ET',"KNN"],
                          'Prediccion ($)': [data['Prediccion lightgbm'],data['Prediccion ET'],data['Prediccion KNN']]
                    }
                    df = pd.DataFrame(data)
                    st.dataframe(df,hide_index=True)
                    # st.success(f"Predicción LGBM. Precio $: {data['Prediccion lightgbm']}")
                    # st.success(f"Predicción ET. Precio $: {data['Prediccion ET']}")
                    # st.success(f"Predicción KNN. Precio $: {data['Prediccion KNN']}")
                else:
                    st.error("Error en la predicción. Mensaje: {}".format(data.get('mensaje', 'No hay mensaje de error.')))
                    if 'error' in data:
                        st.error(f"Detalles del error: {data['error']}")
            else:
                st.error(f"Error en la solicitud al servidor. Código de estado: {response.status_code}")

