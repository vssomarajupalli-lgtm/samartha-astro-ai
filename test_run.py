# -*- coding: utf-8 -*-
from parser import SamarthaAstroEngine
from query_engine import SamarthaQueryEngine

def main():
    print("==================================================")
    print("   SAMARTHA ASTRO AI - LIVE COMPUTATION RUN       ")
    print("==================================================")

    # 1. కోర్ మ్యాథ్ ఇంజన్ ని ప్రారంభించడం
    # (నిజమైన రన్ లో ఇక్కడ _canonical_content.json డేటాను పాస్ చేస్తాము)
    mock_json_data = {
        "current_mahadasha": "Jupiter",
        "current_antardasha": "Saturn",
        "current_pratyantardasha": "Mercury"
    }
    astro_engine = SamarthaAstroEngine(json_file_path="raju_canonical_content.json")

    # 2. ప్రశ్నావళి ప్రెడిక్షన్ ఇంజన్ ని అనుసంధానించడం
    query_engine = SamarthaQueryEngine(graha_bala_engine=astro_engine)

    # 3. దశా టైమ్ లైన్ త్రిశిర పట్టికను ప్రింట్ చేయడం
    dasha_triad = astro_engine.get_vimshottari_triad()
    print("\n[1] ప్రస్తుత త్రిశిర దశా కాలక్రమం:")
    print(f"  -> మహర్దశ నాథుడు: {dasha_triad['Mahadasha_Lord']}")
    print(f"  -> అంతర్దశ నాథుడు: {dasha_triad['Antardasha_Lord']}")
    print(f"  -> प्रत्यంతర్దశ నాథుడు: {dasha_triad['Pratyantardasha_Lord']}")

    # 4. నక్షత్ర పాద ఏలినాటి శని గోచార తీవ్రత పరీక్ష (ఉదాహరణకు నూతన చంద్ర డిగ్రీ 280° తో)
    # మకర రాశి ధనిష్ట 2వ పాదం రఫ్ గా 280 డిగ్రీల వద్ద ఉంటుంది
    sade_sati_status = astro_engine.calculate_pada_sade_sati(natal_moon_degree=280.0, transit_saturn_degree=282.5)
    print("\n[2] నక్షత్ర పాద ఏలినాటి శని గోచార స్థితి:")
    print(f"  -> యాక్టివ్ గా ఉందా?: {sade_sati_status['Sade_Sati_Active']}")
    print(f"  -> ప్రస్తుత తీవ్రత క్షేత్రం: {sade_sati_status['Transit_Intensity_Level']}")

    # 5. 40:30:30 మాస్టర్ ఫార్ములా ద్వారా ప్రశ్నల ఫలితాల లెక్కింపు (Male జాతకం కొరకు)
    print("\n[3] 40:30:30 వెయిటేజీ ఫార్ములా ఆధారిత ప్రశ్నల స్కోర్లు (Out of 100):")
    final_report = query_engine.evaluate_all_queries(gender="Male")
    
    for q_id, score in final_report.items():
        print(f"  * ప్రశ్న {q_id} నిశ్చయ బలం మరియు సంభావ్యత: {score}%")
    
    print("\n==================================================")
    print("         COMPUTATION COMPLETED SUCCESSFULLY       ")
    print("==================================================")

if __name__ == "__main__":
    main()