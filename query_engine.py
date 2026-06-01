# -*- coding: utf-8 -*-
import math

class SamarthaQueryEngine:
    def __init__(self, graha_bala_engine):
        self.engine = graha_bala_engine

    def calculate_query_score(self, query_id, bhava_idx, lord_planet, karaka_planet, varga_chart, gender="Male"):
        # డైనమిక్ లార్డ్ రిజల్యూషన్: లీటరల్ స్ట్రింగ్స్ ని అసలైన గ్రహం పేరుగా మార్చడం
        if "Lord" in str(lord_planet):
            lord_planet = self.engine.get_house_lord(bhava_idx)

        if query_id in ["Q13", "Q14", "Q31", "Q32", "Q34"] and karaka_planet in ["Venus", "Jupiter"]:
            karaka_planet = "Venus" if gender == "Male" else "Jupiter"

        bhava_lord_strength = self.engine.get_planet_strength(lord_planet)
        karaka_strength = self.engine.get_planet_strength(karaka_planet)
        
        d9_strength = self.engine.get_varga_strength(lord_planet, "D9")
        specific_varga_strength = self.engine.get_varga_strength(lord_planet, varga_chart)
        vimshopaka_score = self.engine.get_vimshopaka_score(lord_planet)

        # 40:30:30 ఫార్ములా
        layer_1_score = 0.40 * bhava_lord_strength
        layer_2_score = 0.30 * karaka_strength
        layer_3_score = (0.15 * d9_strength) + (0.10 * specific_varga_strength) + (0.05 * vimshopaka_score)
        
        final_score = layer_1_score + layer_2_score + layer_3_score

        if self.engine.is_karaka_in_bhava(karaka_planet, bhava_idx):
            final_score *= 0.90

        if self.engine.is_vargottama(lord_planet) or self.engine.is_pushkara(lord_planet):
            final_score += 5.0

        return int(math.ceil(max(0.0, min(100.0, final_score))))

    def evaluate_all_queries(self, gender="Male"):
        query_matrix = {
            "Q1": {"house": 1, "lord": "Lagna_Lord", "karaka": "Sun", "varga": "D3"},
            "Q2": {"house": 1, "lord": "Lagna_Lord", "karaka": "Sun", "varga": "D3"},
            "Q5": {"house": 2, "lord": "Second_Lord", "karaka": "Jupiter", "varga": "D2"},
            "Q6": {"house": 2, "lord": "Second_Lord", "karaka": "Jupiter", "varga": "D12"},
            "Q14": {"house": 4, "lord": "Fourth_Lord", "karaka": "Mars", "varga": "D4"},
            "Q16": {"house": 4, "lord": "Fourth_Lord", "karaka": "Venus", "varga": "D16"},
            "Q19": {"house": 5, "lord": "Fifth_Lord", "karaka": "Jupiter", "varga": "D7"},
            "Q23": {"house": 5, "lord": "Fifth_Lord", "karaka": "Jupiter", "varga": "D24"},
            "Q26": {"house": 6, "lord": "Sixth_Lord", "karaka": "Saturn", "varga": "D6"},
            "Q31": {"house": 7, "lord": "Seventh_Lord", "karaka": "Venus", "varga": "D9"},
            "Q40": {"house": 7, "lord": "Seventh_Lord", "karaka": "Mercury", "varga": "D10"},
            "Q41": {"house": 8, "lord": "Eighth_Lord", "karaka": "Saturn", "varga": "D8"},
            "Q46": {"house": 9, "lord": "Ninth_Lord", "karaka": "Jupiter", "varga": "D9"},
            "Q50": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D10"},
            "Q51": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D10"},
            "Q53": {"house": 10, "lord": "Tenth_Lord", "karaka": "Mercury", "varga": "D10"},
            "Q67": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D10"},
            "Q68": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D6"},
            "Q72": {"house": 11, "lord": "Eleventh_Lord", "karaka": "Jupiter", "varga": "D11"},
            "Q76": {"house": 12, "lord": "Twelfth_Lord", "karaka": "Rahu", "varga": "D12"},
            "Q83": {"house": 12, "lord": "D60_Lagna_Lord", "karaka": "Ketu", "varga": "D60"},
            "Q85": {"house": 8, "lord": "D30_Lord", "karaka": "Rahu", "varga": "D30"}
        }

        results = {}
        for q_id, params in query_matrix.items():
            results[q_id] = self.calculate_query_score(
                query_id=q_id,
                bhava_idx=params["house"],
                lord_planet=params["lord"],
                karaka_planet=params["karaka"],
                varga_chart=params["varga"],
                gender=gender
            )
        return results