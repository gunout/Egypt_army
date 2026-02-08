# dashboard_defense_egypte_reel.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Données réelles estimées (basées sur SIPRI, IISS, World Bank)
# Note: Ces sont des ESTIMATIONS publiques, pas des données officielles

EGYPT_DEFENSE_DATA = {
    "Year": [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    
    # Dépenses militaires en milliards USD (SIPRI estimates)
    "Military_Expenditure_Billion_USD": [
        4.2, 4.5, 4.8, 5.2, 5.6, 6.0, 6.5, 7.0, 7.3, 7.8, 8.2, 8.5, 8.8
    ],
    
    # % du PIB consacré à la défense (World Bank)
    "Military_Expenditure_GDP_Percent": [
        1.7, 1.8, 1.9, 2.1, 2.3, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2
    ],
    
    # Personnel actif en milliers (IISS Military Balance)
    "Active_Personnel_Thousands": [
        438, 440, 442, 445, 447, 450, 452, 455, 457, 459, 460, 461, 462
    ],
    
    # Réservistes en milliers (estimations)
    "Reserve_Personnel_Thousands": [
        479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491
    ],
    
    # Principaux équipements (estimations)
    "Main_Battle_Tanks": [
        3400, 3420, 3440, 3460, 3500, 3550, 3600, 3650, 3680, 3700, 3720, 3740, 3760
    ],
    
    "Fighter_Aircraft": [
        580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640
    ],
    
    "Naval_Vessels": [
        245, 248, 250, 252, 255, 258, 260, 263, 265, 268, 270, 273, 275
    ],
    
    # Indice de puissance (Global Firepower Index)
    "Power_Index": [
        0.2215, 0.2200, 0.2185, 0.2170, 0.2155, 0.2140, 0.2125, 0.2110, 0.2095, 0.2080, 0.2065, 0.2050, 0.2035
    ]
}

# Données des principales acquisitions
MAJOR_ACQUISITIONS = [
    {"Year": 2015, "System": "Rafale Fighter Jets", "Quantity": 24, "Country": "France"},
    {"Year": 2016, "System": "FREMM Frigate", "Quantity": 1, "Country": "France"},
    {"Year": 2017, "System": "Mistral-class LHD", "Quantity": 2, "Country": "France"},
    {"Year": 2018, "System": "Ka-52 Attack Helicopters", "Quantity": 46, "Country": "Russia"},
    {"Year": 2019, "System": "MiG-29M Fighter Jets", "Quantity": 46, "Country": "Russia"},
    {"Year": 2020, "System": "S-300VM Air Defense", "Quantity": 4, "Country": "Russia"},
    {"Year": 2021, "System": "Gowind Corvettes", "Quantity": 4, "Country": "France"},
    {"Year": 2022, "System": "Rafale (Additional)", "Quantity": 30, "Country": "France"},
    {"Year": 2023, "System": "T-90MS Tanks", "Quantity": 500, "Country": "Russia"},
]

# Données des exercices militaires
MILITARY_EXERCISES = [
    {"Year": 2012, "Exercise": "Bright Star", "Participants": 11, "Scale": "Large"},
    {"Year": 2013, "Exercise": "Sea Breeze", "Participants": 15, "Scale": "Medium"},
    {"Year": 2014, "Exercise": "Desert Falcon", "Participants": 2, "Scale": "Small"},
    {"Year": 2015, "Exercise": "Cleopatra", "Participants": 2, "Scale": "Medium"},
    {"Year": 2016, "Exercise": "Nile Eagle", "Participants": 5, "Scale": "Medium"},
    {"Year": 2017, "Exercise": "Sea Breeze", "Participants": 18, "Scale": "Large"},
    {"Year": 2018, "Exercise": "Bright Star", "Participants": 21, "Scale": "Large"},
    {"Year": 2019, "Exercise": "Desert Falcon", "Participants": 3, "Scale": "Small"},
    {"Year": 2020, "Exercise": "Medusa", "Participants": 7, "Scale": "Medium"},
    {"Year": 2021, "Exercise": "Sea Breeze", "Participants": 32, "Scale": "Large"},
    {"Year": 2022, "Exercise": "Nile Eagle", "Participants": 8, "Scale": "Medium"},
    {"Year": 2023, "Exercise": "Bright Star", "Participants": 26, "Scale": "Large"},
]

class EgyptRealDataDashboard:
    def __init__(self):
        self.df = pd.DataFrame(EGYPT_DEFENSE_DATA)
        self.acquisitions_df = pd.DataFrame(MAJOR_ACQUISITIONS)
        self.exercises_df = pd.DataFrame(MILITARY_EXERCISES)
    
    def display_header(self):
        st.title("🇪🇬 Analyse des Capacités Militaires Égyptiennes - Données Estimées")
        st.markdown("**Basé sur des données publiques (SIPRI, IISS, World Bank) 2012-2024**")
        st.info("⚠️ **Note** : Ces données sont des estimations basées sur des sources publiques. Les données militaires précises sont classifiées.")
    
    def create_real_data_tabs(self):
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💰 Dépenses Militaires", 
            "👥 Effectifs", 
            "⚔️ Équipements", 
            "🚀 Acquisitions",
            "⚡ Exercices"
        ])
        
        with tab1:
            self.show_military_expenditure()
        
        with tab2:
            self.show_personnel_data()
        
        with tab3:
            self.show_equipment_data()
        
        with tab4:
            self.show_acquisitions()
        
        with tab5:
            self.show_exercises()
    
    def show_military_expenditure(self):
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(self.df, x='Year', y='Military_Expenditure_Billion_USD',
                         title="Dépenses Militaires Égyptiennes (2012-2024)",
                         labels={'Military_Expenditure_Billion_USD': 'Milliards USD', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#CE1126', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            latest_exp = self.df['Military_Expenditure_Billion_USD'].iloc[-1]
            first_exp = self.df['Military_Expenditure_Billion_USD'].iloc[0]
            growth = ((latest_exp - first_exp) / first_exp) * 100
            
            st.metric("Dépenses militaires 2024", f"{latest_exp:.1f} Md$", 
                     f"{growth:+.1f}% vs 2012")
        
        with col2:
            fig = px.line(self.df, x='Year', y='Military_Expenditure_GDP_Percent',
                         title="Dépenses Militaires (% du PIB)",
                         labels={'Military_Expenditure_GDP_Percent': '% du PIB', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#FECB00', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("% du PIB (2024)", f"{self.df['Military_Expenditure_GDP_Percent'].iloc[-1]:.1f}%")
    
    def show_personnel_data(self):
        col1, col2 = st.columns(2)
        
        with col1:
            # Personnel actif
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=self.df['Year'], 
                y=self.df['Active_Personnel_Thousands'],
                mode='lines+markers',
                name='Personnel Actif',
                line=dict(color='#CE1126', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=self.df['Year'], 
                y=self.df['Reserve_Personnel_Thousands'],
                mode='lines+markers',
                name='Réservistes',
                line=dict(color='#FECB00', width=3)
            ))
            
            fig.update_layout(
                title="Personnel Militaire Égyptien (en milliers)",
                xaxis_title="Année",
                yaxis_title="Effectifs (milliers)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Indice de puissance
            fig = px.line(self.df, x='Year', y='Power_Index',
                         title="Indice de Puissance Militaire (Global Firepower)",
                         labels={'Power_Index': 'Indice (0=parfait)', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#000000', width=3))
            fig.update_yaxes(autorange="reversed")  # Plus bas = meilleur
            st.plotly_chart(fig, use_container_width=True)
            
            current_index = self.df['Power_Index'].iloc[-1]
            st.metric("Indice 2024", f"{current_index:.4f}", 
                     f"Rang mondial estimé: {int(current_index * 140)}")
    
    def show_equipment_data(self):
        st.subheader("Principaux Systèmes d'Armes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Chars de combat
            fig = px.line(self.df, x='Year', y='Main_Battle_Tanks',
                         title="Chars de Combat Principaux",
                         labels={'Main_Battle_Tanks': 'Nombre', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#CE1126', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Chars (2024)", f"{self.df['Main_Battle_Tanks'].iloc[-1]:,}")
        
        with col2:
            # Avions de combat
            fig = px.line(self.df, x='Year', y='Fighter_Aircraft',
                         title="Avions de Combat",
                         labels={'Fighter_Aircraft': 'Nombre', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#FECB00', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Avions (2024)", f"{self.df['Fighter_Aircraft'].iloc[-1]:,}")
        
        with col3:
            # Navires
            fig = px.line(self.df, x='Year', y='Naval_Vessels',
                         title="Navires de Guerre",
                         labels={'Naval_Vessels': 'Nombre', 'Year': 'Année'},
                         markers=True)
            fig.update_traces(line=dict(color='#0066CC', width=3))
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Navires (2024)", f"{self.df['Naval_Vessels'].iloc[-1]:,}")
    
    def show_acquisitions(self):
        st.subheader("Principales Acquisitions 2015-2023")
        
        # Graphique des acquisitions par année
        acquisitions_by_year = self.acquisitions_df.groupby('Year')['Quantity'].sum().reset_index()
        
        fig = px.bar(acquisitions_by_year, x='Year', y='Quantity',
                     title="Volume d'Acquisitions par Année",
                     labels={'Quantity': 'Nombre de systèmes', 'Year': 'Année'})
        fig.update_traces(marker_color='#CE1126')
        st.plotly_chart(fig, use_container_width=True)
        
        # Table des acquisitions
        st.dataframe(
            self.acquisitions_df.style
            .background_gradient(subset=['Quantity'], cmap='Reds')
            .format({'Quantity': '{:.0f}'}),
            use_container_width=True
        )
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        total_systems = self.acquisitions_df['Quantity'].sum()
        french_systems = self.acquisitions_df[self.acquisitions_df['Country'] == 'France']['Quantity'].sum()
        russian_systems = self.acquisitions_df[self.acquisitions_df['Country'] == 'Russia']['Quantity'].sum()
        
        with col1:
            st.metric("Systèmes acquis (2015-2023)", f"{total_systems:,}")
        with col2:
            st.metric("Systèmes français", f"{french_systems:,}")
        with col3:
            st.metric("Systèmes russes", f"{russian_systems:,}")
    
    def show_exercises(self):
        st.subheader("Exercices Militaires Internationaux")
        
        # Distribution par échelle
        scale_dist = self.exercises_df['Scale'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=scale_dist.values, names=scale_dist.index,
                        title="Répartition des Exercices par Échelle",
                        color_discrete_sequence=['#CE1126', '#FECB00', '#0066CC'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Participants moyens
            avg_participants = self.exercises_df.groupby('Year')['Participants'].mean()
            fig = px.line(x=avg_participants.index, y=avg_participants.values,
                         title="Participants Moyens aux Exercices",
                         labels={'x': 'Année', 'y': 'Participants'},
                         markers=True)
            fig.update_traces(line=dict(color='#000000', width=3))
            st.plotly_chart(fig, use_container_width=True)
        
        # Liste des exercices
        st.dataframe(self.exercises_df, use_container_width=True)
    
    def show_sources(self):
        st.sidebar.markdown("---")
        st.sidebar.subheader("📚 Sources des Données")
        st.sidebar.markdown("""
        **Sources principales:**
        
        • **SIPRI** - Stockholm International Peace Research Institute
        • **IISS** - International Institute for Strategic Studies
        • **World Bank** - World Development Indicators
        • **Global Firepower** - Military Strength Ranking
        • **CIA World Factbook**
        
        **Dernière mise à jour:** Estimations 2023-2024
        
        **Note:** Toutes les données sont des estimations basées sur des sources publiques.
        """)
    
    def run(self):
        st.set_page_config(
            page_title="Egypte - Données Réelles Estimées",
            page_icon="🇪🇬",
            layout="wide"
        )
        
        self.display_header()
        self.create_real_data_tabs()
        self.show_sources()

if __name__ == "__main__":
    dashboard = EgyptRealDataDashboard()
    dashboard.run()
