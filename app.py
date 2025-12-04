# Calculadora de Aceros FIS - Streamlit Application
# Este es código Python, debe ejecutarse con: streamlit run app.py

"""
IMPORTANTE: Este código debe guardarse en un archivo .py y ejecutarse localmente.
Claude.ai no puede ejecutar aplicaciones Streamlit directamente.

INSTRUCCIONES PARA USAR:
1. Copia este código completo en un archivo llamado "app.py"
2. Instala dependencias: pip install streamlit pandas plotly numpy
3. Ejecuta: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(
    page_title="Aceros FIS - Selector de Aceros al Carbono",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
st.markdown("""
<style>
    /* Paleta de colores */
    :root {
        --primary: #1E3A8A;
        --secondary: #F59E0B;
        --success: #10B981;
        --warning: #EF4444;
        --bg: #F9FAFB;
    }
    
    /* Ocultar menú de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header personalizado */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    /* Cards de modo */
    .mode-card {
        background: white;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .mode-card:hover {
        border-color: #F59E0B;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-4px);
    }
    
    /* Resultados */
    .result-card {
        background: white;
        border-left: 4px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .medal {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    /* Barras de progreso */
    .progress-bar {
        background: #E5E7EB;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3B82F6, #1E3A8A);
        transition: width 0.5s ease;
    }
    
    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
        transform: translateY(-2px);
    }
    
    /* Logo ASCII */
    .logo-ascii {
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        line-height: 1;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOGO ASCII ART ====================
def render_logo():
    logo = """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     █████╗  ██████╗███████╗██████╗   ║
    ║    ██╔══██╗██╔════╝██╔════╝██╔══██╗  ║
    ║    ███████║██║     █████╗  ██████╔╝  ║
    ║    ██╔══██║██║     ██╔══╝  ██╔══██╗  ║
    ║    ██║  ██║╚██████╗███████╗██║  ██║  ║
    ║    ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝  ║
    ║                                       ║
    ║    ███████╗██╗███████╗                ║
    ║    ██╔════╝██║██╔════╝                ║
    ║    █████╗  ██║███████╗                ║
    ║    ██╔══╝  ██║╚════██║                ║
    ║    ██║     ██║███████║                ║
    ║    ╚═╝     ╚═╝╚══════╝                ║
    ║                                       ║
    ║   INGENIERÍA EN MATERIALES            ║
    ║   UNAM - Facultad de Ingeniería       ║
    ╚═══════════════════════════════════════╝
    """
    st.markdown(f'<div class="logo-ascii">{logo}</div>', unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
@st.cache_data
def load_data():
    """Carga y preprocesa el dataset de aceros"""
    # NOTA: Reemplazar con la ruta real del archivo CSV
    try:
        df = pd.read_csv("steel_data.csv")
    except:
        # Datos de ejemplo si no se encuentra el archivo
        df = pd.DataFrame({
            'SAE Grade': ['1020', '1045', '1541', '4140', '4150', '5150'],
            'Condition': ['Hot Rolled', 'Normalized', 'Annealed', 'Q&T', 'Normalized', 'Q&T'],
            'UTS (MPa)': [420, 570, 620, 980, 760, 890],
            'YS (MPa)': [350, 380, 430, 750, 520, 650],
            'Hardness (HB)': [120, 165, 180, 290, 220, 260],
            'Elongation (%)': [25, 20, 18, 14, 16, 13],
            'C (Min)': [0.18, 0.43, 0.36, 0.38, 0.48, 0.48],
            'C (Max)': [0.23, 0.50, 0.44, 0.43, 0.53, 0.53]
        })
    
    # Calcular C_avg
    if 'C (Min)' in df.columns and 'C (Max)' in df.columns:
        df['C_avg'] = (df['C (Min)'] + df['C (Max)']) / 2
    
    # Simplificar tratamientos
    if 'Condition' in df.columns:
        df['Condition_simple'] = df['Condition'].str.split(' at ').str[0].str.strip()
    
    return df

# ==================== FUNCIONES DE SCORING ====================
def calculate_score(row, filters):
    """Calcula puntuación de coincidencia (0-5 estrellas)"""
    score = 5.0
    
    # Penalizar por desviación de requisitos
    if 'uts_min' in filters and pd.notna(row.get('UTS (MPa)')):
        if row['UTS (MPa)'] < filters['uts_min']:
            score -= 2
    
    if 'elongation_min' in filters and pd.notna(row.get('Elongation (%)')):
        if row['Elongation (%)'] < filters['elongation_min']:
            score -= 1.5
    
    if 'treatments' in filters and filters['treatments']:
        if row.get('Condition_simple') not in filters['treatments']:
            score -= 1
    
    return max(0, min(5, score))

def render_stars(score):
    """Convierte puntuación numérica a estrellas"""
    full_stars = int(score)
    half_star = 1 if (score - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "★" * full_stars + "⯨" * half_star + "☆" * empty_stars

# ==================== PÁGINA INICIAL ====================
def page_landing():
    """Página de bienvenida"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    render_logo()
    st.markdown("""
    ## 🔩 Selector de Aceros al Carbono
    
    Encuentra el acero adecuado para tu proyecto basándote en datos técnicos reales
    
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Aceros Analizados", "190+", delta="Dataset completo")
    with col2:
        st.metric("Tratamientos", "5", delta="Térmicos y mecánicos")
    with col3:
        st.metric("Propiedades", "4", delta="UTS, YS, Dureza, Elongación")
    
    st.markdown("---")
    
    if st.button("🚀 COMENZAR SELECCIÓN", use_container_width=True):
        st.session_state.page = 'selector'
        st.rerun()

# ==================== SELECTOR DE MODO ====================
def page_mode_selector():
    """Página para elegir modo de búsqueda"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("### ¿Qué tipo de proyecto tienes?")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.markdown("### 🏠 MODO SIMPLE")
        st.markdown("**Para todos**")
        st.write("Necesito algo resistente para...")
        st.write("✓ Sin términos técnicos")
        st.write("✓ Guiado paso a paso")
        if st.button("Seleccionar Simple", use_container_width=True, key="btn_simple"):
            st.session_state.mode = 'simple'
            st.session_state.page = 'app'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ MODO TÉCNICO")
        st.markdown("**Para ingenieros**")
        st.write("Conozco las propiedades que necesito")
        st.write("✓ Control fino")
        st.write("✓ Filtros avanzados")
        if st.button("Seleccionar Técnico", use_container_width=True, key="btn_tech"):
            st.session_state.mode = 'technical'
            st.session_state.page = 'app'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="mode-card">', unsafe_allow_html=True)
        st.markdown("### 📊 MODO EXPLORAR")
        st.markdown("**Para análisis**")
        st.write("Quiero ver tendencias y datos")
        st.write("✓ Visualizaciones")
        st.write("✓ Gráficas interactivas")
        if st.button("Seleccionar Explorar", use_container_width=True, key="btn_explore"):
            st.session_state.mode = 'explore'
            st.session_state.page = 'app'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MODO SIMPLE ====================
def mode_simple(df):
    """Modo guiado para usuarios no técnicos"""
    st.sidebar.markdown("## 🏠 MODO SIMPLE")
    st.sidebar.markdown("---")
    
    # Paso 1: Aplicación
    st.sidebar.markdown("### PASO 1 DE 3")
    st.sidebar.markdown("¿Para qué lo usarás?")
    use_case = st.sidebar.radio(
        "Aplicación:",
        ["Construcción/cercas", "Herramientas", "Muebles/estructura", 
         "Piezas mecánicas", "Cuchillos/corte"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Paso 2: Soldadura
    st.sidebar.markdown("### PASO 2 DE 3")
    st.sidebar.markdown("¿Necesitas soldarlo?")
    welding = st.sidebar.radio(
        "Soldadura:",
        ["Sí, mucho", "Tal vez", "No"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Paso 3: Dureza
    st.sidebar.markdown("### PASO 3 DE 3")
    st.sidebar.markdown("¿Qué tan duro debe ser?")
    hardness_level = st.sidebar.slider(
        "Dureza",
        1, 5, 3,
        label_visibility="collapsed"
    )
    
    if st.sidebar.button("🔍 BUSCAR ACEROS", use_container_width=True):
        # Lógica de filtrado simplificada
        recommendations = filter_simple_mode(df, use_case, welding, hardness_level)
        display_simple_results(recommendations)

def filter_simple_mode(df, use_case, welding, hardness_level):
    """Filtra aceros según criterios simples"""
    filtered = df.copy()
    
    # Lógica de filtrado basada en casos de uso
    if welding == "Sí, mucho":
        filtered = filtered[filtered['C_avg'] < 0.30]
    elif welding == "Tal vez":
        filtered = filtered[filtered['C_avg'] < 0.45]
    
    if hardness_level <= 2:
        filtered = filtered[filtered['Hardness (HB)'] < 180]
    elif hardness_level >= 4:
        filtered = filtered[filtered['Hardness (HB)'] > 220]
    
    return filtered.head(3)

def display_simple_results(recommendations):
    """Muestra resultados en modo simple"""
    st.markdown("## RECOMENDACIONES PARA TU PROYECTO")
    
    if len(recommendations) == 0:
        st.warning("No se encontraron aceros con estos criterios. Intenta ajustar tus requisitos.")
        return
    
    medals = ["🥇", "🥈", "🥉"]
    labels = ["MEJOR OPCIÓN", "ALTERNATIVA", "OTRA OPCIÓN"]
    
    for idx, (_, row) in enumerate(recommendations.iterrows()):
        if idx < 3:
            st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"## {medals[idx]} {labels[idx]}: SAE {row['SAE Grade']} ({row['Condition_simple']})")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("✓ Características principales")
                st.progress(int(row['UTS (MPa)'])/1000, text=f"💪 Resistencia: {row['UTS (MPa)']} MPa")
                st.progress(int(row['Hardness (HB)'])/400, text=f"🔨 Dureza: {row['Hardness (HB)']} HB")
                st.progress(int(row['Elongation (%)'])/40, text=f"🌊 Flexibilidad: {row['Elongation (%)']}%")
            
            with col2:
                st.metric("Carbono", f"{row['C_avg']:.2f}%")
                st.metric("Límite Elástico", f"{row['YS (MPa)']} MPa")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== MODO TÉCNICO ====================
def mode_technical(df):
    """Modo avanzado con filtros técnicos"""
    st.sidebar.markdown("## ⚙️ MODO TÉCNICO")
    st.sidebar.markdown("---")
    
    # Filtros numéricos
    st.sidebar.markdown("### Resistencia a la Tracción (MPa)")
    uts_range = st.sidebar.slider(
        "UTS",
        int(df['UTS (MPa)'].min()), 
        int(df['UTS (MPa)'].max()),
        (int(df['UTS (MPa)'].min()), int(df['UTS (MPa)'].max())),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### Límite Elástico (MPa)")
    ys_range = st.sidebar.slider(
        "YS",
        int(df['YS (MPa)'].min()), 
        int(df['YS (MPa)'].max()),
        (int(df['YS (MPa)'].min()), int(df['YS (MPa)'].max())),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### Dureza (HB)")
    hardness_range = st.sidebar.slider(
        "Hardness",
        int(df['Hardness (HB)'].min()), 
        int(df['Hardness (HB)'].max()),
        (int(df['Hardness (HB)'].min()), int(df['Hardness (HB)'].max())),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### Elongación (%)")
    elong_range = st.sidebar.slider(
        "Elongation",
        int(df['Elongation (%)'].min()), 
        int(df['Elongation (%)'].max()),
        (int(df['Elongation (%)'].min()), int(df['Elongation (%)'].max())),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Tratamientos
    st.sidebar.markdown("### Tratamientos Disponibles")
    treatments = df['Condition_simple'].unique()
    selected_treatments = st.sidebar.multiselect(
        "Tratamientos",
        treatments,
        default=list(treatments),
        label_visibility="collapsed"
    )
    
    # Aplicar filtros
    filtered = df[
        (df['UTS (MPa)'] >= uts_range[0]) & (df['UTS (MPa)'] <= uts_range[1]) &
        (df['YS (MPa)'] >= ys_range[0]) & (df['YS (MPa)'] <= ys_range[1]) &
        (df['Hardness (HB)'] >= hardness_range[0]) & (df['Hardness (HB)'] <= hardness_range[1]) &
        (df['Elongation (%)'] >= elong_range[0]) & (df['Elongation (%)'] <= elong_range[1]) &
        (df['Condition_simple'].isin(selected_treatments))
    ]
    
    # Mostrar resultados
    st.markdown(f"## RESULTADOS ({len(filtered)} aceros coinciden)")
    
    if len(filtered) > 0:
        # Tabla sorteable
        st.dataframe(
            filtered[['SAE Grade', 'Condition_simple', 'UTS (MPa)', 'YS (MPa)', 
                     'Hardness (HB)', 'Elongation (%)', 'C_avg']],
            use_container_width=True,
            height=400
        )
        
        # Botón de exportación
        csv = filtered.to_csv(index=False)
        st.download_button(
            "📥 Exportar a CSV",
            csv,
            "aceros_filtrados.csv",
            "text/csv"
        )
    else:
        st.warning("No se encontraron aceros con estos criterios. Ajusta los filtros.")

# ==================== MODO EXPLORAR ====================
def mode_explore(df):
    """Modo de visualización y análisis"""
    st.markdown("## 📊 EXPLORACIÓN DE DATOS")
    
    tabs = st.tabs(["Propiedades vs %C", "Tratamientos", "Comparación"])
    
    with tabs[0]:
        st.markdown("### Propiedades Mecánicas vs Contenido de Carbono")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['C_avg'], y=df['UTS (MPa)'],
            mode='markers+lines',
            name='UTS',
            line=dict(color='#3B82F6')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['C_avg'], y=df['YS (MPa)'],
            mode='markers+lines',
            name='YS',
            line=dict(color='#10B981')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['C_avg'], y=df['Hardness (HB)'] * 4,
            mode='markers+lines',
            name='Dureza (×4)',
            line=dict(color='#EF4444')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['C_avg'], y=df['Elongation (%)'] * 20,
            mode='markers+lines',
            name='Elongación (×20)',
            line=dict(color='#F59E0B')
        ))
        
        fig.update_layout(
            xaxis_title="Contenido de Carbono (%)",
            yaxis_title="Valor",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### Comparación de Tratamientos Térmicos")
        
        property_choice = st.selectbox(
            "Selecciona propiedad:",
            ["UTS (MPa)", "YS (MPa)", "Hardness (HB)", "Elongation (%)"]
        )
        
        fig = px.box(
            df, 
            x='Condition_simple', 
            y=property_choice,
            color='Condition_simple',
            title=f"Distribución de {property_choice} por Tratamiento"
        )
        
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### Comparación Directa de Aceros")
        
        selected_steels = st.multiselect(
            "Selecciona hasta 3 aceros para comparar:",
            df['SAE Grade'].unique(),
            max_selections=3
        )
        
        if selected_steels:
            comparison_df = df[df['SAE Grade'].isin(selected_steels)]
            
            fig = go.Figure()
            
            properties = ['UTS (MPa)', 'YS (MPa)', 'Hardness (HB)', 'Elongation (%)']
            
            for steel in selected_steels:
                steel_data = comparison_df[comparison_df['SAE Grade'] == steel].iloc[0]
                values = [steel_data[prop] for prop in properties]
                
                fig.add_trace(go.Bar(
                    name=f"SAE {steel}",
                    x=properties,
                    y=values
                ))
            
            fig.update_layout(
                barmode='group',
                height=500,
                title="Comparación de Propiedades"
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ==================== APLICACIÓN PRINCIPAL ====================
def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado de sesión
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    
    # Cargar datos
    df = load_data()
    
    # Navegación
    if st.session_state.page == 'landing':
        page_landing()
    
    elif st.session_state.page == 'selector':
        page_mode_selector()
    
    elif st.session_state.page == 'app':
        # Botón de regreso
        if st.sidebar.button("⬅️ Cambiar Modo"):
            st.session_state.page = 'selector'
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # Ejecutar modo seleccionado
        if st.session_state.mode == 'simple':
            mode_simple(df)
        elif st.session_state.mode == 'technical':
            mode_technical(df)
        elif st.session_state.mode == 'explore':
            mode_explore(df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; font-size: 0.875rem;'>
        <p><strong>Aceros FIS</strong> - Desarrollado por Fernando Alfaro, Samuel Estrada, Israel González</p>
        <p>UNAM - Facultad de Ingeniería | Ingeniería de Materiales 2026-1</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()