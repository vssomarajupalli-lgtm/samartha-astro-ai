# -*- coding: utf-8 -*-
from base_parser import SamarthaBaseParser
from dasha_engine import SamarthaDashaEngine
from query_engine import SamarthaQueryEngine

def build_and_run_report():
    print("⚡ సమర్థ ఆస్ట్రో-AI మ్యాక్సిమమ్ ఆప్టిమైజ్డ్ పైప్‌లైన్ రన్ అవుతోంది...")
    
    parser = SamarthaBaseParser()
    dasha_engine = SamarthaDashaEngine(parser)
    query_engine = SamarthaQueryEngine(parser)
    
    # డేటా స్కాన్
    client_name = parser.client_name
    dob = parser.dob
    lagna = parser.lagna
    gochara = parser.get_gochara_status()
    shani_periods = parser.elinati_shani_periods
    
    dasha_tree = dasha_engine.build_tree_layout()
    query_grid = query_engine.build_query_grid()
    
    # ఏలినాటి శని హెచ్‌టిఎమ్‌ఎల్ తయారీ
    shani_html = "<table class='master-table'><thead><tr><th>శని పరివర్తన చక్రం</th><th>ఏలినాటి శని దశ శీర్షిక</th><th>కచ్చితమైన సమయ పరిధి</th><th>గోచార జీవిత ప్రభావం</th></tr></thead><tbody>"
    for item in shani_periods:
        shani_html += f"<tr><td style='font-weight:bold;'>{item['cycle']}</td><td style='color:#b71c1c; font-weight:bold;'>{item['phase']}</td><td>{item['span']}</td><td>{item['impact']}</td></tr>"
    shani_html += "</tbody></table>"
    
    html_content = f"""<!DOCTYPE html>
<html lang='te'>
<head>
    <meta charset='UTF-8'>
    <title>SAMARTHA MASTER REPORT</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; }}
        .header {{ text-align: center; border-bottom: 4px double #b38600; padding-bottom: 15px; margin-bottom: 30px; }}
        .header h1 {{ color: #b38600; margin: 0; font-size: 34px; }}
        .profile-box {{ background-color: #fdfbf7; border: 1px solid #e6dbb8; padding: 15px; border-radius: 6px; margin-bottom: 25px; display: flex; justify-content: space-around; }}
        .section-title {{ background-color: #fdfae6; color: #b38600; padding: 12px; font-size: 18px; font-weight: bold; border-left: 6px solid #b38600; margin-top: 35px; margin-bottom: 15px; }}
        
        .master-table, .tree-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
        .master-table th, .master-table td, .tree-table th, .tree-table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        .master-table th, .tree-table th {{ background-color: #b38600; color: white; }}
        
        .row-md {{ background-color: #f7f3e1; font-weight: bold; color: #b38600; }}
        .row-ad {{ background-color: #fafafa; font-weight: bold; }}
        .row-pd {{ background-color: #ffffff; font-size: 13px; color: #444; }}
        .indent-ad {{ padding-left: 25px !important; }}
        .indent-pd {{ padding-left: 50px !important; }}
        .fixed-strength {{ font-weight: bold; color: #2e7d32; text-align: right; }}
        
        .score-badge {{ display: inline-block; padding: 4px 8px; font-weight: bold; border-radius: 4px; color: white; min-width: 50px; text-align: center; }}
        .high-score {{ background-color: #2e7d32; }} .med-score {{ background-color: #ef6c00; }} .low-score {{ background-color: #c62828; }}
        
        thead {{ display: table-header-group; }}
        tr {{ page-break-inside: avoid; }}
        @media print {{
            body {{ margin: 20px; font-size: 12px; }}
            .section-title {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>

    <div class='header'>
        <h1>సమర్థవాస్తు</h1>
        <p>ఆస్ట్రో-AI నిఖర కంప్యూటేషనల్ మాస్టర్ నివేదిక (40:30:15:10:5 Model)</p>
    </div>

    <div class='profile-box'>
        <div><b>జాతకుడు:</b> {client_name}</div>
        <div><b>సవరించిన DOB:</b> {dob}</div>
        <div><b>లగ్న స్థానం:</b> {lagna} లగ్నం</div>
    </div>

    <div class='section-title'>I. గోచార గ్రహ తీవ్రత పరిశీలన పట్టిక (Unaltered Base)</div>
    <table class='master-table'>
        <thead>
            <tr><th>గోచార గ్రహం</th><th>గోచార రాశి</th><th>SAV స్కోర్</th><th>బేస్ బలం</th><th>గోచార ఫలిత బలం</th></tr>
        </thead>
        <tbody>
            <tr><td>Saturn (శని)</td><td>{gochara['Saturn']['rasi']}</td><td>{gochara['Saturn']['sav']}</td><td>{gochara['Saturn']['base']}%</td><td style='font-weight:bold; color:#b38600;'>{gochara['Saturn']['intensity']}%</td></tr>
            <tr><td>Rahu (రాహువు)</td><td>{gochara['Rahu']['rasi']}</td><td>{gochara['Rahu']['sav']}</td><td>{gochara['Rahu']['base']}%</td><td style='font-weight:bold; color:#b38600;'>{gochara['Rahu']['intensity']}%</td></tr>
        </tbody>
    </table>

    <div class='section-title'>II. ఏలినాటి శని త్రి-చక్ర జీవితకాల కాలక్రమ పరిశీలన (Sade Sati Timeline)</div>
    {shani_html}

    <div class='section-title'>III. జీవితకాల దశా-అంతర్దశ-प्रत्यంతర్దశ కాలక్రమ వృక్షం & (MD+AD+PD)/3 సగటు బలాలు</div>
    {dasha_tree}

    <div class='section-title'>IV. నూతన 40:30:15:10:5 వెయిటేజీ ఫార్ములా ఆధారిత అసలైన ప్రశ్నల సంభావ్యత గ్రిడ్</div>
    {query_grid}

</body>
</html>"""

    with open("test_print.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("🎉 మూడు ఇష్యూస్ విజయవంతంగా పరిష్కరించబడ్డాయి సార్! ఫైల్ పేరు: test_print.html")

if __name__ == "__main__":
    build_and_run_report()