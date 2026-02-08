# dashboard_defense_egypte.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse de la Défense Égyptienne - Forces Armées",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #CE1126, #FECB00, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #CE1126;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #000000;
        border-bottom: 2px solid #FECB00;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .pays-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #CE1126;
        background-color: #f8f9fa;
    }
    .egyptian-flag {
        background: linear-gradient(45deg, #CE1126, #FECB00, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .doctrine-card {
        background: linear-gradient(135deg, #CE1126, #FECB00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .nile-bg {
        background: linear-gradient(to right, #0066CC, #00CC99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

class DefenseEgypteDashboard:
    def __init__(self):
        self.branches_options = self.define_branches_options()
        self.programmes_options = self.define_programmes_options()
        
    def define_branches_options(self):
        """Définit les branches militaires disponibles pour l'analyse"""
        return [
            "Forces Armées Égyptiennes", "Armée de Terre", "Marine Égyptienne", 
            "Force Aérienne Égyptienne", "Forces de Défense Aérienne", 
            "Forces Spéciales Égyptiennes", "Garde Républicaine"
        ]
    
    def define_programmes_options(self):
        """Définit les programmes militaires disponibles"""
        return [
            "Modernisation des Forces", "Programme Naval", "Défense Aérienne",
            "Sécurité des Frontières", "Coopération Militaire", "Industrie de Défense"
        ]
    
    def generate_defense_data(self, selection):
        """Génère des données de défense simulées pour le dashboard"""
        # Période d'analyse : 2012-2027
        annees = list(range(2012, 2028))
        
        # Configuration de base selon la sélection
        config = self.get_config(selection)
        
        data = {
            'Annee': annees,
            'Budget_Defense_Mds': self.simulate_budget(annees, config),
            'Personnel_Milliers': self.simulate_personnel(annees, config),
            'Exercices_Militaires': self.simulate_military_exercises(annees, config),
            'Readiness_Operative': self.simulate_readiness(annees),
            'Capacite_Defense': self.simulate_defense_capacity(annees),
            'Temps_Deploiement_Jours': self.simulate_deployment_time(annees),
            'Equipements_Modernes': self.simulate_modern_equipment(annees),
            'Cooperation_Internationale': self.simulate_international_coop(annees),
            'Industrie_Locale': self.simulate_local_industry(annees),
            'Securite_Frontieres': self.simulate_border_security(annees)
        }
        
        # Ajouter des indicateurs spécifiques
        if 'naval' in config.get('priorites', []):
            data['Navires_Modernes'] = self.simulate_naval_modernization(annees)
        if 'aerien' in config.get('priorites', []):
            data['Avions_Combat'] = self.simulate_combat_aircraft(annees)
        if 'defense_aerienne' in config.get('priorites', []):
            data['Systemes_Defense_Aerienne'] = self.simulate_air_defense(annees)
        
        return pd.DataFrame(data), config
    
    def get_config(self, selection):
        """Retourne la configuration pour une branche/programme donné"""
        configs = {
            "Forces Armées Égyptiennes": {
                "type": "armee_totale",
                "budget_base": 4.5,
                "personnel_base": 450,  # en milliers
                "exercices_base": 120,
                "priorites": ["modernisation", "defense_aerienne", "naval", "securite_frontieres"]
            },
            "Armée de Terre": {
                "type": "branche",
                "personnel_base": 310,  # en milliers
                "exercices_base": 85,
                "priorites": ["blindes", "artillerie", "forces_mecanisees", "securite_sinai"]
            },
            "Marine Égyptienne": {
                "type": "branche", 
                "personnel_base": 18,  # en milliers
                "exercices_base": 45,
                "priorites": ["corvettes", "fregates", "sous_marins", "defense_cotes"]
            },
            "Force Aérienne Égyptienne": {
                "type": "branche",
                "personnel_base": 35,  # en milliers
                "exercices_base": 65,
                "priorites": ["avions_chasse", "helicopteres_attaque", "transport", "surveillance"]
            },
            "Forces de Défense Aérienne": {
                "type": "branche_speciale",
                "personnel_base": 85,  # en milliers
                "exercices_base": 40,
                "priorites": ["missiles_sol_air", "systemes_radars", "defense_strategique"]
            },
            "Modernisation des Forces": {
                "type": "programme_strategique",
                "budget_base": 1.8,
                "priorites": ["equipements_occidentaux", "diversification", "maintien_capacite"]
            },
            "Programme Naval": {
                "type": "programme_strategique",
                "budget_base": 1.2,
                "priorites": ["corvettes", "fregates", "patrouilleurs", "sous_marins"]
            }
        }
        
        return configs.get(selection, {
            "type": "branche",
            "personnel_base": 50,
            "exercices_base": 30,
            "priorites": ["defense_generique"]
        })
    
    def simulate_budget(self, annees, config):
        """Simule l'évolution du budget défense"""
        budget_base = config.get('budget_base', 3.0)
        # Forte augmentation après 2014 (émergence de nouvelles menaces)
        budgets = []
        for annee in annees:
            base = budget_base * (1 + 0.05 * (annee - 2012))
            if annee >= 2015:
                base *= 1.3  # Augmentation après les événements régionaux
            if annee >= 2020:
                base *= 1.2  # Modernisation accélérée
            budgets.append(base)
        return budgets
    
    def simulate_personnel(self, annees, config):
        """Simule l'évolution des effectifs (en milliers)"""
        personnel_base = config.get('personnel_base', 100)
        return [personnel_base * (1 + 0.015 * (annee - 2012)) for annee in annees]
    
    def simulate_military_exercises(self, annees, config):
        """Simule les exercices militaires"""
        base = config.get('exercices_base', 50)
        # Augmentation des exercices internationaux après 2015
        return [base * (1 + 0.08 * (annee - 2012)) for annee in annees]
    
    def simulate_readiness(self, annees):
        """Simule le niveau de préparation opérationnelle"""
        # Forte amélioration après 2014
        readiness = []
        for annee in annees:
            if annee < 2014:
                readiness.append(70)
            elif annee < 2018:
                readiness.append(75 + 2 * (annee - 2014))
            else:
                readiness.append(min(85 + 1 * (annee - 2018), 95))
        return readiness
    
    def simulate_defense_capacity(self, annees):
        """Simule la capacité de défense"""
        # Amélioration constante
        return [min(65 + 2.5 * (annee - 2012), 90) for annee in annees]
    
    def simulate_deployment_time(self, annees):
        """Simule le temps de déploiement"""
        # Amélioration des capacités de projection
        return [max(72 - 2 * (annee - 2012), 48) for annee in annees]
    
    def simulate_modern_equipment(self, annees):
        """Simule l'acquisition d'équipements modernes"""
        # Accélération après 2015 avec les contrats internationaux
        equipements = []
        for annee in annees:
            base = 100 * (1 + 0.1 * (annee - 2012))
            if annee >= 2015:
                base *= 1.5  # Contrats avec la France, Russie, etc.
            equipements.append(min(base, 800))
        return equipements
    
    def simulate_international_coop(self, annees):
        """Simule la coopération internationale"""
        return [min(50 + 4 * (annee - 2012), 85) for annee in annees]
    
    def simulate_local_industry(self, annees):
        """Simule le développement de l'industrie locale"""
        # Développement progressif de l'industrie militaire égyptienne
        return [min(40 + 3.5 * (annee - 2012), 75) for annee in annees]
    
    def simulate_border_security(self, annees):
        """Simule la sécurité des frontières"""
        # Renforcement important après 2014
        securite = []
        for annee in annees:
            if annee < 2014:
                securite.append(60)
            else:
                securite.append(min(70 + 2.5 * (annee - 2014), 90))
        return securite
    
    def simulate_naval_modernization(self, annees):
        """Simule la modernisation navale"""
        # Acquisition de nouvelles unités navales
        navires = []
        for annee in annees:
            base = 20 + 2 * (annee - 2012)
            if annee >= 2015:
                base += 15  # Acquisition de corvettes Gowind
            if annee >= 2020:
                base += 10  # Sous-marins Type 209
            navires.append(min(base, 80))
        return navires
    
    def simulate_combat_aircraft(self, annees):
        """Simule les avions de combat modernes"""
        # Modernisation de la flotte aérienne
        avions = []
        for annee in annees:
            base = 200 + 10 * (annee - 2012)
            if annee >= 2015:
                base += 50  # Acquisition de Rafale
            if annee >= 2020:
                base += 30  # Acquisition supplémentaire
            avions.append(min(base, 350))
        return avions
    
    def simulate_air_defense(self, annees):
        """Simule les systèmes de défense aérienne"""
        # Déploiement de systèmes modernes
        systemes = []
        for annee in annees:
            base = 40 + 5 * (annee - 2012)
            if annee >= 2017:
                base += 20  # Acquisition de S-300
            if annee >= 2022:
                base += 15  # Systèmes complémentaires
            systemes.append(min(base, 120))
        return systemes
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🌍 Analyse des Capacités Militaires Égyptiennes</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="egyptian-flag">🇪🇬 DÉFENSE ET SÉCURITÉ NATIONALE 🇪🇬</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Analyse stratégique des forces armées égyptiennes (2012-2027)**")
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Sélection du type d'analyse
        type_analyse = st.sidebar.radio(
            "Type d'analyse:",
            ["Branches Militaires", "Programmes Stratégiques", "Vue d'Ensemble Égypte"]
        )
        
        if type_analyse == "Branches Militaires":
            selection = st.sidebar.selectbox("Sélectionnez une branche:", self.branches_options)
        elif type_analyse == "Programmes Stratégiques":
            selection = st.sidebar.selectbox("Sélectionnez un programme:", self.programmes_options)
        else:
            selection = "Forces Armées Égyptiennes"
        
        # Options d'affichage
        st.sidebar.markdown("### 📊 Options de visualisation")
        show_projection = st.sidebar.checkbox("Afficher les projections 2023-2027", value=True)
        show_doctrine_analysis = st.sidebar.checkbox("Analyse de la doctrine militaire", value=True)
        
        return {
            'selection': selection,
            'type_analyse': type_analyse,
            'show_projection': show_projection,
            'show_doctrine_analysis': show_doctrine_analysis
        }
    
    def display_key_metrics(self, df, config):
        """Affiche les métriques clés"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS STRATÉGIQUES CLÉS</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques
        derniere_annee = df['Annee'].max()
        data_actuelle = df[df['Annee'] == derniere_annee].iloc[0]
        data_2012 = df[df['Annee'] == 2012].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'Budget_Defense_Mds' in df.columns:
                croissance_budget = ((data_actuelle['Budget_Defense_Mds'] - data_2012['Budget_Defense_Mds']) / 
                                   data_2012['Budget_Defense_Mds']) * 100
                st.metric(
                    "Budget Défense 2027",
                    f"{data_actuelle['Budget_Defense_Mds']:.1f} Md$",
                    f"{croissance_budget:+.1f}% vs 2012"
                )
        
        with col2:
            if 'Personnel_Milliers' in df.columns:
                evolution_personnel = ((data_actuelle['Personnel_Milliers'] - data_2012['Personnel_Milliers']) / 
                                     data_2012['Personnel_Milliers']) * 100
                st.metric(
                    "Effectifs 2027",
                    f"{data_actuelle['Personnel_Milliers']:,.0f} K",
                    f"{evolution_personnel:+.1f}% vs 2012"
                )
        
        with col3:
            croissance_defense = ((data_actuelle['Capacite_Defense'] - data_2012['Capacite_Defense']) / 
                                data_2012['Capacite_Defense']) * 100
            st.metric(
                "Capacité Défense 2027",
                f"{data_actuelle['Capacite_Defense']:.1f}%",
                f"{croissance_defense:+.1f}% vs 2012"
            )
        
        with col4:
            reduction_temps = ((data_2012['Temps_Deploiement_Jours'] - data_actuelle['Temps_Deploiement_Jours']) / 
                             data_2012['Temps_Deploiement_Jours']) * 100
            st.metric(
                "Temps Déploiement 2027",
                f"{data_actuelle['Temps_Deploiement_Jours']:.1f} jours",
                f"{reduction_temps:+.1f}% vs 2012"
            )
    
    def create_budget_analysis(self, df, config):
        """Analyse des budgets et effectifs"""
        st.markdown('<h3 class="section-header">💰 ANALYSE BUDGÉTAIRE ET EFFECTIFS</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Budget_Defense_Mds' in df.columns:
                fig = px.line(df, x='Annee', y='Budget_Defense_Mds',
                             title="Évolution du Budget de Défense (2012-2027)",
                             labels={'Budget_Defense_Mds': 'Budget (Md$)', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#CE1126', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Personnel_Milliers' in df.columns:
                fig = px.line(df, x='Annee', y='Personnel_Milliers',
                             title="Évolution des Effectifs (2012-2027)",
                             labels={'Personnel_Milliers': 'Effectifs (Milliers)', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#FECB00', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_military_activities_analysis(self, df, config):
        """Analyse des activités militaires"""
        st.markdown('<h3 class="section-header">⚔️ ACTIVITÉS MILITAIRES ET EXERCICES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='Annee', y='Exercices_Militaires',
                         title="Exercices Militaires (2012-2027)",
                         labels={'Exercices_Militaires': "Nombre d'exercices", 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#CE1126', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Equipements_Modernes' in df.columns:
                fig = px.line(df, x='Annee', y='Equipements_Modernes',
                             title="Équipements Modernes (2012-2027)",
                             labels={'Equipements_Modernes': 'Nombre d\'unités', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#FECB00', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_capabilities_analysis(self, df, config):
        """Analyse des capacités opérationnelles"""
        st.markdown('<h3 class="section-header">⚡ CAPACITÉS OPÉRATIONNELLES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique combiné des capacités
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Readiness_Operative'],
                                    mode='lines', name='Préparation Opérationnelle',
                                    line=dict(color='#CE1126', width=3)))
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Capacite_Defense'],
                                    mode='lines', name='Capacité de Défense',
                                    line=dict(color='#000000', width=3)))
            
            if 'Securite_Frontieres' in df.columns:
                fig.add_trace(go.Scatter(x=df['Annee'], y=df['Securite_Frontieres'],
                                        mode='lines', name='Sécurité Frontières',
                                        line=dict(color='#0066CC', width=3)))
            
            fig.update_layout(title="Évolution des Capacités Opérationnelles (2012-2027)",
                             xaxis_title="Année",
                             yaxis_title="Niveau (%)",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Coopération internationale et industrie locale
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Cooperation_Internationale'],
                                    mode='lines', name='Coopération Internationale',
                                    line=dict(color='#CE1126', width=3)))
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Industrie_Locale'],
                                    mode='lines', name='Industrie Locale',
                                    line=dict(color='#FECB00', width=3)))
            
            fig.update_layout(title="Coopération Internationale et Industrie Locale (2012-2027)",
                             xaxis_title="Année",
                             yaxis_title="Niveau (%)",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_programs_analysis(self, df, config):
        """Analyse des programmes stratégiques"""
        st.markdown('<h3 class="section-header">🚀 PROGRAMMES STRATÉGIQUES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Modernisation navale
            if 'Navires_Modernes' in df.columns:
                fig = px.line(df, x='Annee', y='Navires_Modernes',
                            title="Modernisation de la Marine (2012-2027)",
                            labels={'Navires_Modernes': 'Nombre de navires modernes', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#0066CC', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Force aérienne
            if 'Avions_Combat' in df.columns:
                fig = px.line(df, x='Annee', y='Avions_Combat',
                             title="Modernisation de la Force Aérienne (2012-2027)",
                             labels={'Avions_Combat': 'Avions de combat modernes', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#FECB00', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_doctrine_analysis(self, df, config):
        """Analyse de la doctrine militaire égyptienne"""
        st.markdown('<h3 class="section-header">🎯 DOCTRINE MILITAIRE ÉGYPTIENNE</h3>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div class="doctrine-card">
        <h4>🎯 Principes de la Stratégie de Défense Égyptienne</h4>
        <ul>
        <li><strong>Sécurité multidimensionnelle</strong> - Défense terrestre, aérienne, maritime et cyber</li>
        <li><strong>Équilibre stratégique</strong> - Maintien de l'équilibre régional</li>
        <li><strong>Modernisation continue</strong> - Acquisition et développement technologique</li>
        <li><strong>Coopération régionale</strong> - Partenariats stratégiques au Moyen-Orient</li>
        <li><strong>Défense des frontières</strong> - Sécurisation des frontières terrestres et maritimes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Développement de l'industrie locale
            fig = px.line(df, x='Annee', y='Industrie_Locale',
                         title="Développement de l'Industrie Militaire Locale (2012-2027)",
                         labels={'Industrie_Locale': 'Niveau (%)', 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#CE1126', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Indice de diversification
            diversification = [min(50 + 4 * (annee - 2012), 85) for annee in df['Annee']]
            fig = px.line(x=df['Annee'], y=diversification,
                         title="Diversification des Sources d'Équipements (2012-2027)",
                         labels={'x': 'Année', 'y': 'Diversification (%)'})
            fig.update_traces(line=dict(color='#FECB00', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_comparative_analysis(self, df, config):
        """Analyse comparative avant/après modernisation"""
        st.markdown('<h3 class="section-header">📊 ANALYSE COMPARATIVE</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des moyennes avant et après 2015 (accélération de la modernisation)
        avant_2015 = df[df['Annee'] <= 2015]
        apres_2015 = df[df['Annee'] > 2015]
        
        if len(avant_2015) > 0 and len(apres_2015) > 0:
            indicateurs = ['Capacite_Defense', 'Equipements_Modernes', 'Cooperation_Internationale']
            noms = ['Capacité Défense', 'Équipements Modernes', 'Coopération Internationale']
            
            valeurs_avant = [avant_2015[ind].mean() for ind in indicateurs]
            valeurs_apres = [apres_2015[ind].mean() for ind in indicateurs]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(name='2012-2015', x=noms, y=valeurs_avant,
                                marker_color='#CE1126'))
            fig.add_trace(go.Bar(name='2016-2027', x=noms, y=valeurs_apres,
                                marker_color='#FECB00'))
            
            fig.update_layout(title="Comparaison Avant/Après Modernisation Accélérée",
                             barmode='group',
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_insights(self, df, config, selection):
        """Génère des insights stratégiques"""
        st.markdown('<h3 class="section-header">💡 ANALYSE STRATÉGIQUE</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des indicateurs de performance
        croissance_defense = ((df['Capacite_Defense'].iloc[-1] - df['Capacite_Defense'].iloc[0]) / 
                            df['Capacite_Defense'].iloc[0]) * 100
        
        reduction_temps = ((df['Temps_Deploiement_Jours'].iloc[0] - df['Temps_Deploiement_Jours'].iloc[-1]) / 
                         df['Temps_Deploiement_Jours'].iloc[0]) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 PROGRÈS STRATÉGIQUES")
            st.markdown(f"""
            - **Capacité de défense**: +{croissance_defense:.1f}% depuis 2012
            - **Temps de déploiement**: -{reduction_temps:.1f}% depuis 2012  
            - **Exercices militaires**: {df['Exercices_Militaires'].iloc[-1]:.0f} par an
            - **Préparation opérationnelle**: {df['Readiness_Operative'].iloc[-1]:.0f}%
            """)
            
            if 'Equipements_Modernes' in df.columns:
                st.markdown(f"- **Équipements modernes**: {df['Equipements_Modernes'].iloc[-1]:.0f} unités")
        
        with col2:
            st.markdown("#### 🚀 AXES STRATÉGIQUES")
            
            if config['type'] in ['armee_totale', 'branche']:
                st.markdown("""
                - Modernisation des équipements conventionnels
                - Renforcement des capacités de projection
                - Développement de l'industrie militaire locale
                - Sécurisation des frontières nationales
                """)
            elif config['type'] == 'programme_strategique':
                st.markdown("""
                - Diversification des sources d'approvisionnement
                - Développement des capacités technologiques
                - Renforcement des partenariats stratégiques
                - Formation et entraînement des forces
                """)
        
        # Analyse des priorités
        if config['type'] in ['armee_totale', 'branche', 'programme_strategique']:
            st.markdown("#### 🌟 PRIORITÉS STRATÉGIQUES")
            priorites = config.get('priorites', [])
            if priorites:
                for priorite in priorites:
                    st.markdown(f"- {priorite.replace('_', ' ').title()}")
    
    def create_egyptian_overview(self):
        """Vue d'ensemble des forces armées égyptiennes"""
        st.markdown('<h3 class="section-header">🌍 VUE D\'ENSEMBLE DES FORCES ARMÉES</h3>', 
                   unsafe_allow_html=True)
        
        # Données comparatives des différentes branches
        branches_principales = ["Armée de Terre", "Marine Égyptienne", "Force Aérienne Égyptienne", "Forces de Défense Aérienne"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 👥 EFFECTIFS PAR BRANCHE (2027)")
            effectifs = {
                "Armée de Terre": 310,
                "Marine Égyptienne": 18, 
                "Force Aérienne": 35,
                "Défense Aérienne": 85
            }
            for branche, eff in effectifs.items():
                st.progress(eff/max(effectifs.values()), text=f"{branche}: {eff}K")
        
        with col2:
            st.markdown("#### ⚔️ CAPACITÉS PRINCIPALES")
            capacites = {
                "Défense Aérienne": 85,
                "Forces Blindées": 80,
                "Marine Côtière": 75,
                "Forces Spéciales": 90
            }
            for capacite, niveau in capacites.items():
                st.progress(niveau/100, text=f"{capacite}: {niveau}%")
        
        with col3:
            st.markdown("#### 🚀 ACQUISITIONS MAJEURES")
            acquisitions = {
                "Rafale (France)": 54,
                "FREMM (France)": 1,
                "Gowind (France)": 4,
                "MiG-29M (Russie)": 46,
                "KA-52 (Russie)": 46
            }
            for acquisition, nombre in acquisitions.items():
                st.info(f"{acquisition}: {nombre} unités")
    
    def create_regional_analysis(self):
        """Analyse du rôle régional de l'Égypte"""
        st.markdown('<h3 class="section-header">🌐 RÔLE RÉGIONAL ET PARTENARIATS</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🤝 PARTENAIRES STRATÉGIQUES
            
            **Principaux alliés :**
            - 🇺🇸 **États-Unis** - Coopération militaire historique
            - 🇫🇷 **France** - Transfert de technologie et équipements
            - 🇷🇺 **Russie** - Diversification des sources d'armement
            - 🇸🇦 **Arabie Saoudite** - Coopération régionale
            - 🇦🇪 **Émirats Arabes Unis** - Partenariat stratégique
            
            **Exercices conjoints :**
            - Bright Star (avec les États-Unis)
            - Cleopatra (avec la France)
            - Nile Eagle (exercices régionaux)
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 OBJECTIFS RÉGIONAUX
            
            **Sécurité nationale :**
            - Contrôle du Sinaï et lutte contre le terrorisme
            - Sécurisation des frontières avec la Libye
            - Protection du Nil et des ressources en eau
            - Sécurité de la navigation dans la mer Rouge
            
            **Influence régionale :**
            - Maintien de l'équilibre des forces au Moyen-Orient
            - Leadership dans la Ligue Arabe
            - Médiation dans les conflits régionaux
            - Défense des intérêts arabes communs
            """)
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Génération des données
        df, config = self.generate_defense_data(controls['selection'])
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Vue d'Ensemble", 
            "💰 Budgets & Effectifs", 
            "⚔️ Activités Militaires", 
            "⚡ Capacités", 
            "🚀 Programmes Stratégiques",
            "🌍 Analyse Stratégique"
        ])
        
        with tab1:
            st.markdown(f"## 🌍 Analyse Militaire - {controls['selection']}")
            self.display_key_metrics(df, config)
            self.create_strategic_insights(df, config, controls['selection'])
        
        with tab2:
            self.create_budget_analysis(df, config)
        
        with tab3:
            self.create_military_activities_analysis(df, config)
        
        with tab4:
            self.create_capabilities_analysis(df, config)
        
        with tab5:
            self.create_strategic_programs_analysis(df, config)
            if controls['show_doctrine_analysis']:
                self.create_doctrine_analysis(df, config)
        
        with tab6:
            self.create_egyptian_overview()
            self.create_regional_analysis()
            
            st.markdown("---")
            st.markdown("""
            #### 📋 À PROPOS DE CE DASHBOARD
            
            Ce dashboard présente une analyse stratégique des capacités militaires 
            des Forces Armées Égyptiennes depuis 2012.
            
            **Période d'analyse**: 2012-2027  
            **Indicateurs suivis**: 
            - Budgets de défense et effectifs
            - Exercices et activités militaires
            - Modernisation des équipements
            - Coopération internationale
            - Développement industriel local
            
            **Stratégie de défense**: Basée sur la sécurité multidimensionnelle, 
            la modernisation continue et le maintien de l'équilibre régional.
            
            *Note: Ce dashboard utilise des données estimées et simulées pour l'analyse stratégique.*
            """)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = DefenseEgypteDashboard()
    dashboard.run_dashboard()
