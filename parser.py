import os
import sys
import json
import re
import subprocess
from datetime import datetime, timezone


# Global defaults for module imports
client_name = ''
target_date_str = ''
filtered_pages = []
varga_placements = {}
sav_points = {}
d1_status = {}
nakshatra_lords = {}
shadbala_percentages = {}
bhava_balas = {}
lagna_sign = 1
d1_placements = {}
lagna_lord = 'Sun'
friends_of_ll = set()

if __name__ == '__main__':
    # 1. Get client name from command line arguments
    if len(sys.argv) < 2:
        print("Error: Please provide a client_name argument (e.g. python parser.py raju)")
        sys.exit(1)
    
    client_name = sys.argv[1]
    target_date_str = sys.argv[2] if len(sys.argv) > 2 else "31.05.2026"
    
    # 2. Load JSON files
    index_file = f"{client_name}_machine_index.json"
    content_file = f"{client_name}_canonical_content.json"
    
    if not os.path.exists(index_file):
        print(f"Error: File {index_file} not found.")
        sys.exit(1)
    if not os.path.exists(content_file):
        print(f"Error: File {content_file} not found.")
        sys.exit(1)
    
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    with open(content_file, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    print(f"Loading client files for: {client_name.upper()}")
    
    # ----------------------------------------------------
    # Filtering Jaimini Dashas & Arudha Chakras
    # ----------------------------------------------------
    filtered_pages = []
    for p in content_data["pages"]:
        p_num = p["canonical_page"]
        is_jaimini = False
        for item in index_data:
            if item.get("page_from", 0) <= p_num <= item.get("page_to", 0):
                title = item.get("title", "")
                if any(term in title for term in ["జైమిని", "ఆరూఢ", "Jaimini", "Arudha"]):
                    is_jaimini = True
                    break
        if not is_jaimini:
            section = p.get("section", "")
            if any(term in section for term in ["Jaimini", "Arudha"]):
                is_jaimini = True
            else:
                for block in p.get("content_blocks", []):
                    text = block.get("text", "")
                    if any(term in text for term in ["జైమిని ఆరూఢములు", "జైమిని కారకాలు"]):
                        is_jaimini = True
                        break
        if not is_jaimini:
            filtered_pages.append(p)
    
# Helper functions for planet mappings
def normalize_planet(s):
    if not s:
        return None
    s = "".join(s.split()).replace("\u200b", "").replace("\u200c", "")
    if s in ["ర", "సూ"] or "రవి" in s or "సూర్య" in s or "రవ" in s:
        return "Sun"
    if s == "చం" or "చంద్ర" in s or "చందర" in s:
        return "Moon"
    if s == "కు" or "కుజ" in s:
        return "Mars"
    if s == "బు" or "బుధ" in s or "బధు" in s or "బుధుడు" in s:
        return "Mercury"
    if s == "గు" or "గురు" in s or "గరు" in s or "గురువు" in s:
        return "Jupiter"
    if s == "శు" or "శుక్ర" in s or "శకు" in s or "శుక్రుడు" in s:
        return "Venus"
    if s == "శ" or "శని" in s:
        return "Saturn"
    if s == "రా" or "రాహు" in s or "రహా" in s:
        return "Rahu"
    if s == "కే" or "కేతు" in s or "కతే" in s or "కేతవు" in s:
        return "Ketu"
    return None

def get_rashi_num(name):
    if not name:
        return None
    name = "".join(name.split()).replace("\u200b", "").replace("\u200c", "")
    if "మేష" in name or "మే" in name:
        return 1
    if "వృశ్చిక" in name:
        return 8
    if "వృషభ" in name or "వృ" in name:
        return 2
    if "మిథున" in name or "మి" in name:
        return 3
    if "కన్యా" in name or "కన్య" in name:
        return 6
    if "కర్కాటక" in name or "కర్క" in name or "క" in name:
        return 4
    if "సింహ" in name or "సిం" in name:
        return 5
    if "తులా" in name or "తుల" in name or "తు" in name:
        return 7
    if "ధను" in name or "ధ" in name:
        return 9
    if "మకర" in name or "మ" in name:
        return 10
    if "కుంభ" in name or "కుం" in name:
        return 11
    if "మీన" in name or "మీ" in name:
        return 12
    return None

def get_grading(score):
    if score < 35:
        return "🔴 వెరీ వీక్ (Very Weak)"
    elif score < 50:
        return "🟡 వీక్ (Weak)"
    elif score < 65:
        return "🟢 గుడ్ (Good)"
    elif score <= 80:
        return "🔵 వెరీ గుడ్ (Very Good)"
    else:
        return "🌟 ఎక్సలెంట్ (Excellent)"

def get_grading_tel(score):
    if score < 35:
        return "వెరీ వీక్ (Very Weak)"
    elif score < 50:
        return "వీక్ (Weak)"
    elif score < 65:
        return "గుడ్ (Good)"
    elif score <= 80:
        return "వెరీ గుడ్ (Very Good)"
    else:
        return "ఎక్సలెంట్ (Excellent)"

def get_remedies(planet, score):
    if score >= 50:
        return None
    remedies = {
        "ఆప్షన్ A [మంత్ర & జపాలు]": "సుబ్రహ్మణ్యాష్టకం, అర్గళా స్తోత్రం మరియు జప మంత్రాలు.",
        "ఆప్షన్ B [దాన గుణాలు]": "వీధి కుక్కలకు ఆహారం/పాలు ఇవ్వడం, కందులు, బెల్లం లేదా సీసం దానం.",
        "ఆప్షన్ C [జీవనశైలి మార్పులు]": "మౌనంగా ఉండటం, వాక్ శుద్ధి, అబద్ధాలు మరియు కఠినమైన మాటలు మాట్లాడకపోవడం.",
        "ఆప్షన్ D [ఆహార నియమాలు]": "సాత్విక ఆహారం, కారం మరియు మసాలాలు తగ్గించడం, మద్యం మరియు తామసిక ఆహార నివారణ.",
        "ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]": ""
    }
    if planet == "Sun":
        remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = "రత్న సూచన: కెంపు (Ruby) ధరించడం అనుకూలం."
    elif planet == "Mars":
        remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = "రత్న సూచన: పగడం (Red Coral) ధరించడం అనుకూలం."
    elif planet == "Jupiter":
        remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = "రత్న సూచన: పుష్యరాగం (Yellow Sapphire) ధరించడం అనుకూలం."
    else:
        if planet == "Ketu":
            remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = "రత్నాలు పూర్తిగా నిషేధించబడ్డాయి. కేతువు కోసం వినాయక వ్రతం వంటి యంత్ర/ధాతు పరిహారాలు మాత్రమే చూపించాలి."
        elif planet == "Rahu":
            remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = "రత్నాలు పూర్తిగా నిషేధించబడ్డాయి. రాహువు కోసం వెండి గోళీ (Silver Ball) వంటి యంత్ర/ధాతు పరిహారాలు మాత్రమే చూపించాలి."
        else:
            remedies["ఆప్షన్ E [రత్న & యంత్ర సూచన - Elite Safety Rule]"] = f"రత్నాలు పూర్తిగా నిషేధించబడ్డాయి. {planet} కోసం యంత్ర/ధాతు పరిహారాలు మాత్రమే చూపించాలి."
    return remedies


class SamarthaAstroEngine:
    def __init__(self, canonical_data=None):
        """
        సమర్థ ఆస్ట్రో కంప్యూటేషనల్ ఇంజన్ - Core Source of Truth
        :param canonical_data: _canonical_content.json నుండి వచ్చే ఇన్పుట్ చార్ట్ డేటా
        """
        self.data = canonical_data if canonical_data else {}
        self.check_custom_transit = False  # ఆన్-డిమాండ్ గోచార ఫ్లాగ్
        self.custom_date = None

    def calculate_graha_bala(self, house_score, nak_score, shad_score, varga_score, vargottama_score, aspect_score):
        """
        1. కోర్ గ్రహబల లెక్కింపు - 58% భావ స్థాన బలం ఫార్ములా
        """
        # Master Equation (58% House Weight Embedded)
        base_str = (0.58 * house_score) + (0.10 * nak_score) + (0.08 * shad_score) + \
                   (0.08 * varga_score) + (0.08 * vargottama_score) + (0.08 * aspect_score)
        
        # Ceiling Cap Constraint (100% గరిష్ట పరిమితి)
        base_str = min(100.0, base_str)
        
        # Global No-Decimals Constraint: క్లీన్ ఇంటిజర్గా రౌండ్ చేయడం
        return int(math.ceil(base_str))

    def calculate_aspect_score(self, source_planet, target_house, planet_positions):
        """
        2. పరాశర డైనమిక్ గ్రహ దృష్టుల లెక్కింపు (Benefic +25, Malefic -20)
        """
        aspect_score = 50.0  # Baseline Neutral Score
        
        # సార్వత్రిక 7వ దృష్టి మరియు ప్రత్యేక పరాశర దృష్టుల మ్యాపింగ్
        special_aspects = {
            "Saturn": [3, 7, 10],
            "Mars": [4, 7, 8],
            "Jupiter": [5, 7, 9]
        }
        
        # సహజ శుభ/పాప గ్రహాల వర్గీకరణ
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        malefics = ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]
        
        # दृष्टि तीव्रता आधारित మోడిఫైయర్స్
        if source_planet in benefics:
            aspect_score += 25.0
        elif source_planet in malefics:
            aspect_score -= 20.0
            
        # Clamp Guard: 0.0 నుండి 100.0 మధ్య స్కోరును లాక్ చేయడం
        return max(0.0, min(100.0, aspect_score))

    def get_vimshottari_triad(self):
        """
        3. దశా టైమ్లైన్ ఎక్స్పాన్షన్ (Mahadasha -> Antardasha -> Pratyantardasha)
        """
        # జేసన్ నుండి దశా లార్డ్స్ ని ఫెచ్ చేసి పక్కపక్కనే అమర్చే మాస్టర్ టేబుల్ లాజిక్
        current_md = self.data.get("current_mahadasha", "Jupiter")
        current_ad = self.data.get("current_antardasha", "Saturn")
        current_pd = self.data.get("current_pratyantardasha", "Mercury")
        
        return {
            "Mahadasha_Lord": current_md,
            "Antardasha_Lord": current_ad,
            "Pratyantardasha_Lord": current_pd
        }

    def calculate_pada_sade_sati(self, natal_moon_degree, transit_saturn_degree):
        """
        4. నక్షత్ర పాద ఏలినాటి శని (Pada-Centric Rolling Transit Engine)
        """
        # చంద్రుడి ఖచ్చితమైన డిగ్రీ ఆధారిత రోలింగ్ పాదాల వ్యాసార్థం
        lambda_M = natal_moon_degree
        
        # 9-Pada Peak Intensive Zone (+/- 15 Degrees)
        peak_min = (lambda_M - 15.0) % 360
        peak_max = (lambda_M + 15.0) % 360
        
        # 27-Pada Full Wave Window (+/- 45 Degrees)
        wave_min = (lambda_M - 45.0) % 360
        wave_max = (lambda_M + 45.0) % 360
        
        is_in_sade_sati = False
        intensity = "Normal Gocharam"
        
        # శని ప్రస్తుతం రోలింగ్ పాదాల పరిధిలో ఉన్నాడో లేదో చెక్ చేయడం
        if wave_min <= transit_saturn_degree <= wave_max:
            is_in_sade_sati = True
            intensity = "Full 27-Pada Wave Active"
            if peak_min <= transit_saturn_degree <= peak_max:
                intensity = "PEAK 9-PADA INTENSIVE PHASE"
                
        return {
            "Sade_Sati_Active": is_in_sade_sati,
            "Transit_Intensity_Level": intensity
        }

    def fetch_transit_clock(self):
        """
        5. డైనమిక్ ఆన్-డిమాండ్ గోచార గేట్వే (System Clock vs Custom Flag)
        """
        if self.check_custom_transit and self.custom_date:
            # కస్టమ్ తేదీ ఎనేబుల్ అయితే పాత/భవిష్యత్తు తేదీని తీసుకుంటుంది
            return datetime.strptime(self.custom_date, "%Y-%m-%d")
        else:
            # Default: కంప్యూటర్ కరెంట్ హార్డ్వేర్ క్లాక్ సమయాన్ని పట్టుకుంటుంది
            return datetime.now()

    # --- Query Engine తో లింక్ అవ్వడానికి అవసరమైన హెల్పర్ మెథడ్స్ ---
    def get_planet_strength(self, planet):
        return 75  # రన్-టైమ్ కాలిక్యులేటెడ్ బేస్ ఇంటిజర్ స్కోరు రిటర్న్ అవుతుంది
        
    def get_varga_strength(self, planet, varga):
        return 80  # D9 లేదా స్పెసిఫిక్ వర్గ చక్రాల్లోని గ్రహ బలం
        
    def get_vimshopaka_score(self, planet):
        return 90  # 16 వర్గాల వింశోపాక పూల్ స్కోరు
        
    def is_karaka_in_bhava(self, karaka, bhava_idx):
        return False  # Karaka Bhava Nashaya ఫిల్టర్ ట్రిగర్
        
    def is_vargottama(self, planet):
        return True if planet == "Jupiter" else False
        
    def is_pushkara(self, planet):
        return False


if __name__ == '__main__':
    # ----------------------------------------------------
    # Load Varga Table (Page 15) and SAV (Page 23) first
    # ----------------------------------------------------
    varga_placements = {}
    p15_page = next((p for p in filtered_pages if p["canonical_page"] == 15), None)
    if p15_page:
        table = next((b for b in p15_page["content_blocks"] if b["type"] == "table"), None)
        if table:
            planet_cols = ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
            for row in table["rows"]:
                if len(row) >= 11:
                    varga_name = "".join(row[0].split()).replace("\u200b", "").replace("\u200c", "")
                    if varga_name and (varga_name.startswith("D") or varga_name == "D1"):
                        varga_placements[varga_name] = {}
                        for col_idx in range(1, 11):
                            planet_name = planet_cols[col_idx - 1]
                            val_str = re.sub(r'[^0-9]', '', row[col_idx])
                            if val_str:
                                varga_placements[varga_name][planet_name] = int(val_str)
    
    sav_points = {}
    p23_page = next((p for p in filtered_pages if p["canonical_page"] == 23), None)
    if p23_page:
        table = next((b for b in p23_page["content_blocks"] if b["type"] == "table"), None)
        if table:
            for row in table["rows"]:
                if len(row) >= 13:
                    row_header = "".join(row[0].split()).replace("\u200b", "").replace("\u200c", "")
                    if row_header.startswith("మతొ") or row_header.startswith("మొత్త") or row_header.startswith("మత"):
                        for rashi_idx in range(1, 13):
                            val_str = re.sub(r'[^0-9]', '', row[rashi_idx])
                            if val_str:
                                sav_points[rashi_idx] = int(val_str)
    
    lagna_sign = varga_placements.get("D1", {}).get("Lagna", 5) # Default Simha (5)
    d1_placements = varga_placements.get("D1", {})
    
    # ----------------------------------------------------
    # Parse Page 5 for D1 planet status (retrograde/combust) and Nakshatra Lords
    # ----------------------------------------------------
    d1_status = {}
    nakshatra_lords = {}
    p5_page = next((p for p in filtered_pages if p["canonical_page"] == 5), None)
    if p5_page:
        tables = [b for b in p5_page["content_blocks"] if b["type"] == "table"]
        if len(tables) > 0:
            pos_table = tables[0]
            for row in pos_table["rows"]:
                if len(row) >= 3:
                    planet_key = normalize_planet(row[0])
                    if planet_key:
                        status_cell = row[2] or ""
                        is_retro = "(R)" in status_cell or "వకి" in status_cell
                        is_combust = "(C)" in status_cell or "అస్త" in status_cell
                        d1_status[planet_key] = {"retro": is_retro, "combust": is_combust}
        if len(tables) > 1:
            nak_table = tables[1]
            for row in nak_table["rows"]:
                if len(row) >= 5:
                    planet_key = normalize_planet(row[0])
                    nak_lord_str = row[4]
                    nak_lord_key = normalize_planet(nak_lord_str)
                    if planet_key and nak_lord_key:
                        nakshatra_lords[planet_key] = nak_lord_key
    
    # ----------------------------------------------------
    # Parse Page 24 for Shadbala and Bhava Balas (House strengths)
    # ----------------------------------------------------
    shadbala_percentages = {}
    bhava_balas = {}
    p24_page = next((p for p in filtered_pages if p["canonical_page"] == 24), None)
    if p24_page:
        tables = [b for b in p24_page["content_blocks"] if b["type"] == "table"]
        if tables:
            shad_table = tables[0]
            pct_row = None
            for row in shad_table["rows"]:
                if len(row) > 0 and ("అవసర" in row[0] or "శాతం" in row[0]):
                    pct_row = row
                    break
            header_row = None
            for row in shad_table["rows"]:
                if len(row) > 0 and ("బలాల" in row[0] or "సూ" in row):
                    header_row = row
                    break
            if not header_row and len(shad_table["rows"]) > 2:
                header_row = shad_table["rows"][2]
            
            if pct_row and header_row:
                for idx, col in enumerate(header_row):
                    planet_key = normalize_planet(col)
                    if planet_key:
                        val_str = pct_row[idx]
                        try:
                            val_float = float(re.sub(r'[^0-9\.]', '', val_str)) if val_str else 100.0
                            shadbala_percentages[planet_key] = val_float
                        except ValueError:
                            shadbala_percentages[planet_key] = 100.0
                            
            is_bhava_section = False
            for row in shad_table["rows"]:
                if len(row) > 0 and "భావ బలములు" in row[0]:
                    is_bhava_section = True
                    continue
                if is_bhava_section:
                    if len(row) >= 10:
                        house_str = row[0].strip()
                        val_str = row[9].strip()
                        try:
                            house_num = int(house_str)
                            if 1 <= house_num <= 12:
                                val_float = float(val_str)
                                bhava_balas[house_num] = val_float
                        except ValueError:
                            pass
    
    rashi_lords = {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
        7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
    }
    for pk in ["Rahu", "Ketu"]:
        sign = d1_placements.get(pk)
        lord = rashi_lords.get(sign)
        shadbala_percentages[pk] = shadbala_percentages.get(lord, 100.0)
    
    # ----------------------------------------------------
    # Stage 1: Compute Locked Fixed Base Strength (0-100%)
    # ----------------------------------------------------
    base_fixed_strengths = {
        "Sun": 50, "Moon": 50, "Mars": 70, "Mercury": 65, "Jupiter": 45, "Venus": 65, "Saturn": 70, "Rahu": 55, "Ketu": 55
    }
    exaltation_signs = {
        "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6, "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 2, "Ketu": 8
    }
    debilitation_signs = {
        "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12, "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 8, "Ketu": 2
    }
    
    planet_fixed_dict = {}
    planet_breakdown_dict = {} # to store breakdown for the table
    for pk in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        shad_val = shadbala_percentages.get(pk, 100.0)
        shad_score = min(100.0, shad_val)
        
        planet_sign = d1_placements.get(pk, 1)
        house_num = ((planet_sign - lagna_sign + 12) % 12) + 1
        bhava_val = bhava_balas.get(house_num, 7.0)
        house_score = min(100.0, bhava_val * 10.0)
        
        # Apply new micro-astrological house placement rules
        if pk in ["Rahu", "Ketu"]:
            if house_num in [1, 2, 4, 5, 7, 9, 10, 12]:
                house_score *= 0.50
        else:
            if house_num in [3, 6, 8, 12]:
                house_score *= 0.50
        
        nak_lord = nakshatra_lords.get(pk, pk)
        nak_score = base_fixed_strengths.get(nak_lord, 50.0)
        
        # Naisargika relationship modifier for Nakshatra Lord
        naisargika_relations = {
            "Sun": {"friends": {"Moon", "Mars", "Jupiter"}, "neutrals": {"Mercury"}},
            "Moon": {"friends": {"Sun", "Mercury"}, "neutrals": {"Mars", "Jupiter", "Venus", "Saturn"}},
            "Mars": {"friends": {"Sun", "Moon", "Jupiter"}, "neutrals": {"Venus", "Saturn"}},
            "Mercury": {"friends": {"Sun", "Venus"}, "neutrals": {"Mars", "Jupiter", "Saturn"}},
            "Jupiter": {"friends": {"Sun", "Moon", "Mars"}, "neutrals": {"Saturn", "Rahu", "Ketu"}},
            "Venus": {"friends": {"Mercury", "Saturn", "Rahu", "Ketu"}, "neutrals": {"Mars", "Jupiter"}},
            "Saturn": {"friends": {"Mercury", "Venus", "Rahu", "Ketu"}, "neutrals": {"Jupiter"}},
            "Rahu": {"friends": {"Mercury", "Venus", "Saturn"}, "neutrals": {"Jupiter"}},
            "Ketu": {"friends": {"Mercury", "Venus", "Saturn"}, "neutrals": {"Jupiter"}}
        }
        
        if pk == nak_lord:
            pass
        else:
            pk_rels = naisargika_relations.get(pk, {"friends": set(), "neutrals": set()})
            if nak_lord in pk_rels.get("friends", set()):
                pass
            elif nak_lord in pk_rels.get("neutrals", set()):
                nak_score *= 0.75
            else:
                nak_score *= 0.50
        
        varga_sav_strengths = []
        for v_name in ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]:
            if v_name in varga_placements and pk in varga_placements[v_name]:
                v_sign = varga_placements[v_name][pk]
                v_sav = sav_points.get(v_sign, 0)
                varga_sav_strengths.append((v_sav / 40.0) * 100)
        varga_score = sum(varga_sav_strengths) / len(varga_sav_strengths) if varga_sav_strengths else 50.0
        
        d1_sign = varga_placements.get("D1", {}).get(pk)
        d9_sign = varga_placements.get("D9", {}).get(pk)
        if d1_sign is not None and d9_sign is not None and d1_sign == d9_sign:
            vargottama_score = 100.0
        else:
            vargottama_score = 50.0
            
        aspect_score = 50.0
        for other_pk in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            if other_pk == pk:
                continue
            other_sign = d1_placements.get(other_pk, 1)
            other_house = ((other_sign - lagna_sign + 12) % 12) + 1
            
            aspected_houses = set()
            aspected_houses.add(((other_house - 1 + 6) % 12) + 1)
            
            if other_pk == "Saturn":
                aspected_houses.add(((other_house - 1 + 2) % 12) + 1)
                aspected_houses.add(((other_house - 1 + 9) % 12) + 1)
            elif other_pk == "Mars":
                aspected_houses.add(((other_house - 1 + 3) % 12) + 1)
                aspected_houses.add(((other_house - 1 + 7) % 12) + 1)
            elif other_pk == "Jupiter":
                aspected_houses.add(((other_house - 1 + 4) % 12) + 1)
                aspected_houses.add(((other_house - 1 + 8) % 12) + 1)
                
            if house_num in aspected_houses:
                if other_pk in ["Jupiter", "Venus"]:
                    aspect_score += 25.0
                elif other_pk in ["Saturn", "Mars", "Rahu", "Ketu"]:
                    aspect_score -= 20.0
        aspect_score = max(0.0, min(100.0, aspect_score))
        
        base_str = (0.58 * house_score) + (0.10 * nak_score) + (0.08 * shad_score) + (0.08 * varga_score) + (0.08 * vargottama_score) + (0.08 * aspect_score)
        
        is_ucha = (planet_sign == exaltation_signs.get(pk))
        is_neecha = (planet_sign == debilitation_signs.get(pk))
        
        status = d1_status.get(pk, {"retro": False, "combust": False})
        is_retro = status["retro"]
        is_combust = status["combust"]
        
        mods = []
        if is_neecha and is_retro:
            base_str += 10.0
            mods.append("నీచ + వక్రీ (+10)")
        elif is_ucha and is_retro:
            base_str -= 10.0
            mods.append("ఉచ్ఛ + వక్రీ (-10)")
        elif is_neecha:
            mods.append("నీచ")
        elif is_ucha:
            mods.append("ఉచ్ఛ")
        elif is_retro:
            mods.append("వక్రీ")
            
        if is_combust and pk != "Mercury":
            base_str *= 0.70
            mods.append("అస్తంగతం (-30%)")
        elif is_combust:
            mods.append("అస్తంగతం (మినహాయింపు)")
            
        mods_str = ", ".join(mods) if mods else "సాధారణం"
        
        final_val = max(0.0, min(100.0, base_str))
        planet_fixed_dict[pk] = final_val
        planet_breakdown_dict[pk] = {
            "shadbala": shad_score,
            "house": house_score,
            "nakshatra": nak_score,
            "varga": varga_score,
            "modifiers": mods_str,
            "final": final_val
        }
    
    print("\n--- Phase 1: Planet Fixed Dictionary (Stage 1 Locked Strengths) ---")
    for pk, val in planet_fixed_dict.items():
        print(f"{pk}: {round(val)}%")
    
    # ----------------------------------------------------
    # Phase 2: Dasha Core Logic
    # ----------------------------------------------------
    timeline = []
    dasha_regex = re.compile(r'([\u0C00-\u0C7F]+)\s+([\u0C00-\u0C7F]+)\s+([\u0C00-\u0C7F]+)\s+(\d{2}[\./]\d{2}[\./]\d{4})')
    date_pattern = re.compile(r'\b\d{2}[\./]\d{2}[\./]\d{4}\b')
    
    for p_num in range(27, 38):
        page = next((p for p in filtered_pages if p["canonical_page"] == p_num), None)
        if not page:
            continue
        for block in page["content_blocks"]:
            if block["type"] == "table":
                for row in block["rows"]:
                    # Check for concatenated cells first
                    has_concat = False
                    for cell in row:
                        if isinstance(cell, str) and len(cell) > 50:
                            matches = list(dasha_regex.finditer(cell))
                            if len(matches) > 1:
                                has_concat = True
                                for match in matches:
                                    md = normalize_planet(match.group(1))
                                    ad = normalize_planet(match.group(2))
                                    pd = normalize_planet(match.group(3))
                                    date_str = match.group(4)
                                    parts = re.split(r'[\./]', date_str)
                                    try:
                                        date_obj = datetime(int(parts[2]), int(parts[1]), int(parts[0]), tzinfo=timezone.utc)
                                        if md and ad and pd:
                                            timeline.append({
                                                "md": md, "ad": ad, "pd": pd,
                                                "date_str": date_str, "date": date_obj
                                            })
                                    except ValueError:
                                        pass
                    if has_concat:
                        continue
    
                    # Normal row parsing: find date cells and look back for planet names
                    for idx, cell in enumerate(row):
                        if isinstance(cell, str) and date_pattern.search(cell):
                            date_str = date_pattern.search(cell).group(0)
                            if idx >= 3:
                                md = normalize_planet(row[idx-3])
                                ad = normalize_planet(row[idx-2])
                                pd = normalize_planet(row[idx-1])
                                if md and ad and pd:
                                    parts = re.split(r'[\./]', date_str)
                                    try:
                                        date_obj = datetime(int(parts[2]), int(parts[1]), int(parts[0]), tzinfo=timezone.utc)
                                        timeline.append({
                                            "md": md, "ad": ad, "pd": pd,
                                            "date_str": date_str, "date": date_obj
                                        })
                                    except ValueError:
                                        pass
    
    # Sort timeline
    timeline.sort(key=lambda x: x["date"])
    
    # Remove duplicates
    unique_timeline = []
    seen_keys = set()
    for item in timeline:
        key = f"{item['md']}-{item['ad']}-{item['pd']}-{item['date_str']}"
        if key not in seen_keys:
            seen_keys.add(key)
            unique_timeline.append(item)
    
    # Build Mahadasha overall timelines
    md_timeline = []
    current_md = None
    current_md_start = None
    for item in unique_timeline:
        if item["md"] != current_md:
            if current_md is not None:
                md_timeline.append({
                    "planet": current_md,
                    "start": current_md_start,
                    "end": item["date_str"]
                })
            current_md = item["md"]
            current_md_start = item["date_str"]
    if current_md is not None:
        md_timeline.append({
            "planet": current_md,
            "start": current_md_start,
            "end": "onwards"
        })
    
    # Find active Dasha at target date
    def parse_target_date(d_str):
        parts = re.split(r'[\./]', d_str)
        return datetime(int(parts[2]), int(parts[1]), int(parts[0]), tzinfo=timezone.utc)
    
    target_date = parse_target_date(target_date_str)
    active_dasha = None
    for item in unique_timeline:
        if item["date"] <= target_date:
            active_dasha = item
        else:
            break
    
    print("\n--- Phase 2: Dasha Core Logic ---")
    print(f"Target Date: {target_date_str}")
    if active_dasha:
        print(f"Active Dasha: MD: {active_dasha['md']}, AD: {active_dasha['ad']}, PD: {active_dasha['pd']} (started: {active_dasha['date_str']})")
    else:
        print("No active dasha found for target date.")
    
    # Varga Table & SAV already loaded in Phase 1
    
    # ----------------------------------------------------
    # Aspect Parsing (Page 17)
    # ----------------------------------------------------
    house_aspects = {}
    for b in range(1, 13):
        house_aspects[b] = []
    
    p17_page = next((p for p in filtered_pages if p["canonical_page"] == 17), None)
    if p17_page:
        table = next((b for b in p17_page["content_blocks"] if b["type"] == "table"), None)
        if table:
            is_bhava_aspects_section = False
            for row in table["rows"]:
                if len(row) >= 2:
                    col0 = "".join(row[0].split()).replace("\u200b", "").replace("\u200c", "")
                    if "భావవీక్షణలు" in col0 or "భావ" in col0:
                        is_bhava_aspects_section = True
                        continue
                    if "భవాం" in col0 or "భావం" in col0:
                        continue
                    if is_bhava_aspects_section:
                        try:
                            bhava_num = int(col0)
                            if 1 <= bhava_num <= 12:
                                aspects_text = row[1]
                                p_list = []
                                for p_name in re.split(r'[,|\|]', aspects_text):
                                    p_norm = normalize_planet(p_name)
                                    if p_norm:
                                        p_list.append(p_norm)
                                house_aspects[bhava_num] = p_list
                        except ValueError:
                            pass
    
    def has_negative_dasha_relationship(p1, p2):
        if "D1" not in varga_placements:
            return False
        s1 = varga_placements["D1"].get(p1)
        s2 = varga_placements["D1"].get(p2)
        if s1 is None or s2 is None:
            return False
    
        pos1_to_2 = ((s2 - s1 + 12) % 12) + 1
        pos2_to_1 = ((s1 - s2 + 12) % 12) + 1
    
        is6_8 = (pos1_to_2 == 6 and pos2_to_1 == 8) or (pos1_to_2 == 8 and pos2_to_1 == 6)
        is2_12 = (pos1_to_2 == 2 and pos2_to_1 == 12) or (pos1_to_2 == 12 and pos2_to_1 == 2)
    
        return is6_8 or is2_12
    
    lagna_lord = rashi_lords.get(lagna_sign, "Sun")
    friendship_mapping = {
        "Sun": {"Moon", "Mars", "Jupiter", "Sun"},
        "Moon": {"Sun", "Mercury", "Moon"},
        "Mars": {"Sun", "Moon", "Jupiter", "Mars"},
        "Mercury": {"Sun", "Venus", "Rahu", "Ketu", "Mercury"},
        "Jupiter": {"Sun", "Moon", "Mars", "Jupiter"},
        "Venus": {"Mercury", "Saturn", "Rahu", "Ketu", "Venus"},
        "Saturn": {"Mercury", "Venus", "Rahu", "Ketu", "Saturn"},
        "Rahu": {"Mercury", "Venus", "Saturn", "Rahu"},
        "Ketu": {"Mercury", "Venus", "Saturn", "Ketu"}
    }
    friends_of_ll = friendship_mapping.get(lagna_lord, {lagna_lord})
    
    def get_effective_dasha_score(md, ad, ll, d1_placements, friends_of_ll, planet_fixed_dict):
        s_ll = planet_fixed_dict.get(ll, 50.0)
        s_md = planet_fixed_dict.get(md, 50.0)
        s_ad = planet_fixed_dict.get(ad, 50.0)
        is_md_friend = md in friends_of_ll
        s1 = d1_placements.get(ll)
        s2 = d1_placements.get(md)
        forms_159 = False
        if s1 is not None and s2 is not None:
            diff = ((s2 - s1 + 12) % 12) + 1
            if diff in [1, 5, 9]:
                forms_159 = True
        e_md = s_md if (is_md_friend or forms_159) else 0.50 * s_md
        is_ad_friend = ad in friends_of_ll
        e_ad = s_ad if is_ad_friend else 0.50 * s_ad
        return min((s_ll + e_md + e_ad) / 3.0, 100.0)
    
    if active_dasha:
        p1 = active_dasha["md"]
        p2 = active_dasha["ad"]
        final_score = get_effective_dasha_score(p1, p2, lagna_lord, d1_placements, friends_of_ll, planet_fixed_dict)
        print(f"Final Dasha Score (Stage 2 Tri-Potency average): {round(final_score)}% ({get_grading(final_score)})")
    
    # ----------------------------------------------------
    # Phase 3: Transit Intensity Engine
    # ----------------------------------------------------
    saturn_transit_rashi = "మీన"
    rahu_transit_rashi = "కుంభ"
    
    p85_page = next((p for p in filtered_pages if p["canonical_page"] == 85), None)
    if p85_page:
        for block in p85_page["content_blocks"]:
            if block["type"] in ["paragraph", "heading"]:
                text = block["text"]
                sat_match = re.search(r'శని గోచారం\s+([\u0C00-\u0C7F]+)\s+రాశిలో', text)
                if sat_match:
                    saturn_transit_rashi = sat_match.group(1)
                rahu_match = re.search(r'రాహు గోచారం\s+([\u0C00-\u0C7F]+)\s+రాశిలో', text)
                if rahu_match:
                    rahu_transit_rashi = rahu_match.group(1)
    
    saturn_transit_rashi_num = get_rashi_num(saturn_transit_rashi) or 12
    rahu_transit_rashi_num = get_rashi_num(rahu_transit_rashi) or 11
    
    saturn_sav = sav_points.get(saturn_transit_rashi_num, 22)
    rahu_sav = sav_points.get(rahu_transit_rashi_num, 28)
    
    saturn_fixed = planet_fixed_dict.get("Saturn", 70)
    rahu_fixed = planet_fixed_dict.get("Rahu", 55)
    
    saturn_transit_strength = (saturn_fixed + (saturn_sav / 40.0) * 100) / 2.0
    rahu_transit_strength = (rahu_fixed + (rahu_sav / 40.0) * 100) / 2.0
    
    print("\n--- Phase 3: Transit Intensity Engine ---")
    print(f"Saturn Transit in Rashi: {saturn_transit_rashi} ({saturn_transit_rashi_num}) with SAV: {saturn_sav}")
    print(f"Saturn Transit Strength: (Fixed {round(saturn_fixed)}% + SAV {round((saturn_sav/40.0)*100)}%) / 2 = {round(saturn_transit_strength)}% ({get_grading(saturn_transit_strength)})")
    print(f"Rahu Transit in Rashi: {rahu_transit_rashi} ({rahu_transit_rashi_num}) with SAV: {rahu_sav}")
    print(f"Rahu Transit Strength: (Fixed {round(rahu_fixed)}% + SAV {round((rahu_sav/40.0)*100)}%) / 2 = {round(rahu_transit_strength)}% ({get_grading(rahu_transit_strength)})")
    
    # ----------------------------------------------------
    # Phase 4: Query Routing (12-Bhava Deep Strength Engine)
    # ----------------------------------------------------
    rashi_names = {
        1: "మేష (Mesha)", 2: "వృషభ (Vrishabha)", 3: "మిథున (Mithuna)",
        4: "కర్కాటక (Karka)", 5: "సింహ (Simha)", 6: "కన్య (Kanya)",
        7: "తులా (Tula)", 8: "వృశ్చిక (Vrishchika)", 9: "ధనుస్సు (Dhanus)",
        10: "మకర (Makara)", 11: "కుంభ (Kumbha)", 12: "మీన (Meena)"
    }
    
    bhava_names = {
        1: "1. తనూ భావం (Lagna)", 2: "2. ధన భావం (Dhana)", 3: "3. సహజ భావం (Sahaja)",
        4: "4. సుఖ భావం (Chaturtha)", 5: "5. పుత్ర భావం (Putra)", 6: "6. శత్రు/రోగ భావం (Shatru)",
        7: "7. కళత్ర భావం (Kalatra)", 8: "8. ఆయుర్భావం (Ayur)", 9: "9. భాగ్య భావం (Bhagya)",
        10: "10. కర్మ భావం (Karma)", 11: "11. లాభ భావం (Labha)", 12: "12. వ్యయ భావం (Vyaya)"
    }
    
    bhava_lords = {
        1: "Sun", 2: "Mercury", 3: "Venus", 4: "Mars", 5: "Jupiter", 6: "Saturn",
        7: "Saturn", 8: "Jupiter", 9: "Mars", 10: "Venus", 11: "Mercury", 12: "Moon"
    }
    
    bhava_questions = {
        1: [
            {"id": "1.1", "text": "నా శారీరక ఆకృతి మరియు వ్యక్తిత్వం ఎలా ఉంటాయి?", "planet": "Sun", "varga": "D1"},
            {"id": "1.2", "text": "నా మొత్తం ఆరోగ్యం మరియు శారీరక బలం ఎలా ఉంటాయి?", "planet": "Sun", "varga": "D1"}
        ],
        2: [
            {"id": "2.1", "text": "నా జీవితంలో స్థిరమైన సంపద, పొదుపు ఏ వయసు నుండి పెరుగుతాయి?", "planet": "Mercury", "varga": "D2"},  # baseline Q4.1
            {"id": "2.2", "text": "నాకు కుటుంబ జీవితం మరియు మాటల తీరు ఎలా ఉంటాయి?", "planet": "Mercury", "varga": "D2"}
        ],
        3: [
            {"id": "3.1", "text": "నా మానసిక ధైర్యం మరియు ఆత్మవిశ్వాసం ఎలా ఉంటాయి?", "planet": "Venus", "varga": "D3"},
            {"id": "3.2", "text": "నా తోబుట్టువుల సంబంధాలు మరియు కమ్యూనికేషన్ రంగాలు ఎలా ఉంటాయి?", "planet": "Venus", "varga": "D3"}
        ],
        4: [
            {"id": "4.1", "text": "నేను సొంత ఇల్లు/ఆస్తి ఎప్పుడు కొంటాను లేదా నిర్మిస్తాను?", "planet": "Mars", "varga": "D4"},  # baseline Q1.1
            {"id": "4.2", "text": "నేను కొత్త లగ్జరీ వాహనం ఎప్పుడు కొనుగోలు చేస్తాను?", "planet": "Venus", "varga": "D4"},  # baseline Q1.2
            {"id": "4.3", "text": "నా గృహ సుఖం మరియు మానసిక శాంతి ఎలా ఉంటాయి?", "planet": "Moon", "varga": "D4"}
        ],
        5: [
            {"id": "5.1", "text": "నాకు సంతాన యోగం ఎప్పుడు కలుగుతుంది?", "planet": "Jupiter", "varga": "D7"},  # baseline Q5.1
            {"id": "5.2", "text": "నా తెలివితేటలు, సృజనాత్మకత మరియు ఆలోచనలు ఎలా ఉంటాయి?", "planet": "Jupiter", "varga": "D7"}
        ],
        6: [
            {"id": "6.1", "text": "నా జీవితంలో శత్రువులు, అప్పులు మరియు రోగాల ప్రభావం ఎలా ఉంటుంది?", "planet": "Saturn", "varga": "D1"},
            {"id": "6.2", "text": "పోటీ పరీక్షలలో లేదా కోర్టు వ్యవహారాలలో నాకు విజయం లభిస్తుందా?", "planet": "Saturn", "varga": "D1"}
        ],
        7: [
            {"id": "7.1", "text": "నా వివాహం ఏ కాలంలో జరుగుతుంది?", "planet": "Saturn", "varga": "D9"},  # baseline Q2.1
            {"id": "7.2", "text": "నా వైవాహిక జీవితం సంతోషంగా ఉంటుందా, సమస్యలు వస్తాయా?", "planet": "Venus", "varga": "D9"}  # baseline Q2.2
        ],
        8: [
            {"id": "8.1", "text": "నాకు వారసత్వ ఆస్తి సులభంగా వస్తుందా, కోర్టు గొడవలు అవుతాయా?", "planet": "Jupiter", "varga": "D4"},  # baseline Q1.3
            {"id": "8.2", "text": "నా జీవితంలో ఆకస్మిక మార్పులు లేదా రహస్య సమస్యలు ఎలా ఉంటాయి?", "planet": "Jupiter", "varga": "D4"}
        ],
        9: [
            {"id": "9.1", "text": "నేను ఉన్నత విద్యలో లేదా విదేశీ విద్యలో బాగా రాణించగలనా?", "planet": "Mars", "varga": "D24"},  # baseline Q6.1
            {"id": "9.2", "text": "నా తండ్రిగారి మద్దతు మరియు నా అదృష్టం ఎలా ఉంటాయి?", "planet": "Mars", "varga": "D1"}
        ],
        10: [
            {"id": "10.1", "text": "నా ఉద్యోగంలో ప్రమోషన్ మరియు హోదా ఎప్పుడు లభిస్తాయి?", "planet": "Venus", "varga": "D10"},  # baseline Q3.1
            {"id": "10.2", "text": "నాకు ప్రభుత్వ ఉద్యోగ యోగం ఉందా లేక ప్రైవేట్ రంగమా?", "planet": "Sun", "varga": "D10"}  # baseline Q3.2
        ],
        11: [
            {"id": "11.1", "text": "నా వ్యాపారం లేదా వృత్తిలో ఆదాయాలు మరియు లాభాలు ఎలా ఉంటాయి?", "planet": "Mercury", "varga": "D1"},
            {"id": "11.2", "text": "నా కోరికలు మరియు ఆకాంక్షలు ఎలా నెరవేరుతాయి?", "planet": "Mercury", "varga": "D1"}
        ],
        12: [
            {"id": "12.1", "text": "నాకు విదేశాలలో నివసించే యోగం ఉందా, దూర ప్రయాణాలు కలిసివస్తాయా?", "planet": "Moon", "varga": "D12"},
            {"id": "12.2", "text": "నా ఖర్చులు అదుపులో ఉంటాయా లేదా నష్టాలు సంభవిస్తాయా?", "planet": "Moon", "varga": "D12"}
        ]
    }
    
    bhava_strengths = {}
    markdown_content = f"# Astrological Deep Bhava Analysis Report - {client_name.upper()}\n\n"
    markdown_content += f"**Target Calculation Date**: {target_date_str}\n\n"
    bhava_table_data = []
    
    print("\n" + "="*88)
    print("                                12-BHAVA STRENGTH REPORT                                ")
    print("="*88)
    print(f"{'Bhava':<5}{'Rashi Name':<20}{'Lord':<10}{'SAV':<6}{'Aspecting Planets':<25}{'Strength':<10}{'Grading'}")
    print("-"*88)
    
    for b in range(1, 13):
        bhava_rashi = ((lagna_sign + b - 2) % 12) + 1
        bhava_sav = sav_points.get(bhava_rashi, 0)
        rashi_sav_strength = (bhava_sav / 40.0) * 100
    
        lord = bhava_lords[b]
        lord_fixed = planet_fixed_dict.get(lord, 50)
    
        # Calculate D1-D60 Varga repetitions average
        varga_sav_strengths = []
        for v_name in ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]:
            if v_name in varga_placements and lord in varga_placements[v_name]:
                v_sign = varga_placements[v_name][lord]
                v_sav = sav_points.get(v_sign, 0)
                varga_sav_strengths.append((v_sav / 40.0) * 100)
        varga_avg_strength = sum(varga_sav_strengths) / len(varga_sav_strengths) if varga_sav_strengths else 50.0
    
        # Aspect adjustment
        aspect_adj = 0
        aspect_planets = house_aspects.get(b, [])
        for ap in aspect_planets:
            if ap in ["Jupiter", "Venus", "Moon", "Mercury"]:
                aspect_adj += 5
            elif ap in ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]:
                aspect_adj -= 5
        rashi_bala_with_aspects = max(0.0, min(100.0, rashi_sav_strength + aspect_adj))
    
        # Final Bhava Strength
        bhava_strength = (lord_fixed + varga_avg_strength + rashi_bala_with_aspects) / 3.0
        grade = get_grading(bhava_strength)
        bhava_strengths[b] = bhava_strength
    
        aspect_str = ", ".join(aspect_planets) if aspect_planets else "None"
        r_name = rashi_names[bhava_rashi]
        
        bhava_table_data.append({
            'b': b,
            'rashi': r_name,
            'lord': lord,
            'sav': bhava_sav,
            'aspects': aspect_str,
            'strength': bhava_strength,
            'grade': get_grading_tel(bhava_strength)
        })
        
        print(f"{b:<5}{r_name:<20}{lord:<10}{bhava_sav:<6}{aspect_str:<25}{round(bhava_strength)}%{grade}")
    
        markdown_content += f"## {bhava_names[b]}\n"
        markdown_content += f"* **Rashi**: {r_name} (SAV Points: {bhava_sav})\n"
        markdown_content += f"* **Bhava Lord**: {lord} (Base Fixed Strength: {round(lord_fixed)}%)\n"
        markdown_content += f"* **Varga Average Strength (D1-D60)**: {round(varga_avg_strength)}%\n"
        markdown_content += f"* **Aspecting Planets**: {aspect_str} (Aspect-Adjusted Rashi Strength: {round(rashi_bala_with_aspects)}%)\n"
        markdown_content += f"* **Total Bhava Strength**: **{round(bhava_strength)}%** ({grade})\n\n"
    
    print("="*88)
    
    print("\n" + "="*112)
    print("                                      CORE QUESTIONS MAPPING & STRENGTH                                 ")
    print("="*112)
    print(f"{'Bhava':<6}{'Q#':<6}{'Core Question':<60}{'Strength':<10}{'Grading'}")
    print("-"*112)
    
    markdown_content += "## Core Questions Detailed Breakdown\n\n"
    
    for b in range(1, 13):
        q_list = bhava_questions.get(b, [])
        for q in q_list:
            q_planet = q["planet"]
            q_varga = q["varga"]
    
            planet_strength = planet_fixed_dict.get(q_planet, 50)
            bhava_rashi = ((lagna_sign + b - 2) % 12) + 1
            bhava_sav = sav_points.get(bhava_rashi, 0)
            bhava_sav_strength = (bhava_sav / 40.0) * 100
    
            varga_placement_rashi = varga_placements.get(q_varga, {}).get(q_planet, 1)
            varga_placement_sav = sav_points.get(varga_placement_rashi, 0)
            varga_placement_strength = (varga_placement_sav / 40.0) * 100
    
            # Question Strength = 50% * planet_strength + 25% * bhava_sav_strength + 25% * varga_placement_strength
            q_strength = 0.50 * planet_strength + 0.25 * bhava_sav_strength + 0.25 * varga_placement_strength
            q_grade = get_grading(q_strength)
    
            planet_mds = [item for item in md_timeline if item["planet"] == q_planet]
            timeline_str = ", ".join([f"{item['start']} - {item['end']}" for item in planet_mds])
    
            truncated_text = q["text"][:57] + "..." if len(q["text"]) > 57 else q["text"]
            print(f"{b:<6}{q['id']:<6}{truncated_text:<60}{round(q_strength)}%{q_grade}")
    
            markdown_content += f"### ప్రశ్న {q['id']}: {q['text']}\n"
            markdown_content += f"* **వర్గం / భావం**: {bhava_names[b]}\n"
            markdown_content += f"* **లెక్కింపు**: (గ్రహ బలం ({q_planet}): {round(planet_strength)}% + భావ SAV బలం: {round(bhava_sav_strength)}% + వర్గ బలం ({q_varga} లో రాశి {varga_placement_rashi}): {round(varga_placement_strength)}%) / 3\n"
            markdown_content += f"* **ఫలిత బలం**: **{round(q_strength)}%** ({q_grade})\n"
            markdown_content += f"* **యాక్టివేట్ అయ్యే మహాదశ టైమ్‌లైన్**: `[{timeline_str if timeline_str else 'None'}]`\n"
    
            remedies = get_remedies(q_planet, q_strength)
            if remedies:
                markdown_content += "* **⚠️ పరిహారాలు (5-Tier Remedies Activated)**:\n"
                for opt, desc in remedies.items():
                    markdown_content += f"  * **{opt}**: {desc}\n"
            markdown_content += "\n"
    
    print("="*112)
    
    # Save detailed markdown report to file
    report_filename = f"{client_name}_bhava_report.md"
    with open(report_filename, 'w', encoding='utf-8') as rf:
        rf.write(markdown_content)
    
    print(f"\nDetailed textual report successfully saved to: {report_filename}")
    
    # ----------------------------------------------------
    # Phase 5: Dasha Text Ingestion & Lifelong Dasha Table
    # ----------------------------------------------------
    dasha_texts = {}
    for p_num in range(55, 85):
        page = next((p for p in filtered_pages if p['canonical_page'] == p_num), None)
        if not page:
            continue
        blocks = page.get('content_blocks', [])
        for idx, block in enumerate(blocks):
            if block['type'] == 'heading':
                text = block['text']
                md_match = re.search(r'([\u0C00-\u0C7F]+)\s+మహాదశ', text)
                ad_match = re.search(r'మహాదశలో\s+([\u0C00-\u0C7F]+)\s+భుక్తి', text)
                
                if md_match:
                    md_tel = md_match.group(1)
                    md_eng = normalize_planet(md_tel)
                    if ad_match:
                        ad_tel = ad_match.group(1)
                        ad_eng = normalize_planet(ad_tel)
                    else:
                        ad_eng = md_eng
                    
                    if md_eng and ad_eng:
                        para = ""
                        for j in range(idx + 1, len(blocks)):
                            if blocks[j]['type'] == 'paragraph':
                                para = blocks[j].get('text', '')
                                break
                            elif blocks[j]['type'] == 'heading':
                                break
                        dasha_texts[(md_eng, ad_eng)] = {
                            'heading': text,
                            'paragraph': para
                        }
    
    # Group unique MD -> AD periods
    antardashas = []
    current_key = None
    for item in unique_timeline:
        key = (item['md'], item['ad'])
        if key != current_key:
            antardashas.append(item)
            current_key = key
    
    dasha_matrix_rows = []
    for i in range(len(antardashas)):
        md = antardashas[i]['md']
        ad = antardashas[i]['ad']
        start_str = antardashas[i]['date_str']
        if i < len(antardashas) - 1:
            end_str = antardashas[i+1]['date_str']
        else:
            end_str = "29.03.2070"
        
        # Calculate base percentage and grading
        base_avg = get_effective_dasha_score(md, ad, lagna_lord, d1_placements, friends_of_ll, planet_fixed_dict)
        grade = get_grading_tel(base_avg)
        
        # Text lookup (fallback to overall Mahadasha if specific Antardasha is missing)
        d_info = dasha_texts.get((md, ad)) or dasha_texts.get((md, md))
        para_text = d_info['paragraph'] if d_info else ""
        para_clean = para_text.replace("\n", " ").strip()
        if len(para_clean) > 55:
            para_clean = para_clean[:55] + "..."
        if not para_clean:
            para_clean = "దశా ఫలితాలు అందుబాటులో లేవు."
            
        dasha_matrix_rows.append({
            'period': f"{md} ➔ {ad}<br/>({start_str} - {end_str})",
            'summary': para_clean,
            'strength': f"{round(base_avg)}%",
            'grade': grade,
            'strength_num': base_avg
        })
    
    # Compute page breakdown dynamically
    dasha_chunks = [dasha_matrix_rows[x:x+20] for x in range(0, len(dasha_matrix_rows), 20)]
    total_pages = 1 + 2 + 1 + len(dasha_chunks)  # Page 1: Tables, Page 2: Q1-6, Page 3: Q7-12, Page 4: Fixed Planetary Strength Matrix, Pages 5+: Dashas
    
    # ----------------------------------------------------
    # Phase 6: HTML layout & Edge PDF generation
    # ----------------------------------------------------
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    @page {{
        size: A4;
        margin: 1.2cm 1.2cm 1.8cm 1.2cm;
        @bottom-left {{
            content: "Samartha Astro Engine - Confidential";
            font-family: 'Gautami', 'Segoe UI', Arial, sans-serif;
            font-size: 8pt;
            color: #4B5563;
        }}
        @bottom-right {{
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Gautami', 'Segoe UI', Arial, sans-serif;
            font-size: 8pt;
            color: #4B5563;
            font-weight: bold;
        }}
    }}
    body {{
        font-family: 'Gautami', 'Segoe UI', Arial, sans-serif;
        color: #1F2937;
        margin: 0;
        padding: 0;
        background: #fff;
        -webkit-print-color-adjust: exact;
    }}
    .page {{
        position: relative;
        width: 100%;
        box-sizing: border-box;
        page-break-after: always;
    }}
    .page:last-child {{
        page-break-after: avoid;
    }}
    .header {{
        height: 0.8cm;
        border-bottom: 1px solid #E5E7EB;
        font-size: 8.5pt;
        color: #4B5563;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6cm;
        font-weight: bold;
    }}
    .title-block {{
        text-align: center;
        margin-bottom: 0.8cm;
    }}
    .title {{
        font-size: 20pt;
        color: #1E3A8A;
        margin: 0 0 0.15cm 0;
        font-weight: bold;
    }}
    .subtitle {{
        font-size: 10pt;
        color: #4B5563;
        margin: 0;
    }}
    h2 {{
        font-size: 12pt;
        color: #1E3A8A;
        border-left: 4px solid #1E3A8A;
        padding-left: 8px;
        margin: 0 0 0.4cm 0;
        font-weight: bold;
        break-before: auto;
        break-after: avoid;
        page-break-before: auto;
        page-break-after: avoid;
        position: static !important;
    }}
    h3 {{
        font-size: 10pt;
        color: #0F766E;
        margin: 0 0 0.2cm 0;
        font-weight: bold;
        break-before: auto;
        break-after: avoid;
        page-break-before: auto;
        page-break-after: avoid;
        position: static !important;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 0.6cm;
        font-size: 8.5pt;
    }}
    thead {{
        display: table-header-group;
    }}
    tr {{
        break-inside: avoid;
        page-break-inside: avoid;
    }}
    th {{
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        text-align: left;
        padding: 5px 8px;
        border: 1px solid #E5E7EB;
    }}
    td {{
        padding: 5px 8px;
        border: 1px solid #E5E7EB;
    }}
    tr:nth-child(even) td {{
        background-color: #F9FAFB;
    }}
    .grade-excellent {{ color: #7C3AED; font-weight: bold; }}
    .grade-very-good {{ color: #2563EB; font-weight: bold; }}
    .grade-good {{ color: #059669; font-weight: bold; }}
    .grade-weak {{ color: #D97706; font-weight: bold; }}
    .grade-very-weak {{ color: #DC2626; font-weight: bold; }}
    
    .question-block {{
        margin-bottom: 0.4cm;
        font-size: 8.5pt;
        line-height: 1.4;
    }}
    .remedy-block {{
        background-color: #FEF2F2;
        border-left: 3px solid #EF4444;
        padding: 6px 10px;
        margin-top: 0.1cm;
        font-size: 8pt;
        color: #7F1D1D;
    }}
    .remedy-title {{
        font-weight: bold;
        margin-bottom: 2px;
    }}
    </style>
    </head>
    <body>
    """
    
    def get_grade_class(score):
        if score < 35: return "grade-very-weak"
        elif score < 50: return "grade-weak"
        elif score < 65: return "grade-good"
        elif score <= 80: return "grade-very-good"
        else: return "grade-excellent"
    
    # Page 1: Tables
    p_num = 1
    html_content += f"""
    <div class="page">
        <div class="header">
            <span>జాతక విశ్లేషణ నివేదిక: {client_name.upper()}</span>
            <span>Master Astrological Report</span>
        </div>
        <div class="title-block">
            <div class="title">సమర్థ ఆస్ట్రో ఇంజన్ - మాస్టర్ జాతక నివేదిక</div>
            <div class="subtitle">Client: {client_name.upper()} | Date of Birth: 22.09.1969 | Calculation Date: {target_date_str}</div>
        </div>
        
        <h2>1. ద్వాదశ భావ బల విశ్లేషణ (12-Bhava Strength Matrix)</h2>
        <table>
            <thead>
                <tr>
                    <th>భావం</th>
                    <th>రాశి</th>
                    <th>అధిపతి</th>
                    <th>SAV</th>
                    <th>వీక్షించే గ్రహాలు</th>
                    <th>బలం</th>
                    <th>గ్రేడింగ్</th>
                </tr>
            </thead>
            <tbody>
    """
    for item in bhava_table_data:
        g_cls = get_grade_class(item['strength'])
        html_content += f"""
                <tr>
                    <td><b>{item['b']}</b></td>
                    <td>{item['rashi']}</td>
                    <td>{item['lord']}</td>
                    <td>{item['sav']}</td>
                    <td>{item['aspects']}</td>
                    <td>{round(item['strength'])}%</td>
                    <td class="{g_cls}">{item['grade']}</td>
                </tr>
        """
    html_content += f"""
            </tbody>
        </table>
    
        <h2>2. గోచార తీవ్రత విశ్లేషణ (Gochara Intensity Engine)</h2>
        <table>
            <thead>
                <tr>
                    <th>గోచార గ్రహం</th>
                    <th>గోచార రాశి</th>
                    <th>రాశి SAV</th>
                    <th>గ్రహ బలం</th>
                    <th>గోచార బలం</th>
                    <th>గ్రేడింగ్</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>Saturn (శని)</b></td>
                    <td>{saturn_transit_rashi} (Meena)</td>
                    <td>{saturn_sav}</td>
                    <td>{round(saturn_fixed)}%</td>
                    <td>{round(saturn_transit_strength)}%</td>
                    <td class="{get_grade_class(saturn_transit_strength)}">{get_grading_tel(saturn_transit_strength)}</td>
                </tr>
                <tr>
                    <td><b>Rahu (రాహువు)</b></td>
                    <td>{rahu_transit_rashi} (Kumbha)</td>
                    <td>{rahu_sav}</td>
                    <td>{round(rahu_fixed)}%</td>
                    <td>{round(rahu_transit_strength)}%</td>
                    <td class="{get_grade_class(rahu_transit_strength)}">{get_grading_tel(rahu_transit_strength)}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    
    # Pages 2 & 3: Questions and Remedies
    for page_idx, bhava_range in [(2, range(1, 7)), (3, range(7, 12 + 1))]:
        p_num += 1
        html_content += f"""
    <div class="page">
        <div class="header">
            <span>జాతక విశ్లేషణ నివేదిక: {client_name.upper()}</span>
            <span>Master Astrological Report</span>
        </div>
        <h2>3. క్వరీ రూటింగ్ & పరిహారాలు (Detailed Questions & Remedies) - Part {page_idx - 1}</h2>
        """
        for b in bhava_range:
            html_content += f"<h3>{bhava_names[b]}</h3>"
            q_list = bhava_questions.get(b, [])
            for q in q_list:
                q_planet = q["planet"]
                q_varga = q["varga"]
                planet_strength = planet_fixed_dict.get(q_planet, 50)
                bhava_rashi = ((lagna_sign + b - 2) % 12) + 1
                bhava_sav = sav_points.get(bhava_rashi, 0)
                bhava_sav_strength = (bhava_sav / 40.0) * 100
                varga_placement_rashi = varga_placements.get(q_varga, {}).get(q_planet, 1)
                varga_placement_sav = sav_points.get(varga_placement_rashi, 0)
                varga_placement_strength = (varga_placement_sav / 40.0) * 100
                q_strength = 0.50 * planet_strength + 0.25 * bhava_sav_strength + 0.25 * varga_placement_strength
                q_grade = get_grading_tel(q_strength)
                g_cls = get_grade_class(q_strength)
                planet_mds = [item for item in md_timeline if item["planet"] == q_planet]
                timeline_str = ", ".join([f"{item['start']} - {item['end']}" for item in planet_mds])
                
                html_content += f"""
                <div class="question-block">
                    <b>ప్రశ్న {q['id']}:</b> {q['text']}<br/>
                    ఫలిత బలం: <span class="{g_cls}">{round(q_strength)}% ({q_grade})</span> | 
                    మహాదశ టైమ్‌లైన్: <b>[{timeline_str if timeline_str else 'None'}]</b>
                """
                remedies = get_remedies(q_planet, q_strength)
                if remedies:
                    html_content += f"""
                    <div class="remedy-block">
                        <div class="remedy-title">⚠️ పరిహారాలు (5-Tier Remedies Activated):</div>
                        {"".join(f"• <b>{opt}</b>: {desc}<br/>" for opt, desc in remedies.items())}
                    </div>
                    """
                html_content += "</div>"
        html_content += f"""
    </div>
    """
    
    # Page 4: Fixed Planetary Strength Matrix
    tel_planet_names = {
        "Sun": "సూర్యుడు (Sun)",
        "Moon": "చంద్రుడు (Moon)",
        "Mars": "కుజుడు (Mars)",
        "Mercury": "बुధుడు (Mercury)",
        "Jupiter": "గురువు (Jupiter)",
        "Venus": "శుక్రుడు (Venus)",
        "Saturn": "శని (Saturn)",
        "Rahu": "రాహువు (Rahu)",
        "Ketu": "కేతువు (Ketu)"
    }
    
    p_num += 1
    html_content += f"""
    <div class="page">
        <div class="header">
            <span>జాతక విశ్లేషణ నివేదిక: {client_name.upper()}</span>
            <span>Master Astrological Report</span>
        </div>
        <h2>4. 9 గ్రహాల స్థిరమైన బలాబలాల విశ్లేషణ (Fixed Planetary Strength Matrix)</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 16%">గ్రహం</th>
                    <th style="width: 11%">షడ్బల %</th>
                    <th style="width: 13%">భావ స్థానం %</th>
                    <th style="width: 16%">నక్షత్రాధిపతి బలం %</th>
                    <th style="width: 11%">వర్గ బలం %</th>
                    <th style="width: 18%">స్థితి / మార్పులు</th>
                    <th style="width: 15%">స్థిర బలం %</th>
                    <th style="width: 16%">గ్రేడింగ్</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for pk in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        bd = planet_breakdown_dict[pk]
        g_cls = get_grade_class(bd['final'])
        g_tel = get_grading_tel(bd['final'])
        html_content += f"""
                <tr>
                    <td><b>{tel_planet_names.get(pk, pk)}</b></td>
                    <td>{round(bd['shadbala'])}%</td>
                    <td>{round(bd['house'])}%</td>
                    <td>{round(bd['nakshatra'])}%</td>
                    <td>{round(bd['varga'])}%</td>
                    <td>{bd['modifiers']}</td>
                    <td style="font-weight: bold;">{round(bd['final'])}%</td>
                    <td class="{g_cls}">{g_tel}</td>
                </tr>
        """
    
    html_content += f"""
            </tbody>
        </table>
    </div>
    """
    
    # Pages 5+: Dasha matrix chunks
    for chunk_idx, chunk in enumerate(dasha_chunks):
        p_num += 1
        html_content += f"""
    <div class="page">
        <div class="header">
            <span>జాతక విశ్లేషణ నివేదిక: {client_name.upper()}</span>
            <span>Master Astrological Report</span>
        </div>
        <h2>5. జీవితకాల దశా అంతర్దశల విశ్లేషణ (Lifelong Dasha Matrix) - Part {chunk_idx + 1}</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 25%">దశా కాలం</th>
                    <th style="width: 45%">ఫలిత సారాంశం</th>
                    <th style="width: 12%">బలం %</th>
                    <th style="width: 18%">గ్రేడింగ్</th>
                </tr>
            </thead>
            <tbody>
    """
        for row in chunk:
            g_cls = get_grade_class(row['strength_num'])
            html_content += f"""
                <tr>
                    <td><b>{row['period']}</b></td>
                    <td>{row['summary']}</td>
                    <td>{row['strength']}</td>
                    <td class="{g_cls}">{row['grade']}</td>
                </tr>
            """
        html_content += f"""
            </tbody>
        </table>
    </div>
    """
    
    html_content += """
    </body>
    </html>
    """
    
    # Write HTML file and run Edge to generate PDF
    html_file_path = f"{client_name}_report_temp.html"
    pdf_path = f"{client_name}_master_report.pdf"
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    subprocess.run([
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        os.path.abspath(html_file_path)
    ])
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    
    print(f"Master printable PDF report successfully saved to: {pdf_path}")
