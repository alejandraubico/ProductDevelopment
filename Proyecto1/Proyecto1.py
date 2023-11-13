import streamlit as st
import pandas as pd
import re
import utils 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
import numpy as np
from streamlit_option_menu import option_menu

#para poder compartir los datos entre funciones/tabs
session_state = st.session_state
st.set_option('deprecation.showPyplotGlobalUse', False)

def carga_archivo(file):
    data = pd.read_csv(file) if file is not None else None
    session_state['data'] = data
    return data

def vista_previa_archivo():
    if st.session_state['data'] is not None:
        st.write("## Vista previa del archivo cargado:")
        st.write(st.session_state['data'].head())

def listado_columnas_por_tipo(data):
    if session_state['data'] is not None:
        st.write("### Variables por categoría")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("#### Discretas")
            st.write("\n".join(session_state.data.select_dtypes(include='int64').columns.tolist()))

        with col2:
            st.write("#### Continuas")
            st.write("\n".join(session_state.data.select_dtypes(include='float64').columns.tolist()))

        with col3:
            st.write("#### Fechas")
            st.write("\n".join(session_state.data.select_dtypes(include='datetime64').columns.tolist()))

        with col4:
            st.write("#### Categóricas")
            st.write("\n".join(session_state.data.select_dtypes(include='object').columns.tolist()))

#pestaña inicial
def tab1():
    st.title("Bienvenidos")
    st.write("En esta pestaña puede cargar su archivo .csv o .xls")
    
    #Carga del archivo csv o xls
    archivo = st.file_uploader("Seleccione el archivo que desea cargar (.csv o .xlsx)", type=["csv", "xlsx"])
    carga_archivo(archivo)
    st.write("El archivo no debe contener valores nulos.")

    #mostrar la data cargada
    vista_previa_archivo()

#pestaña de analisis y configuracion
def tab2():
    st.title("Análisis y Configuración")

    #listado de variables por tipo
    if session_state['data'] is not None:
        listado_columnas_por_tipo(session_state['data'])

    #graficas univariables
    st.write("### Gráficas Individuales (una variable)")
    continuas ,discretas, categoricas, fechas = utils.getColumnTypes(st.session_state['data'])
    dataset = st.session_state['data']

    tipo_variable = st.radio("Seleccionar tipo de variable:", ("continuas", "discretas","categóricas"))

    if tipo_variable == "continuas":
        features = continuas
    elif tipo_variable == "categóricas":
        features = categoricas
    elif tipo_variable == "discretas":
        features = discretas
    else:
        st.error("Tipo de variable no válido")

    # Selector de columna
    variable = st.selectbox("Seleccionar columna:", features)

    #hacemos grafico de densidad 
    
    boton_promedio = st.button("analizar")
    
    #funcion para graficas 
    def plotDistBoxQQ(dataset, col):
    # Configurar el estilo de seaborn
         sns.set(style="whitegrid")

    # Crear una figura con tres subgráficos
         fig1, axes = plt.subplots(1, 3, figsize=(10, 4))

    # Histograma y densidad
         sns.histplot(dataset[col], bins=30, ax=axes[0])
         axes[0].set_title("Histograma y Densidad")

    # Boxplot
         sns.boxplot(y=dataset[col], ax=axes[1])
         axes[1].set_title("Boxplot")

    # Q-Q plot
         stats.probplot(dataset[col], dist="norm", plot=axes[2])
         axes[2].set_title("Q-Q Plot")

    # Ajustar diseño
         plt.tight_layout()

    # Mostrar el gráfico en Streamlit
         st.pyplot(fig1)
    
    #programamos el primer boton
    if boton_promedio:
       
       if tipo_variable == "continuas":
        #minimo  y máximo de variable
        mini = dataset[variable].min()
        max = dataset[variable].max()
        kde = stats.gaussian_kde(dataset[variable])
       
        r_min = mini
        r_max = max

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.kdeplot(dataset[variable], color="blue", shade=False)

        kde_value_min = kde.evaluate(r_min)
        ax.vlines(x = r_min, ymin=0, ymax=kde_value_min, color="blue")

        kde_value_max = kde.evaluate(r_max)
        ax.vlines(x = r_max, ymin=0, ymax=kde_value_max)

        x = np.linspace(r_min, r_max, 10000)  # 1000 puntos entre r_min y r_max
        y = kde.evaluate(x)
        ax.fill_between(x, y, color="orange", alpha=0.5)  # alpha es para la transparencia
        plt.title(f"Densidad de {variable}")
        st.pyplot(fig)


       # Obtener un resumen descriptivo para la columna seleccionada
        summary_columna = dataset[variable].describe()

       # Mostrar el resumen descriptivo en Streamlit
        st.write(f"Resumen Descriptivo para la columna '{variable}':")
        st.write(summary_columna)

        st.write(f"analisis grafico para la variable '{variable}':")
       #monstramos una analisis visual
        plotDistBoxQQ(dataset, variable)
       elif tipo_variable == "discretas":
            #minimo  y máximo de variable
        mini = dataset[variable].min()
        max = dataset[variable].max()
        kde = stats.gaussian_kde(dataset[variable])
       
        r_min = mini
        r_max = max

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.kdeplot(dataset[variable], color="blue", shade=False)

        kde_value_min = kde.evaluate(r_min)
        ax.vlines(x = r_min, ymin=0, ymax=kde_value_min, color="blue")

        kde_value_max = kde.evaluate(r_max)
        ax.vlines(x = r_max, ymin=0, ymax=kde_value_max)

        x = np.linspace(r_min, r_max, 10000)  # 1000 puntos entre r_min y r_max
        y = kde.evaluate(x)
        ax.fill_between(x, y, color="orange", alpha=0.5)  # alpha es para la transparencia
        plt.title(f"Densidad de {variable}")
        st.pyplot(fig)


       # Obtener un resumen descriptivo para la columna seleccionada
        summary_columna = dataset[variable].describe()

       # Mostrar el resumen descriptivo en Streamlit
        st.write(f"Resumen Descriptivo para la columna '{variable}':")
        st.write(summary_columna)

        st.write(f"analisis grafico para la variable '{variable}':")
       #monstramos una analisis de outliers
        plotDistBoxQQ(dataset, variable)
     
       elif tipo_variable == "categóricas":
          # Gráfico de barras para variables categóricas
        counts = dataset[variable].value_counts()
        st.bar_chart(counts)
        st.write(f"Conteo de valores por categoría para la variable '{variable}':")
        st.write(counts)

    #graficas bivariables
    ## segmento de vars continuas vrs discretas 
    st.header("Análisis de dos variables")
    st.subheader("Continuas/discretas vs  continuas/discretas")
    tipo_variable1 = st.radio("Seleccionar tipo de variable 1:", ("continuas", "discretas"),key="var1")
    tipo_variable2 = st.radio("Seleccionar tipo de variable 2:", ("continuas", "discretas"),key="var2")
    
    if tipo_variable1 == "continuas":
        features1 = continuas
    elif tipo_variable1 == "categóricas":
        features1 = categoricas
    elif tipo_variable1 == "discretas":
        features1 = discretas
    
    
    if tipo_variable2 == "categóricas":
        features2 = categoricas
    elif tipo_variable2 == "discretas":
        features2 = discretas
    elif tipo_variable2 == "continuas":
        features2 = continuas
    
    variable1 = st.selectbox("Seleccionar var1:", features1, key="v1")
    variable2 = st.selectbox("Seleccionar var2:", features2,key="v2")
    
    boton_promedio2 = st.button("analizar",key="b2")

    if boton_promedio2:
       if tipo_variable1 == "continuas" or tipo_variable1 =="discretas"  and tipo_variable2 =="continuas" or tipo_variable2 =="discretas" :
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=dataset[variable1], y=dataset[variable2])
            plt.title(f"Scatter Plot entre '{variable1}' y '{variable2}'")
            st.pyplot()

            correlacion_dos_variables = dataset[variable1].corr(dataset[variable2])
            st.write(f"Métrica de Correlación (Pearson) entre '{variable1}' y '{variable2}': {correlacion_dos_variables}")


#segmento de 2 variables  cat vrs cont
    st.subheader("categórica vs  continua")
    features3 = categoricas
    features4 = continuas
    
    variable3 = st.selectbox("Seleccionar var1 categórica:", features3,key="v3")
    variable4 = st.selectbox("Seleccionar var2 continua:", features4, key="v4")
    
    boton_promedio3 = st.button("analizar",key="b3")

    if boton_promedio3:
        if variable3 in categoricas and variable4 in continuas :
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=dataset[variable3], y=dataset[variable4])
            plt.title(f"box Plot entre '{variable3}' y '{variable4}'")
            st.pyplot()
    

## segmentos categórica vrs categórica
    st.subheader("Categórica vs categórica")

    features5 = categoricas
    features6 = categoricas
    
    variable5 = st.selectbox("Seleccionar var1 categórica:", features5, key="variable_cat1")
    variable6 = st.selectbox("Seleccionar var2 categórica:", features6, key="variable_cat2")
    
    boton_promedio4 = st.button("analizar",key="b4")

    if boton_promedio4:
        if variable5 in categoricas and variable6 in categoricas :
           # Crear el mosaico plot
            plt.figure(figsize=(8, 6))
            mosaic_data = dataset[[variable5, variable6]]
            sns.heatmap(pd.crosstab(mosaic_data[variable5], mosaic_data[variable6], normalize='index'), cmap='Blues', annot=True, fmt=".2f")
            plt.title(f'Mosaic Plot entre {variable5} y {variable6}')
            st.pyplot()

    # Calcular el coeficiente de contingencia de Cramer
            contingency_table = pd.crosstab(dataset[variable5], dataset[variable6])
            chi2, _, _, _ = chi2_contingency(contingency_table)
            n =  min(contingency_table.shape[0], contingency_table.shape[1])
            cramer_v = np.sqrt(chi2 / (dataset.shape[0] * (n - 1)))
    
            st.write(f"Coeficiente de Contingencia de Cramer: {cramer_v:.4f}")



    # parte de var temp vrs numerica
    ## segmentos categórica vrs categórica
    st.subheader("Serie temporal")

    features7 = continuas + discretas
    features8 = fechas
    
    variable7 = st.selectbox("Seleccionar var1 numerica:", features7, key="var7")
    variable8 = st.selectbox("Seleccionar var2 temporal:", features8, key="var8")
    
    boton_promedio5 = st.button("analizar",key="b5")

    if boton_promedio5:
        if (variable7 in continuas + discretas) and (variable8 in fechas):
        
            plt.figure(figsize=(10, 6))
            plt.plot(dataset[variable8], dataset[variable7])
            plt.title(f'Serie Temporal de {variable7} a lo largo de {variable8}')
            plt.xlabel(variable8)
            plt.ylabel(variable7)
            st.pyplot()

def main(): 
    session_state = {'data': None}

    st.sidebar.title("Menú")
    tabs = ["Carga de Datos", "Análisis y Configuración"]
    selected_tab = st.sidebar.radio("", tabs)

    if selected_tab == "Carga de Datos":
        tab1()
    elif selected_tab == "Análisis y Configuración":
        tab2()


if(__name__ == '__main__'):
    main() 