import streamlit as st
from groq import Groq 

st.set_page_config("MI CHAT BOT")
st.title("BIENVENIDO AL CHATBOT DE LU, EL MEJOR CHATBOT DEL MUNDO")

MODELOS = ["llama3-8b-8192", "llama3-70b-8192"]

def configurar_pagina():
    st. title("My little chat")

    nombre = st.text_input("¿Como te llamas?")
    if st.button("saludar"):
        st.write(f"Hola {nombre}, un gusto en conocerte")

    st.sidebar.title("Configuración modelos")

    Modelo_elegido = st.sidebar.selectbox(
        "Modelos",
        MODELOS,
        index=0)
    
    return Modelo_elegido
    
def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_entrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user" , "content" : mensaje_entrada}],
        stream = True
)
def inicializador_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []  

def actualizar_historial(rol, contenido, avatar): 
    st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedor = st.container(height=400, border=True)
    with contenedor: mostrar_historial()

def generar_respuesta(respuesta_ia):
    respuesta_completa = "" 
    for frase in respuesta_ia:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():

    usuario_groq = crear_usuario()
    inicializador_estado()
    modelo_actual = configurar_pagina()
    area_chat()
    mensaje = st.chat_input("¿Que queres saber?")


    if mensaje: 
        actualizar_historial("user", mensaje,"🐲")
        respuesta_ia = configurar_modelo(usuario_groq, modelo_actual, mensaje)
        
        if respuesta_ia:
            with st.chat_message("assistant"):
                respuesta_ia = st.write_stream(generar_respuesta(respuesta_ia))
                actualizar_historial("assistant", respuesta_ia, "👾")
                st.rerun()


if __name__ == "__main__":
    main()