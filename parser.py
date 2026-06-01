import math
import json
from datetime import datetime

class SamarthaAstroEngine:
    def __init__(self, json_file_path="raju_canonical_content.json"):
        """
        సమర్థ ఆస్ట్రో కంప్యూటేషనల్ ఇంజన్ - Real JSON Data Integration
        """
        self.check_custom_transit = False
        self.custom_date = None
        
        # 1. రియల్ జేసన్ ఫైల్ ని లోడ్ చేయడం
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"⚠️ జేసన్ ఫైల్ లోడ్ చేయడంలో లోపం: {e}")
            self.data = {}

    def get_planet_strength(self, planet):
        """
        జేసన్ నుండి గ్రహం యొక్క నిజమైన బేస్ బలాన్ని (D1 Graph Bala) ఫెచ్ చేస్తుంది
        """
        # జేసన్ లో 'planetary_strengths' -> 'Jupiter' లాంటి ఫార్మాట్ ఉంటే రీడ్ చేస్తుంది
        strengths_pool = self.data.get("planetary_strengths", {})
        return strengths_pool.get(planet, 70)  # డేటా లేకపోతే డిఫాల్ట్ 70

    def get_varga_strength(self, planet, varga_chart):
        """
        నిర్దిష్ట వర్గ చక్రంలో (D9, D10, D4) ఆ గ్రహం యొక్క నిజమైన బలాన్ని ఇస్తుంది
        """
        varga_pool = self.data.get("varga_strengths", {})  # e.g., {"D9": {"Jupiter": 85}}
        chart_pool = varga_pool.get(varga_chart, {})
        return chart_pool.get(planet, 75)  # డిఫాల్ట్ 75

    def get_vimshopaka_score(self, planet):
        """
        16 వర్గాల మొత్తం వింశోపాక పూల్ స్కోరును జేసన్ నుండి తీస్తుంది
        """
        vimshopaka_pool = self.data.get("vimshopaka_scores", {})
        return vimshopaka_pool.get(planet, 80)  # డిఫాల్ట్ 80

    def is_karaka_in_bhava(self, karaka, bhava_idx):
        """
        Karaka Bhava Nashaya ఫిల్టర్ - కారకుడు ఆ భావంలోనే ఉన్నాడా అనేది జేసన్ నుండి చెక్ చేస్తుంది
        """
        planet_positions = self.data.get("planet_positions", {})  # {"Jupiter": 5}
        current_house = planet_positions.get(karaka, -1)
        return current_house == bhava_idx

    def is_vargottama(self, planet):
        """
        గ్రహం వర్గోత్తమ స్థితిని (D1 రాశి == D9 రాశి) చెక్ చేస్తుంది
        """
        vargottama_list = self.data.get("vargottama_planets", [])
        return planet in vargottama_list

    def is_pushkara(self, planet):
        """
        గ్రహం పుష్కర నవాంశలో ఉందో లేదో గుర్తిస్తుంది
        """
        pushkara_list = self.data.get("pushkara_planets", [])
        return planet in pushkara_list

    def calculate_graha_bala(self, house_score, nak_score, shad_score, varga_score, vargottama_score, aspect_score):
        """
        కోర్ గ్రహబల లెక్కింపు - 58% భావ స్థాన బలం ఫార్ములా
        """
        base_str = (0.58 * house_score) + (0.10 * nak_score) + (0.08 * shad_score) + \
                   (0.08 * varga_score) + (0.08 * vargottama_score) + (0.08 * aspect_score)
        return int(math.ceil(min(100.0, base_str)))

    def get_vimshottari_triad(self):
        """
        దశా టైమ్‌లైన్ ఎక్స్‌పాన్షన్ (Mahadasha -> Antardasha -> Pratyantardasha)
        """
        return {
            "Mahadasha_Lord": self.data.get("current_mahadasha", "Jupiter"),
            "Antardasha_Lord": self.data.get("current_antardasha", "Saturn"),
            "Pratyantardasha_Lord": self.data.get("current_pratyantardasha", "Mercury")
        }

    def calculate_pada_sade_sati(self, natal_moon_degree=None, transit_saturn_degree=None):
        """
        నక్షత్ర పాద ఏలినాటి శని (Pada-Centric Rolling Transit Engine)
        """
        # జేసన్ లో ఉన్న రియల్ చంద్రుడి డిగ్రీని ఆటోమేటిక్ గా పట్టుకోవడం
        if natal_moon_degree is None:
            natal_moon_degree = self.data.get("natal_moon_degree", 280.0)
        if transit_saturn_degree is None:
            transit_saturn_degree = self.data.get("transit_saturn_degree", 282.5)

        lambda_M = natal_moon_degree
        peak_min, peak_max = (lambda_M - 15.0) % 360, (lambda_M + 15.0) % 360
        wave_min, wave_max = (lambda_M - 45.0) % 360, (lambda_M + 45.0) % 360
        
        is_in_sade_sati = False
        intensity = "Normal Gocharam"
        
        if wave_min <= transit_saturn_degree <= wave_max:
            is_in_sade_sati = True
            intensity = "Full 27-Pada Wave Active"
            if peak_min <= transit_saturn_degree <= peak_max:
                intensity = "PEAK 9-PADA INTENSIVE PHASE"
                
        return {
            "Sade_Sati_Active": is_in_sade_sati,
            "Transit_Intensity_Level": intensity
        }