import math

class SamarthaQueryEngine:
    def __init__(self, graha_bala_engine):
        """
        సమర్థ క్వెరీ ఇంజన్ - 40:30:30 వెయిటేజీ ఫార్ములా అమలు
        :param graha_bala_engine: కోర్ గణిత ఇంజన్ నుండి వచ్చే గ్రహాల బలాల డేటా
        """
        self.engine = graha_bala_engine

    def calculate_query_score(self, query_id, bhava_idx, lord_planet, karaka_planet, varga_chart, gender="Male"):
        """
        ప్రతి సింగిల్-ఫోకస్ ప్రశ్నకు 100 మార్కులకు గాను స్కోరును లెక్కిస్తుంది (Strict Integer Rounding)
        """
        # 1. జెండర్ ఆధారిత కారకత్వ స్విచ్ (వివాహ ప్రశ్నల కోసం)
        if query_id in ["Q13", "Q14", "Q31", "Q32"] and karaka_planet in ["Venus", "Jupiter"]:
            karaka_planet = "Venus" if gender == "Male" else "Jupiter"

        # కోర్ బలాలను ఫెచ్ చేయడం (0 - 100 రేంజ్ లో అనుకుంటాం)
        bhava_lord_strength = self.engine.get_planet_strength(lord_planet)
        karaka_strength = self.engine.get_planet_strength(karaka_planet)
        
        # వర్గ చక్రాల బలాలు
        d9_strength = self.engine.get_varga_strength(lord_planet, "D9")
        specific_varga_strength = self.engine.get_varga_strength(lord_planet, varga_chart)
        vimshopaka_score = self.engine.get_vimshopaka_score(lord_planet)

        # --- 40:30:30 మ్యాథ్ లేయర్స్ ---
        
        # లేయర్ 1: D1 భావాధిపతి బలం (40%)
        layer_1_score = 0.40 * bhava_lord_strength
        
        # లేయర్ 2: నిసర్గ కారక గ్రహ బలం (30%)
        layer_2_score = 0.30 * karaka_strength
        
        # లేయర్ 3: షోడశ వర్గాల బలం (30% టోటల్ -> 15% D9 + 10% Sp.Varga + 5% Vimshopaka)
        layer_3_score = (0.15 * d9_strength) + (0.10 * specific_varga_strength) + (0.05 * vimshopaka_score)
        
        # టోటల్ బేస్ స్కోరు
        final_score = layer_1_score + layer_2_score + layer_3_score

        # --- స్పెషల్ మోడిఫైయర్స్ & గార్డ్రైల్స్ ---
        
        # కారక భావ నాశాయ్ ఫిల్టర్ (కారకుడే స్వయంగా ఆ ఇంట్లో కూర్చుంటే వచ్చే నెగటివ్ ఇంపాక్ట్)
        if self.engine.is_karaka_in_bhava(karaka_planet, bhava_idx):
            # కారక భావ నాశాయ్ వర్తిస్తే 10% స్కోరు తగ్గించి ఆలస్యాన్ని సూచిస్తాం
            final_score *= 0.90

        # పుష్కర నవాంశ లేదా వర్గోత్తమ మోడిఫైయర్ (+5% బోనస్ క్లాసికల్ బంప్)
        if self.engine.is_vargottama(lord_planet) or self.engine.is_pushkara(lord_planet):
            final_score += 5.0

        # క్లాంప్ గార్డ్ (ఎట్టి పరిస్థితుల్లోనూ 100 దాటకూడదు, 0 కంటే తగ్గకూడదు)
        final_score = max(0.0, min(100.0, final_score))

        # Global No-Decimals Constraint: క్లీన్ ఇంటిజర్గా రౌండ్ చేయడం
        return int(math.ceil(final_score))

    def evaluate_all_queries(self, birth_data, gender="Male"):
        """
        మాస్టర్ మ్యాట్రిక్స్ లోని అన్ని ప్రశ్నలను లూప్ రన్ చేసి రిపోర్ట్ జనరేట్ చేస్తుంది
        """
        results = {}
        # ఉదాహరణకు కొన్ని ముఖ్యమైన ప్రశ్నల మ్యాపింగ్ లూప్
        query_matrix = {
            "Q1": {"house": 1, "lord": "Mars", "karaka": "Sun", "varga": "D3"},
            "Q5": {"house": 2, "lord": "Venus", "karaka": "Jupiter", "varga": "D2"},
            "Q7": {"house": 4, "lord": "Moon", "karaka": "Mars", "varga": "D4"},
            "Q9": {"house": 5, "lord": "Sun", "karaka": "Jupiter", "varga": "D7"},
            "Q13": {"house": 7, "lord": "Venus", "karaka": "Venus", "varga": "D9"}, # జెండర్ స్విచ్ అవుతుంది
            "Q51": {"house": 10, "lord": "Saturn", "karaka": "Sun", "varga": "D10"}
        }

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
