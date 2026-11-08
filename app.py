import streamlit as st
import pandas as pd
import os
st.set_page_config(page_title="Sistema ISP", layout="wide")
ARCHIVO="clientes.csv"
if not os.path.exists(ARCHIVO):
    pd.DataFrame(columns=["Nombre","Telefono","Direccion","Plan","Precio","Estado"]).to_csv(ARCHIVO, index=False)
df=pd.read_csv(ARCHIVO)
st.sidebar.title("Administración")
menu=st.sidebar.radio("Menú", ["Panel","Clientes","Finanzas"], key="menu_final")
if st.sidebar.button("Cerrar Sesión", key="cerrar_final"):
    st.rerun()
if menu=="Panel":
    st.title("Panel")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Clientes", len(df))
    c2.metric("Activos", len(df[df["Estado"]=="Activo"]) if len(df)>0 else 0)
    c3.metric("Suspendidos", len(df[df["Estado"]=="Suspendido"]) if len(df)>0 else 0)
    c4.metric("Ingreso Mes", f"${df['Precio'].sum() if len(df)>0 else 0:.2f}")
    if len(df)>0:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay clientes. Ve a Clientes para agregar uno.")
elif menu=="Clientes":
    st.title("Clientes")
    with st.form("f", clear_on_submit=True):
        n=st.text_input("Nombre")
        t=st.text_input("Telefono / WhatsApp")
        d=st.text_input("Direccion")
        p=st.selectbox("Plan", ["50 Mbps - $250","100 Mbps - $350"])
        pr=st.number_input("Precio", value=250)
        e=st.selectbox("Estado", ["Activo","Suspendido"])
        if st.form_submit_button("Guardar Cliente"):
            if n and t:
                nuevo=pd.DataFrame([[n,t,d,p,pr,e]], columns=df.columns)
                pd.concat([df, nuevo]).to_csv(ARCHIVO, index=False)
                st.success("Guardado!")
                st.rerun()
    st.dataframe(df, use_container_width=True)
else:
    st.title("Finanzas")
    st.metric("Total por cobrar", f"${df['Precio'].sum() if len(df)>0 else 0:.2f}")
    st.dataframe(df, use_container_width=True)