# dashboard_armee_egypte_approfondi.py
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
    page_title="Analyse Approfondie - Armée Égyptienne",
    page_icon="🇪🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé amélioré
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #CE1126, #FECB00, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        color: #000000;
        border-bottom: 3px solid #CE1126;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .sub-section {
        color: #CE1126;
        border-left: 4px solid #FECB00;
        padding-left: 1rem;
        margin-top: 1.5rem;
        font-size: 1.4rem;
        font-weight: 600;
    }
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #CE1126;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #CE1126;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    .egyptian-flag {
        font-size: 1.2rem;
        font-weight: bold;
        background: linear-gradient(45deg, #CE1126, #FECB00, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem;
        border-radius: 8px;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .comparison-badge {
        background: #CE1126;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

class ArmeeEgypteAnalyseApprofondie:
    def __init__(self):
        # Données détaillées de l'armée égyptienne
        self.donnees_armee = self.charger_donnees_detaillees()
        self.donnees_regionales = self.charger_donnees_regionales()
        self.donnees_modernisation = self.charger_donnees_modernisation()
        
    def charger_donnees_detaillees(self):
        """Charge des données détaillées sur l'armée égyptienne"""
        # Structure organisationnelle
        structure = {
            "Commandements": ["Commandement Nord", "Commandement Centre", "Commandement Sud", 
                            "Commandement Ouest", "Commandement Est", "Commandement du Sinaï"],
            "Divisions_Blindees": [3, 2, 1, 1, 2, 1],
            "Divisions_Mecanisees": [2, 2, 1, 1, 1, 1],
            "Divisions_Infanterie": [4, 3, 2, 2, 3, 2],
            "Forces_Speciales": [2, 1, 1, 1, 1, 1]
        }
        
        # Équipements par type
        equipements = {
            "Type": ["Chars Principaux", "Véhicules Blindés", "Artillerie Tractée", 
                    "Artillerie Automotrice", "Lance-roquettes", "Systèmes ATGM"],
            "Quantite_2024": [3760, 12000, 1200, 850, 600, 3000],
            "Quantite_2012": [3400, 9500, 1100, 650, 450, 2000],
            "Taux_Modernite": [35, 40, 25, 45, 30, 60]
        }
        
        # Capacités opérationnelles
        capacites = pd.DataFrame({
            "Annee": list(range(2012, 2025)),
            "Readiness_Operative": [70, 72, 74, 76, 78, 80, 82, 84, 85, 86, 87, 88, 89],
            "Temps_Deploiement_Jours": [72, 70, 68, 65, 62, 58, 55, 52, 50, 48, 47, 46, 45],
            "Exercices_Combines": [15, 16, 18, 20, 22, 25, 28, 30, 32, 34, 36, 38, 40],
            "Entrainement_Heures_An": [800, 820, 850, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060]
        })
        
        return {
            "structure": pd.DataFrame(structure),
            "equipements": pd.DataFrame(equipements),
            "capacites": capacites
        }
    
    def charger_donnees_regionales(self):
        """Charge des données comparatives régionales"""
        pays = ["Égypte", "Israël", "Turquie", "Arabie Saoudite", "Iran", "Algérie"]
        
        donnees = {
            "Pays": pays,
            "Effectifs_Actifs_K": [462, 169, 355, 227, 610, 130],
            "Reservistes_K": [491, 465, 380, 25, 350, 150],
            "Chars_Principaux": [3760, 1500, 3200, 1065, 2300, 1300],
            "Veh_Blindes": [12000, 10000, 11000, 8500, 15000, 6000],
            "Artillerie": [2050, 750, 3000, 1250, 3500, 1000],
            "Budget_Defense_MdUSD": [8800, 24000, 15000, 57000, 10000, 9500],
            "Depense_Par_Soldat_KUSD": [19.0, 142.0, 42.3, 251.1, 16.4, 73.1]
        }
        
        return pd.DataFrame(donnees)
    
    def charger_donnees_modernisation(self):
        """Charge des données sur la modernisation"""
        programmes = [
            {"Programme": "Modernisation T-55/T-62", "Budget_MdUSD": 800, "Debut": 2015, "Fin": 2025, "Statut": "En cours"},
            {"Programme": "Acquisition T-90MS", "Budget_MdUSD": 1200, "Debut": 2020, "Fin": 2027, "Statut": "En cours"},
            {"Programme": "Véhicules 8x8 EIFV", "Budget_MdUSD": 500, "Debut": 2018, "Fin": 2024, "Statut": "Terminé"},
            {"Programme": "Systèmes ATGM modernes", "Budget_MdUSD": 300, "Debut": 2016, "Fin": 2022, "Statut": "Terminé"},
            {"Programme": "Artillerie automotrice", "Budget_MdUSD": 400, "Debut": 2019, "Fin": 2026, "Statut": "En cours"},
            {"Programme": "Systèmes C4ISR", "Budget_MdUSD": 600, "Debut": 2017, "Fin": 2025, "Statut": "En cours"}
        ]
        
        return pd.DataFrame(programmes)
    
    def afficher_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🇪🇬 ANALYSE APPROFONDIE - ARMÉE DE TERRE ÉGYPTIENNE</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="egyptian-flag">🏜️ FORCE TERRESTRE - COMMANDEMENT STRATÉGIQUE 🏜️</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Analyse détaillée des capacités, organisation et modernisation (2012-2024)**")
    
    def creer_sidebar_avancee(self):
        """Crée une sidebar avancée avec plus d'options"""
        st.sidebar.markdown("## 🎯 ANALYSE STRATÉGIQUE")
        
        niveau_analyse = st.sidebar.selectbox(
            "Niveau d'analyse:",
            ["Vue d'ensemble", "Structure organisationnelle", "Capacités opérationnelles", 
             "Modernisation", "Comparaison régionale", "Projections futures"]
        )
        
        st.sidebar.markdown("## 📊 OPTIONS D'ANALYSE")
        
        afficher_details = st.sidebar.checkbox("Afficher les données détaillées", True)
        comparer_region = st.sidebar.checkbox("Comparaison régionale", True)
        show_projections = st.sidebar.checkbox("Projections 2025-2030", False)
        mode_expert = st.sidebar.checkbox("Mode expert (plus de métriques)", False)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 FILTRES TEMPORELS")
        annee_debut, annee_fin = st.sidebar.slider(
            "Période d'analyse", 
            2012, 2024, (2012, 2024)
        )
        
        return {
            'niveau_analyse': niveau_analyse,
            'afficher_details': afficher_details,
            'comparer_region': comparer_region,
            'show_projections': show_projections,
            'mode_expert': mode_expert,
            'periode': (annee_debut, annee_fin)
        }
    
    def analyser_structure_organisationnelle(self):
        """Analyse détaillée de la structure organisationnelle"""
        st.markdown('<h3 class="section-header">🏛️ STRUCTURE ORGANISATIONNELLE</h3>', 
                   unsafe_allow_html=True)
        
        df_structure = self.donnees_armee["structure"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Carte thermique de la distribution des forces
            fig = px.imshow(
                df_structure[['Divisions_Blindees', 'Divisions_Mecanisees', 'Divisions_Infanterie', 'Forces_Speciales']].T,
                labels=dict(x="Commandements", y="Type de Division", color="Nombre"),
                x=df_structure['Commandements'],
                y=['Divisions Blindées', 'Divisions Mécanisées', 'Divisions Infanterie', 'Forces Spéciales'],
                title="Distribution des Forces par Commandement",
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('<div class="sub-section">📊 Distribution Totale des Divisions</div>', unsafe_allow_html=True)
            total_blindees = df_structure['Divisions_Blindees'].sum()
            total_mecanisees = df_structure['Divisions_Mecanisees'].sum()
            total_infanterie = df_structure['Divisions_Infanterie'].sum()
            total_speciales = df_structure['Forces_Speciales'].sum()
            
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Blindées", total_blindees)
            col_b.metric("Mécanisées", total_mecanisees)
            col_c.metric("Infanterie", total_infanterie)
            col_d.metric("Spéciales", total_speciales)
        
        with col2:
            # Graphique en radar des capacités par commandement
            fig = go.Figure()
            
            for idx, row in df_structure.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[row['Divisions_Blindees'], row['Divisions_Mecanisees'], 
                       row['Divisions_Infanterie'], row['Forces_Speciales']],
                    theta=['Blindées', 'Mécanisées', 'Infanterie', 'Spéciales'],
                    fill='toself',
                    name=row['Commandements']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=True,
                title="Profil des Commandements (Capacités Relatives)",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse stratégique des commandements
        st.markdown('<div class="sub-section">🎯 ANALYSE STRATÉGIQUE DES COMMANDEMENTS</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown("**Commandement Nord (Le Caire/Alexandrie)**")
            st.markdown("""
            • Protection centres urbains  
            • Réserve stratégique  
            • Contrôle Delta du Nil  
            • 3 divisions blindées
            """)
        
        with cols[1]:
            st.markdown("**Commandement du Sinaï**")
            st.markdown("""
            • Opérations anti-terroristes  
            • Sécurisation frontières  
            • Coordination avec police  
            • 1 division blindée + forces spéciales
            """)
        
        with cols[2]:
            st.markdown("**Commandement Ouest (Frontière Libye)**")
            st.markdown("""
            • Surveillance frontière  
            • Contrôle immigration  
            • Prévention trafics  
            • 1 division mécanisée
            """)
    
    def analyser_capacites_operationnelles(self, periode):
        """Analyse détaillée des capacités opérationnelles"""
        st.markdown('<h3 class="section-header">⚡ CAPACITÉS OPÉRATIONNELLES</h3>', 
                   unsafe_allow_html=True)
        
        df_capacites = self.donnees_armee["capacites"]
        df_capacites = df_capacites[(df_capacites['Annee'] >= periode[0]) & (df_capacites['Annee'] <= periode[1])]
        
        # Métriques clés
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            croissance_readiness = ((df_capacites['Readiness_Operative'].iloc[-1] - 
                                   df_capacites['Readiness_Operative'].iloc[0]) / 
                                   df_capacites['Readiness_Operative'].iloc[0]) * 100
            st.metric(
                "Préparation Opérationnelle",
                f"{df_capacites['Readiness_Operative'].iloc[-1]:.1f}%",
                f"{croissance_readiness:+.1f}%",
                delta_color="normal"
            )
        
        with col2:
            reduction_temps = ((df_capacites['Temps_Deploiement_Jours'].iloc[0] - 
                              df_capacites['Temps_Deploiement_Jours'].iloc[-1]) / 
                             df_capacites['Temps_Deploiement_Jours'].iloc[0]) * 100
            st.metric(
                "Temps de Déploiement",
                f"{df_capacites['Temps_Deploiement_Jours'].iloc[-1]:.0f} jours",
                f"{reduction_temps:+.1f}%",
                delta_color="inverse"
            )
        
        with col3:
            croissance_exercices = ((df_capacites['Exercices_Combines'].iloc[-1] - 
                                   df_capacites['Exercices_Combines'].iloc[0]) / 
                                   df_capacites['Exercices_Combines'].iloc[0]) * 100
            st.metric(
                "Exercices Combinés",
                f"{df_capacites['Exercices_Combines'].iloc[-1]:.0f}",
                f"{croissance_exercices:+.1f}%"
            )
        
        with col4:
            croissance_entrainement = ((df_capacites['Entrainement_Heures_An'].iloc[-1] - 
                                      df_capacites['Entrainement_Heures_An'].iloc[0]) / 
                                     df_capacites['Entrainement_Heures_An'].iloc[0]) * 100
            st.metric(
                "Heures d'Entraînement",
                f"{df_capacites['Entrainement_Heures_An'].iloc[-1]:.0f}h",
                f"{croissance_entrainement:+.1f}%"
            )
        
        # Graphiques détaillés
        col1, col2 = st.columns(2)
        
        with col1:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=df_capacites['Annee'], y=df_capacites['Readiness_Operative'],
                          name="Préparation Opérationnelle", line=dict(color='#CE1126', width=3)),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=df_capacites['Annee'], y=df_capacites['Temps_Deploiement_Jours'],
                          name="Temps Déploiement (jours)", line=dict(color='#000000', width=3)),
                secondary_y=True,
            )
            
            fig.update_layout(
                title="Évolution Préparation vs Temps Réponse",
                xaxis_title="Année",
                height=400
            )
            
            fig.update_yaxes(title_text="Préparation (%)", secondary_y=False)
            fig.update_yaxes(title_text="Jours", secondary_y=True, autorange="reversed")
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_capacites['Annee'], 
                y=df_capacites['Exercices_Combines'],
                mode='lines+markers',
                name='Exercices Combinés',
                line=dict(color='#FECB00', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Bar(
                x=df_capacites['Annee'], 
                y=df_capacites['Entrainement_Heures_An'],
                name='Heures Entraînement',
                marker_color='#0066CC',
                opacity=0.6
            ))
            
            fig.update_layout(
                title="Activités d'Entraînement et Exercices",
                xaxis_title="Année",
                yaxis_title="Nombre/Heures",
                barmode='overlay',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des tendances
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown("### 📈 TENDANCES OPÉRATIONNELLES")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Améliorations notables:**")
            st.markdown("""
            • ⬆️ Préparation opérationnelle: +27% depuis 2012  
            • ⬇️ Temps de réponse: -37.5% depuis 2012  
            • ⬆️ Exercices combinés: +166% depuis 2012  
            • ⬆️ Formation: +32.5% d'heures d'entraînement  
            """)
        
        with col2:
            st.markdown("**Facteurs clés de succès:**")
            st.markdown("""
            • Modernisation des équipements  
            • Augmentation des exercices internationaux  
            • Amélioration de la maintenance  
            • Formation spécialisée accrue  
            • Systèmes C4ISR modernes  
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def analyser_equipements_modernisation(self):
        """Analyse détaillée des équipements et modernisation"""
        st.markdown('<h3 class="section-header">🛡️ ÉQUIPEMENTS ET MODERNISATION</h3>', 
                   unsafe_allow_html=True)
        
        df_equipements = self.donnees_armee["equipements"]
        df_programmes = self.donnees_modernisation
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution des équipements
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='2012',
                x=df_equipements['Type'],
                y=df_equipements['Quantite_2012'],
                marker_color='rgba(206, 17, 38, 0.6)'
            ))
            
            fig.add_trace(go.Bar(
                name='2024',
                x=df_equipements['Type'],
                y=df_equipements['Quantite_2024'],
                marker_color='rgba(206, 17, 38, 1)'
            ))
            
            fig.update_layout(
                title="Évolution du Parc d'Équipements (2012 vs 2024)",
                xaxis_title="Type d'équipement",
                yaxis_title="Quantité",
                barmode='group',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Taux de modernité
            fig = px.bar(df_equipements, x='Type', y='Taux_Modernite',
                        title="Taux de Modernité du Parc d'Équipements (%)",
                        color='Taux_Modernite',
                        color_continuous_scale='Reds',
                        labels={'Taux_Modernite': '% Modernité'})
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Métriques de modernité
            modernite_moyenne = df_equipements['Taux_Modernite'].mean()
            st.metric("Modernité Moyenne du Parc", f"{modernite_moyenne:.1f}%")
        
        # Programmes de modernisation
        st.markdown('<div class="sub-section">🚀 PROGRAMMES DE MODERNISATION</div>', unsafe_allow_html=True)
        
        # Table interactive
        st.dataframe(
            df_programmes.style
            .bar(subset=['Budget_MdUSD'], color='#CE1126', vmin=0)
            .apply(lambda x: ['background: #d4edda' if v == 'Terminé' 
                            else 'background: #fff3cd' if v == 'En cours' 
                            else '' for v in x], subset=['Statut']),
            use_container_width=True,
            height=300
        )
        
        # Analyse des programmes
        total_budget = df_programmes['Budget_MdUSD'].sum()
        programmes_en_cours = df_programmes[df_programmes['Statut'] == 'En cours'].shape[0]
        programmes_termines = df_programmes[df_programmes['Statut'] == 'Terminé'].shape[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Budget Total Modernisation", f"{total_budget:,.0f} M$")
        col2.metric("Programmes en Cours", programmes_en_cours)
        col3.metric("Programmes Terminés", programmes_termines)
        
        # Détail par type d'équipement
        st.markdown('<div class="sub-section">🔧 ANALYSE PAR TYPE D\'ÉQUIPEMENT</div>', unsafe_allow_html=True)
        
        cols = st.columns(len(df_equipements))
        for idx, row in df_equipements.iterrows():
            with cols[idx]:
                avec cols[idx]:
                    croissance = ((row['Quantite_2024'] - row['Quantite_2012']) / row['Quantite_2012']) * 100
                    
                    st.markdown(f"**{row['Type']}**")
                    st.metric("2024", f"{row['Quantite_2024']:,}")
                    st.metric("Croissance", f"{croissance:+.1f}%")
                    st.progress(row['Taux_Modernite'] / 100, 
                               text=f"Modernité: {row['Taux_Modernite']}%")
    
    def analyser_comparaison_regionale(self):
        """Analyse comparative avec les armées régionales"""
        st.markdown('<h3 class="section-header">🌍 COMPARAISON RÉGIONALE</h3>', 
                   unsafe_allow_html=True)
        
        df_region = self.donnees_regionales
        
        # Sélection des indicateurs à comparer
        indicateurs = st.multiselect(
            "Sélectionnez les indicateurs à comparer:",
            ["Effectifs_Actifs_K", "Chars_Principaux", "Veh_Blindes", 
             "Artillerie", "Budget_Defense_MdUSD", "Depense_Par_Soldat_KUSD"],
            default=["Effectifs_Actifs_K", "Chars_Principaux", "Budget_Defense_MdUSD"]
        )
        
        if indicateurs:
            # Normalisation pour le radar chart
            df_normalized = df_region.copy()
            for col in indicateurs:
                df_normalized[col] = df_normalized[col] / df_normalized[col].max() * 100
            
            # Graphique radar comparatif
            fig = go.Figure()
            
            for idx, row in df_normalized.iterrows():
                values = [row[col] for col in indicateurs]
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=indicateurs,
                    fill='toself',
                    name=row['Pays'],
                    opacity=0.7
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Comparaison Régionale (Normalisée)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Table de comparaison détaillée
            st.markdown('<div class="sub-section">📋 DONNÉES COMPARATIVES DÉTAILLÉES</div>', unsafe_allow_html=True)
            
            # Calcul des rangs
            df_comparison = df_region.copy()
            for col in indicateurs:
                df_comparison[f'Rang_{col}'] = df_comparison[col].rank(ascending=False, method='dense').astype(int)
            
            # Affichage avec mise en forme
            st.dataframe(
                df_comparison.style
                .highlight_max(subset=indicateurs, color='#d4edda')
                .highlight_min(subset=indicateurs, color='#f8d7da')
                .apply(lambda x: ['font-weight: bold' if v == 'Égypte' else '' for v in x], subset=['Pays']),
                use_container_width=True,
                height=400
            )
            
            # Analyse des positions relatives
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 POSITIONNEMENT STRATÉGIQUE DE L'ÉGYPTE")
            
            position_egypte = {}
            for col in indicateurs:
                valeur = df_region[df_region['Pays'] == 'Égypte'][col].values[0]
                rang = df_comparison[df_comparison['Pays'] == 'Égypte'][f'Rang_{col}'].values[0]
                total = len(df_region)
                position_egypte[col] = {"valeur": valeur, "rang": rang, "total": total}
            
            cols = st.columns(len(indicateurs))
            for idx, col in enumerate(indicateurs):
                avec cols[idx]:
                    st.metric(
                        label=col.replace('_', ' '),
                        value=f"{position_egypte[col]['valeur']:,.0f}",
                        delta=f"Rang {position_egypte[col]['rang']}/{position_egypte[col]['total']}"
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def analyser_projection_futures(self):
        """Projections des capacités futures"""
        st.markdown('<h3 class="section-header">🔮 PROJECTIONS 2025-2030</h3>', 
                   unsafe_allow_html=True)
        
        # Scénarios de projection
        scenarios = {
            "Scenario_Conservative": [89, 87, 85, 84, 82, 80],
            "Scenario_Moderne": [89, 88, 87, 86, 85, 84],
            "Scenario_Ambitieux": [89, 90, 91, 92, 93, 94]
        }
        
        annees_projection = list(range(2025, 2031))
        
        # Graphique des projections
        fig = go.Figure()
        
        for scenario, valeurs in scenarios.items():
            nom_scenario = scenario.replace('_', ' ').replace('Scenario ', '')
            fig.add_trace(go.Scatter(
                x=annees_projection,
                y=valeurs,
                mode='lines+markers',
                name=nom_scenario,
                line=dict(width=2, dash='dot' if 'Conservative' in scenario else 'solid')
            ))
        
        # Ajouter les données historiques
        df_capacites = self.donnees_armee["capacites"]
        fig.add_trace(go.Scatter(
            x=df_capacites['Annee'],
            y=df_capacites['Readiness_Operative'],
            mode='lines+markers',
            name='Données Historiques',
            line=dict(color='#000000', width=3)
        ))
        
        fig.update_layout(
            title="Projections de Préparation Opérationnelle (2025-2030)",
            xaxis_title="Année",
            yaxis_title="Préparation Opérationnelle (%)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des scénarios
        st.markdown('<div class="sub-section">📊 DÉTAIL DES SCÉNARIOS</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        
        scenarios_detail = {
            "Conservative": {
                "description": "Maintien des capacités actuelles",
                "investissement": "+5% budget",
                "modernisation": "Rénovation limitée",
                "risques": "Décalage technologique"
            },
            "Moderne": {
                "description": "Modernisation progressive",
                "investissement": "+15% budget",
                "modernisation": "Renouvellement partiel",
                "risques": "Dépendance extérieure"
            },
            "Ambitieux": {
                "description": "Transformation numérique",
                "investissement": "+25% budget",
                "modernisation": "Saut technologique",
                "risques": "Problèmes d'intégration"
            }
        }
        
        for idx, (scenario, details) in enumerate(scenarios_detail.items()):
            avec cols[idx]:
                st.markdown(f"### {scenario}")
                st.markdown(f"**{details['description']}**")
                st.markdown(f"• Investissement: {details['investissement']}")
                st.markdown(f"• Modernisation: {details['modernisation']}")
                st.markdown(f"• Risques: {details['risques']}")
                
                # Bouton pour voir plus de détails
                with st.expander("Voir les hypothèses"):
                    st.markdown(f"""
                    **Hypothèses clés:**
                    - Taux de croissance économique: {2+idx}%
                    - Coopération internationale: {'limitée' if idx==0 else 'modérée' if idx==1 else 'intensive'}
                    - Développement industriel local: {'faible' if idx==0 else 'moyen' if idx==1 else 'fort'}
                    - Intégration numérique: {'progressive' if idx<2 else 'accélérée'}
                    """)
    
    def creer_tableau_bord_complet(self):
        """Crée un tableau de bord complet avec toutes les analyses"""
        # Sidebar
        controls = self.creer_sidebar_avancee()
        
        # Header
        self.afficher_header()
        
        # Navigation basée sur la sélection
        if controls['niveau_analyse'] == "Vue d'ensemble":
            self.afficher_vue_ensemble(controls)
        elif controls['niveau_analyse'] == "Structure organisationnelle":
            self.analyser_structure_organisationnelle()
        elif controls['niveau_analyse'] == "Capacités opérationnelles":
            self.analyser_capacites_operationnelles(controls['periode'])
        elif controls['niveau_analyse'] == "Modernisation":
            self.analyser_equipements_modernisation()
        elif controls['niveau_analyse'] == "Comparaison régionale":
            self.analyser_comparaison_regionale()
        elif controls['niveau_analyse'] == "Projections futures":
            self.analyser_projection_futures()
        
        # Affichage des données détaillées si demandé
        if controls['afficher_details']:
            self.afficher_donnees_detaillees()
        
        # Mode expert
        if controls['mode_expert']:
            self.afficher_mode_expert()
    
    def afficher_vue_ensemble(self, controls):
        """Affiche une vue d'ensemble complète"""
        st.markdown('<h3 class="section-header">📊 VUE D\'ENSEMBLE STRATÉGIQUE</h3>', 
                   unsafe_allow_html=True)
        
        # Métriques synthétiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Effectifs Totaux", "462,000", "+5.5% vs 2012")
        
        with col2:
            st.metric("Chars Principaux", "3,760", "+10.6% vs 2012")
        
        with col3:
            st.metric("Budget 2024", "8.8 Md$", "+110% vs 2012")
        
        with col4:
            st.metric("Préparation Opé", "89%", "+27% vs 2012")
        
        # Vue synthétique
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("### 🏆 POINTS FORTS")
            st.markdown("""
            • **Quantité d'équipements**: Parc blindé conséquent  
            • **Expérience opérationnelle**: Opérations réelles au Sinaï  
            • **Infrastructure**: Bases bien positionnées  
            • **Formation**: Programme d'entraînement intensif  
            • **Coopération**: Partenariats internationaux solides  
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("### ⚠️ DÉFIS")
            st.markdown("""
            • **Modernisation**: Parc vieillissant  
            • **Interopérabilité**: Systèmes hétérogènes  
            • **Maintenance**: Coûts élevés  
            • **Logistique**: Dépendance aux importations  
            • **Doctrine**: Adaptation aux guerres hybrides  
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Graphique de synthèse
        self.analyser_capacites_operationnelles(controls['periode'])
        
        if controls['comparer_region']:
            st.markdown('<div class="sub-section">🌍 CONTEXTE RÉGIONAL</div>', unsafe_allow_html=True)
            self.analyser_comparaison_regionale()
    
    def afficher_donnees_detaillees(self):
        """Affiche les données détaillées en format tabulaire"""
        with st.expander("📁 DONNÉES DÉTAILLÉES (Cliquez pour développer)"):
            tab1, tab2, tab3 = st.tabs(["Structure", "Équipements", "Capacités"])
            
            with tab1:
                st.dataframe(self.donnees_armee["structure"], use_container_width=True)
            
            with tab2:
                st.dataframe(self.donnees_armee["equipements"], use_container_width=True)
            
            with tab3:
                st.dataframe(self.donnees_armee["capacites"], use_container_width=True)
    
    def afficher_mode_expert(self):
        """Affiche des analyses expert supplémentaires"""
        st.markdown('<div class="section-header">🔬 MODE EXPERT - ANALYSES AVANCÉES</div>', 
                   unsafe_allow_html=True)
        
        # Analyse de corrélation
        st.markdown('<div class="sub-section">📈 ANALYSE DE CORRÉLATION</div>', unsafe_allow_html=True)
        
        df_capacites = self.donnees_armee["capacites"]
        correlations = df_capacites.corr()
        
        fig = px.imshow(correlations,
                       text_auto='.2f',
                       color_continuous_scale='RdBu_r',
                       title="Matrice de Corrélation entre Indicateurs")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des tendances temporelles
        st.markdown('<div class="sub-section">⏰ ANALYSE DES TENDANCES TEMPORELLES</div>', unsafe_allow_html=True)
        
        # Calcul des taux de croissance annuels
        df_capacites['Croissance_Readiness'] = df_capacites['Readiness_Operative'].pct_change() * 100
        df_capacites['Croissance_Exercices'] = df_capacites['Exercises_Combines'].pct_change() * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_capacites['Annee'][1:],
            y=df_capacites['Croissance_Readiness'][1:],
            mode='lines+markers',
            name='Croissance Préparation (%)',
            line=dict(color='#CE1126', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_capacites['Annee'][1:],
            y=df_capacites['Croissance_Exercices'][1:],
            mode='lines+markers',
            name='Croissance Exercices (%)',
            line=dict(color='#FECB00', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Taux de Croissance Annuels (%)",
            xaxis_title="Année",
            yaxis=dict(title='Croissance Préparation (%)', side='left'),
            yaxis2=dict(title='Croissance Exercices (%)', side='right', overlaying='y'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse SWOT approfondie
        st.markdown('<div class="sub-section">🎯 ANALYSE SWOT APPROFONDIE</div>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        swot_data = {
            "Forces": [
                "Effectifs nombreux et expérimentés",
                "Parc blindé important",
                "Position géostratégique",
                "Expérience opérationnelle réelle",
                "Coopération internationale établie"
            ],
            "Faiblesses": [
                "Dépendance aux importations",
                "Modernisation inégale",
                "Interopérabilité limitée",
                "Coûts de maintenance élevés",
                "Vieillissement du parc"
            ],
            "Opportunités": [
                "Coopération renforcée avec les Émirats",
                "Développement industriel local",
                "Nouvelles technologies (drones, cyber)",
                "Exercices internationaux accrus",
                "Formation spécialisée"
            ],
            "Menaces": [
                "Instabilité régionale",
                "Concurrence technologique",
                "Sanctions potentielles",
                "Tensions frontalières",
                "Évolution des doctrines militaires"
            ]
        }
        
        for idx, (categorie, elements) in enumerate(swot_data.items()):
            avec cols[idx]:
                st.markdown(f"### {categorie.upper()}")
                for element in elements:
                    st.markdown(f"• {element}")

    def run(self):
        """Exécute le dashboard complet"""
        self.creer_tableau_bord_complet()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = ArmeeEgypteAnalyseApprofondie()
    dashboard.run()
