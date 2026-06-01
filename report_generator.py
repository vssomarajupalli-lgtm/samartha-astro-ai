# -*- coding: utf-8 -*-
import json
from parser import SamarthaAstroEngine
from query_engine import SamarthaQueryEngine

def generate_html_report(output_filename="test_print.html", gender="Male"):
    # 1. కోర్ ఇంజన్లను మరియు నిజమైన జేసన్ డేటాను లోడ్ చేయడం
    astro_engine = SamarthaAstroEngine("raju_canonical_content.json")
    query_engine = SamarthaQueryEngine(graha_bala_engine=astro_engine)
    
    # 2. దశా మరియు శని గోచార లెక్కలను సేకరించడం
    dasha_triad = astro_engine.get_vimshottari_triad()
    sade_sati_status = astro_engine.calculate_pada_sade_sati()
    final_scores = query_engine.evaluate_all_queries(gender=gender)
    
    # 3. హై-క్వాలిటీ ప్రొఫెషనల్ HTML & CSS టెంప్లేట్ డిజైన్ (ప్రింట్-ఫ్రెండ్లీ)
    html_content = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>సమర్థవాస్తు - జ్యోతిష్య నివేదిక</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            color: #333;
            background-color: #fff;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px double #b38600;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #b38600;
            margin: 0;
            font-size: 32px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            font-size: 14px;
            color: #666;
            letter-spacing: 1px;
        }}
        .section-title {{
            background-color: #f9f5e8;
            color: #b38600;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            border-left: 5px solid #b38600;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #b38600;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .score-badge {{
            display: inline-block;
            padding: 5px 10px;
            font-weight: bold;
            border-radius: 4px;
            color: white;
        }}
        .high-score {{ background-color: #2e7d32; }}
        .med-score {{ background-color: #f57c00; }}
        .low-score {{ background-color: #d32f2f; }}
        
        /* ప్రింట్ సెట్టింగ్స్ - పేజీ బ్రేక్ అవ్వకుండా రక్షణ */
        @media print {{
            body {{ margin: 20px; }}
            .section-title {{ page-break-after: avoid; }}
            tr {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>

    <div class="header">
        <h1>సమర్థవాస్తు</h1>
        <p>ఆస్ట్రో-AI కంప్యూటేషనల్ లైవ్ ప్రెడిక్షన్ రిపోర్ట్</p>
    </div>

    <div class="section-title">1. ప్రస్తుత త్రిశిర దశా కాలక్రమం</div>
    <table>
        <thead>
            <tr>
                <th>మహర్దశ నాథుడు</th>
                <th>అంతర్దశ నాథుడు</th>
                <th>प्रत्यంతర్దశ నాథుడు</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{dasha_triad['Mahadasha_Lord']}</td>
                <td>{dasha_triad['Antardasha_Lord']}</td>
                <td>{dasha_triad['Pratyantardasha_Lord']}</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2. నక్షత్ర పాద ఏలినాటి శని గోచార తీవ్రత పరిశీలన</div>
    <table>
        <thead>
            <tr>
                <th>గోచార శని స్థితి</th>
                <th>ప్రస్తుత తీవ్రత క్షేత్రం</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{"యాక్టివ్ లో ఉంది" if sade_sati_status['Sade_Sati_Active'] else "సాధారణ గోచారం"}</td>
                <td style="font-weight: bold; color: #d32f2f;">{sade_sati_status['Transit_Intensity_Level']}</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">3. నూతన 40:30:30 వెయిటేజీ ఫార్ములా ఆధారిత ప్రశ్నల సంభావ్యత ఫలితాలు</div>
    <p style="font-size: 13px; color: #555;">
        * గమనిక: D1 భావాధిపతికి 40%, కారక గ్రహానికి 30%, మరియు షోడశ వర్గాల బలానికి (D9 + నిర్దిష్ట వర్గం + వింశోపాక) 30% వెయిటేజీతో లెక్కించబడిన నిశ్చయ బలం ఇది.
    </p>
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
    
    # ప్రశ్నల తెలుగు డిస్క్రిప్షన్స్ మ్యాపింగ్ (రిపోర్ట్ లో అందంగా కనిపించడానికి)
    question_desc = {
        "Q1": "నా ఆయుష్షు దీర్ఘంగా ఉంటుందా?",
        "Q2": "నా శరీరం ఆరోగ్యంగా ఉంటుందా?",
        "Q5": "నేను ధనవంతుడిని అవుతానా / ఆర్థిక స్థితి ఎలా ఉంటుంది?",
        "Q6": "నాకు గృహ/కుటుంబ సౌఖ్యం మరియు శాంతి లభిస్తుందా?",
        "Q14": "నేను సొంత ఇల్లు కట్టగలనా / ఎప్పుడు కొనుగోలు చేస్తాను?",
        "Q16": "నేను కొత్త వాహనం కొనగలనా?",
        "Q19": "నాకు సంతాన యోగం ఎప్పుడు కలుగుతుంది?",
        "Q23": "నేను హయ్యర్ ఎడ్యుకేషన్ (ఉన్నత విద్య) సాధించగలనా?",
        "Q26": "నా శరీరంలో వచ్చే ప్రధాన అనారోగ్య సమస్యలు ఏమిటి?",
        "Q31": "నా వివాహం ఎప్పుడు జరుగుతుంది? ఆలస్యంగానా లేక త్వరగానా?",
        "Q40": "నేను వ్యాపారంలో భాగస్వామితో విజయం పొందగలనా?",
        "Q41": "నా జీవితంలో పెద్ద ఆర్థిక నష్టం వచ్చే అవకాశం ఉందా?",
        "Q46": "నా జీవితంలో అసలైన అదృష్టం / భాగ్యోదయం ఎప్పుడు కలుగుతుంది?",
        "Q50": "నా ఉద్యోగ/వ్యాపారంలో ప్రమోషన్ ఎప్పుడు ఉంటుంది?",
        "Q51": "నాకు ప్రభుత్వ ఉద్యోగం వచ్చే అవకాశం ఉందా?",
        "Q53": "నా స్వంత వ్యాపారం సక్సెస్ అవుతానా?",
        "Q67": "నేను రాజకీయాల్లో ప్రవేశించగలనా / నాకు రాజకీయం సరిపడుతుందా?",
        "Q68": "నేను ఎన్నికలలో పోటీ చేస్తే గెలుస్తానా?",
        "Q72": "నాకు పెద్ద మొత్తంలో ఆదాయ మార్గాలు, లాభాలు వస్తాయా?",
        "Q76": "నేను విదేశాలకు వెళ్లడమే కాకుండా అక్కడే శాశ్వతంగా స్థిరపడగలనా?",
        "Q83": "నా గత జన్మ ఏమిటి — నేను ఏ యోనిలో జన్మించాను?",
        "Q85": "నేను గత జన్మలో ఏయే ప్రధాన పాపాలు చేశాను?"
    }

    # లూప్ ద్వారా టేబుల్ రోస్ ని జనరేట్ చేయడం
    for q_id, score in final_scores.items():
        desc = question_desc.get(q_id, "జ్యోతిష్య ప్రశ్న విశ్లేషణ")
        
        # స్కోరు తీవ్రతను బట్టి కలర్ బ్యాడ్జ్ నిర్ణయించడం
        if score >= 75:
            badge_class = "high-score"
        elif score >= 50:
            badge_class = "med-score"
        else:
            badge_class = "low-score"
            
        html_content += f"""
            <tr>
                <td>style="font-weight: bold;"{q_id}</td>
                <td>{desc}</td>
                <td><span class="score-badge {badge_class}">{score}%</span></td>
            </tr>"""

    html_content += """
        </tbody>
    </table>

</body>
</html>
    """
    
    # 4. ఫైల్ ను రైట్ చేయడం
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"🎉 విజయవంతంగా రిపోర్ట్ జనరేట్ అయింది! ఫైల్ పేరు: {output_filename}")
    except Exception as e:
        print(f"⚠️ HTML ఫైల్ సేవ్ చేయడంలో లోపం: {e}")

if __name__ == "__main__":
    generate_html_report()