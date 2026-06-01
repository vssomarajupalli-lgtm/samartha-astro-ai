# -*- coding: utf-8 -*-
import math
import json
from datetime import datetime

class SamarthaAstroEngine:
    def __init__(self, json_file_path="raju_canonical_content.json"):
        """
        సమర్థ ఆస్ట్రో కంప్యూటేషనల్ ఇంజన్ - Foolproof Angular Distance Integration
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
        జేసన్ నుండి గ్రహం యొక్క నిజమైన D1 స్థాన బలాన్ని ఫెచ్ చేస్తుంది
        """
        strengths_pool = self.data.get("planetary_strengths", {})
        return strengths_pool.get(planet, 70)  # డేటా లేకపోతే డిఫాల్ట్ 70

    def get_varga_strength(self, planet, varga_chart):
        """
        నిర్దిష్ట వర్గ చక్రంలో (D9, D10, D4) ఆ గ్రహం యొక్క నిజమైన బలాన్ని ఇస్తుంది
        """
        varga_pool = self.data.get("varga_strengths", {})
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
        planet_positions = self.data.get("planet_positions", {})
        current_house = planet_positions.get(karaka, -1)
        return current_house == bhava_idx

    def is_vargottama(self, planet):
        """
        ग्रहం వర్గోత్తమ స్థితిని చెక్ చేస్తుంది
        """
        vargottama_list = self.data.get("vargottama_planets", [])
        return planet in vargottama_list

    def is_pushkara(self, planet):
        """
        ग्रहం పుష్కర నవాంశలో ఉందో లేదో గుర్తిస్తుంది
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
        షార్టెస్ట్ యాంగ్యులర్ డిస్టెన్స్ (Shortest Angular Distance) అల్గారిథమ్ - 360° బౌండరీ బగ్ ఫిక్స్డ్
        """
        if natal_moon_degree is None:
            natal_moon_degree = self.data.get("natal_moon_degree", 280.0)
        if transit_saturn_degree is None:
            transit_saturn_degree = self.data.get("transit_saturn_degree", 282.5)

        lambda_M = natal_moon_degree
        
        # 360 డిగ్రీల వృత్తంలో రెండు బిందువుల మధ్య ఉండే షార్టెస్ట్ కోణీయ దూరాన్ని కనుగొనడం
        diff = (transit_saturn_degree - lambda_M) % 360
        if diff > 180:
            diff -= 360
        abs_diff = abs(diff)
        
        is_in_sade_sati = False
        intensity = "Normal Gocharam"
        
        # 1. PEAK 9-Pada Intensive Phase: దూరం +/- 15 డిగ్రీల లోపు ఉంటే (9 పాదాల కోర్ జోన్)
        if abs_diff <= 15.0:
            is_in_sade_sati = True
            intensity = "PEAK 9-PADA INTENSIVE PHASE"
        
        # 2. Full 27-Pada Wave Active: దూరం +/- 45 డిగ్రీల లోపు ఉంటే (27 పాదాల పూర్తి తరంగం)
        elif abs_diff <= 45.0:
            is_in_sade_sati = True
            intensity = "Full 27-Pada Wave Active"
            
        else:
            is_in_sade_sati = False
            intensity = "Normal Gocharam"
                
        return {
            "Sade_Sati_Active": is_in_sade_sati,
            "Transit_Intensity_Level": intensity
        }

    def fetch_transit_clock(self):
        """
        డైనమిక్ ఆన్-డిమాండ్ గోచార గేట్వే (System Clock vs Custom Flag)
        """
        if self.check_custom_transit and self.custom_date:
            return datetime.strptime(self.custom_date, "%Y-%m-%d")
        else:
            return datetime.now()