import streamlit as st
import pandas as pd
import plotly.express as px

class VisualizadorDatos:
    def __init__(self, archivo):
        self.data = pd.read_csv(archivo, delimiter=";")
        self.columnas_departamento = ['DEPARTAMENTO1']
        self.columnas_provincia = ['DEPARTAMENTO1', 'PROVINCIA1']
        self.columnas_distrito = ['DEPARTAMENTO1', 'PROVINCIA1', 'DISTRITO1']
        self.columnas_anp_cate = ['ANP_CATE']

    def filtrar_y_eliminar_nulos(self, data_frame):
        return data_frame.dropna()

    def convertir_a_str(self, data_frame):
        return data_frame.applymap(str)

    def concatenar_columnas(self, data_frame, columnas):
        data_frame['Location'] = data_frame.apply(lambda row: ', '.join(row), axis=1)
        return data_frame

    def contar_ocurrencias(self, data_frame):
        conteo = data_frame['Location'].value_counts().reset_index()
        conteo.columns = ['Ubicacion', 'Count']
        return conteo

    def generar_grafica(self, conteo, titulo):
        figura = px.bar(conteo, x='Ubicacion', y='Count', title=titulo)
        return figura

    def mostrar_grafica(self, figura):
        st.plotly_chart(figura)

def main():
    # Título de la aplicación Streamlit
    st.markdown("# GRAFICA DE DATOS ")

    # Crear una instancia de la clase VisualizadorDatos y cargar el archivo CSV
    visualizador = VisualizadorDatos("archivo.csv")

    # Filtrar y eliminar valores nulos para cada nivel geográfico (departamento, provincia, distrito)
    data_anp_cate = visualizador.filtrar_y_eliminar_nulos(visualizador.data[visualizador.columnas_anp_cate])
    data_departamento = visualizador.filtrar_y_eliminar_nulos(visualizador.data[visualizador.columnas_departamento])
    data_provincia = visualizador.filtrar_y_eliminar_nulos(visualizador.data[visualizador.columnas_provincia])
    data_distrito = visualizador.filtrar_y_eliminar_nulos(visualizador.data[visualizador.columnas_distrito])

    # Convertir las columnas a tipo str si no lo son
    data_anp_cate = visualizador.convertir_a_str(data_anp_cate)
    data_departamento = visualizador.convertir_a_str(data_departamento)
    data_provincia = visualizador.convertir_a_str(data_provincia)
    data_distrito = visualizador.convertir_a_str(data_distrito)

    # Concatenar las columnas para formar la columna 'Location' para cada nivel geográfico
    data_anp_cate = visualizador.concatenar_columnas(data_anp_cate, visualizador.columnas_anp_cate)
    data_departamento = visualizador.concatenar_columnas(data_departamento, visualizador.columnas_departamento)
    data_provincia = visualizador.concatenar_columnas(data_provincia, visualizador.columnas_provincia)
    data_distrito = visualizador.concatenar_columnas(data_distrito, visualizador.columnas_distrito)

    # Contar las ocurrencias de cada ubicación para cada nivel geográfico
    conteo_anp_cate = visualizador.contar_ocurrencias(data_anp_cate)
    conteo_departamento = visualizador.contar_ocurrencias(data_departamento)
    conteo_provincia = visualizador.contar_ocurrencias(data_provincia)
    conteo_distrito = visualizador.contar_ocurrencias(data_distrito)

    # Generar gráficas de barras para cada nivel geográfico
    fig_anp_cate = visualizador.generar_grafica(conteo_anp_cate, "Conteo por ANP CATE")
    fig_departamento = visualizador.generar_grafica(conteo_departamento, "Conteo por Departamento")
    fig_provincia = visualizador.generar_grafica(conteo_provincia, "Conteo por Provincia")
    fig_distrito = visualizador.generar_grafica(conteo_distrito, "Conteo por Distrito")

    # Mostrar las gráficas en la aplicación Streamlit
    visualizador.mostrar_grafica(fig_anp_cate)
    visualizador.mostrar_grafica(fig_departamento)
    visualizador.mostrar_grafica(fig_provincia)
    visualizador.mostrar_grafica(fig_distrito)

if __name__ == "__main__":
    main()
