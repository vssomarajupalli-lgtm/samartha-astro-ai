# -*- coding: utf-8 -*-
import json
import traceback
from parser import SamarthaAstroEngine
from query_engine import SamarthaQueryEngine

def generate_html_report(output_filename="test_print.html", gender="Male"):
    try:
        # 1. కోర్ ఇంజన్లను లోడ్ చేయడం
        astro_engine = SamarthaAstroEngine("raju_canonical_content.json")
        query_engine = SamarthaQueryEngine(graha_bala_engine=astro_engine)
        
        # 2. దశా పీరియడ్స్ మరియు శని గోచార డేటాను సేకరించడం
        dasha_triad = astro_engine.get_vimshottari_triad()
        sade_sati_status = astro_engine.calculate_pada_sade_sati()
        final_scores = query_engine.evaluate_all_queries(gender=gender)
        
        # జేసన్ నుండి దశా పీరియడ్స్ డేటాను డైనమిక్ గా లాగడం (లేకపోతే జాతక వెరిఫైడ్ టైమ్‌లైన్ ఫాల్‌బ్యాక్)
        md_period = astro_engine.data.get("mahadasha_period", "2018-06-20 నుండి 2034-06-20 వరకు")
        ad_period = astro_engine.data.get("antardasha_period", "2023-12-15 నుండి 2026-08-30 వరకు")
        pd_period = astro_engine.data.get("pratyantardasha_period", "2026-03-01 నుండి 2026-07-15 వరకు")
        
        # 3. హై-క్వాలిటీ ప్రొఫెషనల్ HTML & CSS టెంప్లేట్ డిజైన్
        html_content = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>సమర్థవాస్తు - జ్యోతిష్య నివేదిక</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #333; background-color: #fff; }}
        .header {{ text-align: center; border-bottom: 3px double #b38600; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #b38600; margin: 0; font-size: 32px; }}
        .header p {{ margin: 5px 0 0 0; font-size: 14px; color: #666; }}
        .section-title {{ background-color: #f9f5e8; color: #b38600; padding: 10px; font-size: 18px; font-weight: bold; border-left: 5px solid #b38600; margin-top: 30px; margin-bottom: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #b38600; color: white; font-size: 15px; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .score-badge {{ display: inline-block; padding: 5px 10px; font-weight: bold; border-radius: 4px; color: white; min-width: 50px; text-align: center; }}
        .high-score {{ background-color: #2e7d32; }}
        .med-score {{ background-color: #f57c00; }}
        .low-score {{ background-color: #b71c1c; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>సమర్థవాస్తు</h1>
        <p>ఆస్ట్రో-AI కంప్యూటేషనల్ లైవ్ ప్రెడిక్షన్ రిపోర్ట్</p>
    </div>

    <div class="section-title">1. ప్రస్తుత త్రిశిర దశా కాలక్రమం & కాలపరిమితి</div>
    <table>
        <thead>
            <tr>
                <th>దశా విభాగం</th>
                <th>దశా నాథుడు (Lord)</th>
                <th>ప్రస్తుత కాలపరిమితి (Time Period)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight: bold; color: #b38600;">మహర్దశ</td>
                <td style="font-weight: bold;">{dasha_triad['Mahadasha_Lord']}</td>
                <td>{md_period}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #b38600;">అంతర్దశ</td>
                <td style="font-weight: bold;">{dasha_triad['Antardasha_Lord']}</td>
                <td>{ad_period}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #b38600;">प्रत्यంతర్దశ</td>
                <td style="font-weight: bold;">{dasha_triad['Pratyantardasha_Lord']}</td>
                <td>{pd_period}</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2. నక్షత్ర పాద ఏలినాటి శని గోచార తీవ్రత పరిశీలన</div>
    <table>
        <thead>
            <tr>
                <th>గోచార శని స్థితి</th>
                <th>ప్రస్తుత తీవ్రత క్షేత్రం</th>
                <th>ప్రభావ కాలం</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{"యాక్టివ్ లో ఉంది" if sade_sati_status['Sade_Sati_Active'] else "సాధారణ గోచారం"}</td>
                <td style="font-weight: bold; color: #b71c1c;">{sade_sati_status['Transit_Intensity_Level']}</td>
                <td>ప్రస్తుత రన్-టైమ్ పరిధి (2025 నుండి 2028 వరకు)</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">3. నూతన 40:30:30 వెయిటేజీ ఫార్ములా ఆధారిత ప్రశ్నల సంభావ్యత ఫలితాలు</div>
    <table>
        <thead>
            <tr>
                <th>ప్రశ్న ఐడి</th>
                <th>జీవిత ప్రశ్న వివరాలు</th>
                <th>నిశ్చయ బలం (సంభావ్యత)</th>
            </tr>
        </thead>
        <tbody>
        """
        
        question_desc = {
            "Q1": "నా ఆయుష్షు దీర్ఘంగా ఉంటుందా?", "Q2": "నా శరీరం ఆరోగ్యంగా ఉంటుందా?",
            "Q5": "నేను ధనవంతుడిని అవుతానా / ఆర్థిక స్థితి ఎలా ఉంటుంది?", "Q6": "నాకు గృహ/కుటుంబ సౌఖ్యం మరియు శాంతి లభిస్తుందా?",
            "Q14": "నేను సొంత ఇల్లు కట్టగలనా / ఎప్పుడు కొనుగోలు చేస్తాను?", "Q16": "నేను కొత్త वाहनం కొనగలనా?",
            "Q19": "నాకు సంతాన యోగం ఎప్పుడు కలుగుతుంది?", "Q23": "నేను హయ్యర్ ఎడ్యుకేషన్ (ఉన్నత విద్య) సాధించగలనా?",
            "Q26": "నా శరీరంలో వచ్చే ప్రధాన అనారోగ్య సమస్యలు ఏమిటి?", "Q31": "నా వివాహం ఎప్పుడు జరుగుతుంది? ఆలస్యంగానా లేక త్వరగానా?",
            "Q40": "నేను వ్యాపారంలో భాగస్వామితో విజయం పొందగలనా?", "Q41": "నా జీవితంలో పెద్ద ఆర్థిక నష్టం వచ్చే అవకాశం ఉందా?",
            "Q46": "నా జీవితంలో అసలైన అదృష్టం / భాగ్యోదయం ఎప్పుడు కలుగుతుంది?", "Q50": "నా ఉద్యోగ/వ్యాపారంలో ప్రమోషన్ ఎప్పుడు ఉంటుంది?",
            "Q51": "నాకు ప్రభుత్వ ఉద్యోగం వచ్చే అవకాశం ఉందా?", "Q53": "నా స్వంత వ్యాపారం సక్సెస్ అవుతానా?",
            "Q67": "నేను రాజకీయాల్లో ప్రవేశించగలనా / నాకు రాజకీయం సరిపడుతుందా?", "Q68": "నేను ఎన్నికలలో పోటీ చేస్తే గెలుస్తానా?",
            "Q72": "నాకు పెద్ద మొత్తంలో ఆదాయ మార్గాలు, లాభాలు వస్తాయా?", "Q76": "నేను విదేశాలకు వెళ్లడమే కాకుండా అక్కడే శాశ్వతంగా స్థిరపడగలనా?",
            "Q83": "నా గత జన్మ ఏమిటి — నేను ఏ యనిలో జన్మించాను?", "Q85": "నేను గత జన్మలో ఏయే ప్రధాన పాపాలు చేశాను?"
        }

        for q_id, score in final_scores.items():
            desc = question_desc.get(q_id, "జ్యోతిష్య ప్రశ్న విశ్లేషణ")
            badge_class = "high-score" if score >= 75 else ("med-score" if score >= 50 else "low-score")
            
            html_content += f"""
                <tr>
                    <td style="font-weight: bold; color: #b38600;">{q_id}</td>
                    <td>{desc}</td>
                    <td><span class="score-badge {badge_class}">{score}%</span></td>
                </tr>"""

        html_content += """
        </tbody>
    </table>
</body>
</html>"""
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"🎉 విజయవంతంగా రిపోర్ట్ జనరేట్ అయింది! ఫైల్ పేరు: {output_filename}")
        
    except Exception as e:
        print(f"⚠️ రన్ టైమ్ లో తీవ్రమైన లోపం వచ్చింది సార్:")
        traceback.print_exc()

if __name__ == "__main__":
    generate_html_report()