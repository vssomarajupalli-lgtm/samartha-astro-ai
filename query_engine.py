import math

class SamarthaQueryEngine:
    def __init__(self, graha_bala_engine):
        """
        సమర్థ క్వెరీ ఇంజన్ - 40:30:30 వెయిటేజీ ఫార్ములా అమలు
        """
        self.engine = graha_bala_engine

    def calculate_query_score(self, query_id, bhava_idx, lord_planet, karaka_planet, varga_chart, gender="Male"):
        """
        ప్రతి సింగిల్-ఫోకస్ ప్రశ్నకు 100 మార్కులకు గాను స్కోరును లెక్కిస్తుంది
        """
        # జెండర్ ఆధారిత కారకత్వ స్విచ్ (వివాహ ప్రశ్నల కోసం)
        if query_id in ["Q13", "Q14", "Q31", "Q32", "Q34"] and karaka_planet in ["Venus", "Jupiter"]:
            karaka_planet = "Venus" if gender == "Male" else "Jupiter"

        # కోర్ బలాలు ఫెచ్ చేయడం
        bhava_lord_strength = self.engine.get_planet_strength(lord_planet)
        karaka_strength = self.engine.get_planet_strength(karaka_planet)
        
        # వర్గ చక్రాల బలాలు
        d9_strength = self.engine.get_varga_strength(lord_planet, "D9")
        specific_varga_strength = self.engine.get_varga_strength(lord_planet, varga_chart)
        vimshopaka_score = self.engine.get_vimshopaka_score(lord_planet)

        # --- 40:30:30 మ్యాథ్ లేయర్స్ ---
        layer_1_score = 0.40 * bhava_lord_strength
        layer_2_score = 0.30 * karaka_strength
        layer_3_score = (0.15 * d9_strength) + (0.10 * specific_varga_strength) + (0.05 * vimshopaka_score)
        
        # టోటల్ బేస్ స్కోరు
        final_score = layer_1_score + layer_2_score + layer_3_score

        # --- స్పెషల్ మోడిఫైయర్స్ & గార్డ్రైల్స్ ---
        
        # 1. కారక భావ నాశాయ్ ఫిల్టర్
        if self.engine.is_karaka_in_bhava(karaka_planet, bhava_idx):
            final_score *= 0.90  # 10% డిలే మోడిఫైయర్

        # 2. పుష్కర నవాంశ లేదా వర్గోత్తమ మోడిఫైయర్ (+5% క్లాసికల్ బంప్)
        if self.engine.is_vargottama(lord_planet) or self.engine.is_pushkara(lord_planet):
            final_score += 5.0

        # క్లాంప్ గార్డ్ (0 - 100 రేంజ్ లాక్)
        final_score = max(0.0, min(100.0, final_score))

        return int(math.ceil(final_score))

    def evaluate_all_queries(self, gender="Male"):
        """
        మాస్టర్ మ్యాట్రిక్స్ లోని అన్ని క్లాసికల్ ప్రశ్నల సమగ్ర లెక్కింపు
        """
        query_matrix = {
            # Bhava 1 & 2
            "Q1": {"house": 1, "lord": "Lagna_Lord", "karaka": "Sun", "varga": "D3"},
            "Q2": {"house": 1, "lord": "Lagna_Lord", "karaka": "Sun", "varga": "D3"},
            "Q5": {"house": 2, "lord": "Second_Lord", "karaka": "Jupiter", "varga": "D2"},
            "Q6": {"house": 2, "lord": "Second_Lord", "karaka": "Jupiter", "varga": "D12"},
            # Bhava 4 & 5
            "Q14": {"house": 4, "lord": "Fourth_Lord", "karaka": "Mars", "varga": "D4"},
            "Q16": {"house": 4, "lord": "Fourth_Lord", "karaka": "Venus", "varga": "D16"},
            "Q19": {"house": 5, "lord": "Fifth_Lord", "karaka": "Jupiter", "varga": "D7"},
            "Q23": {"house": 5, "lord": "Fifth_Lord", "karaka": "Jupiter", "varga": "D24"},
            # Bhava 6 & 7
            "Q26": {"house": 6, "lord": "Sixth_Lord", "karaka": "Saturn", "varga": "D6"},
            "Q31": {"house": 7, "lord": "Seventh_Lord", "karaka": "Venus", "varga": "D9"}, # Dynamic Switch
            "Q40": {"house": 7, "lord": "Seventh_Lord", "karaka": "Mercury", "varga": "D10"},
            # Bhava 8, 9 & 10
            "Q41": {"house": 8, "lord": "Eighth_Lord", "karaka": "Saturn", "varga": "D8"},
            "Q46": {"house": 9, "lord": "Ninth_Lord", "karaka": "Jupiter", "varga": "D9"},
            "Q50": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D10"},
            "Q51": {"house": 10, "lord": "Tenth_Lord", "karaka": "Sun", "varga": "D10"},
            "Q53": {"house": 10, "lord": "Tenth_Lord", "karaka": "Mercury", "varga": "D10"},
            # Politics & Past Life Tracks
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
