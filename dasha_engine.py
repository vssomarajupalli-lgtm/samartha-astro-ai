# -*- coding: utf-8 -*-
import math

class SamarthaDashaEngine:
    def __init__(self, base_parser):
        self.parser = base_parser

    def get_lifelong_timeline_matrix(self):
        return [
            {
                "md_lord": "Saturn", "md_telugu": "శని", "span": "29.05.2008 నుండి 29.05.2027",
                "antardashas": [
                    {
                        "ad_lord": "Jupiter", "ad_telugu": "గురు", "span": "14.03.2023 నుండి 29.05.2027",
                        "pds": [
                            {"pd_lord": "Jupiter", "span": "14.03.2023 నుండి 15.07.2023"},
                            {"pd_lord": "Saturn", "span": "15.07.2023 నుండి 08.12.2023"},
                            {"pd_lord": "Mercury", "span": "08.12.2023 నుండి 17.04.2024"},
                            {"pd_lord": "Ketu", "span": "17.04.2024 నుండి 10.06.2024"},
                            {"pd_lord": "Venus", "span": "10.06.2024 నుండి 11.11.2024"},
                            {"pd_lord": "Sun", "span": "11.11.2024 నుండి 27.12.2024"},
                            {"pd_lord": "Moon", "span": "27.12.2024 నుండి 14.03.2025"},
                            {"pd_lord": "Mars", "span": "14.03.2025 నుండి 07.05.2025"},
                            {"pd_lord": "Rahu", "span": "07.05.2025 నుండి 29.05.2027"}
                        ]
                    }
                ]
            },
            {
                "md_lord": "Mercury", "md_telugu": "బుధ", "span": "29.05.2027 నుండి 29.05.2044",
                "antardashas": [
                    {
                        "ad_lord": "Mercury", "ad_telugu": "బుధ", "span": "29.05.2027 నుండి 25.10.2029",
                        "pds": [
                            {"pd_lord": "Mercury", "span": "29.05.2027 నుండి 24.09.2027"},
                            {"pd_lord": "Ketu", "span": "24.09.2027 నుండి 15.11.2027"},
                            {"pd_lord": "Venus", "span": "15.11.2027 నుండి 10.04.2028"},
                            {"pd_lord": "Sun", "span": "10.04.2028 నుండి 24.05.2028"},
                            {"pd_lord": "Moon", "span": "24.05.2028 నుండి 05.08.2028"},
                            {"pd_lord": "Mars", "span": "05.08.2028 నుండి 26.09.2028"},
                            {"pd_lord": "Rahu", "span": "26.09.2028 నుండి 05.02.2029"},
                            {"pd_lord": "Jupiter", "span": "05.02.2029 నుండి 03.06.2029"},
                            {"pd_lord": "Saturn", "span": "03.06.2029 నుండి 25.10.2029"}
                        ]
                    }
                ]
            }
        ]

    def build_tree_layout(self):
        matrix = self.get_lifelong_timeline_matrix()
        html = "<table class='tree-table'><thead><tr><th>దశా క్రమానుగతం (MD - AD - PD)</th><th>సమయ పరిధి (d-m-y Format)</th><th style='text-align:right;'>సంయుక్త ఫలిత బలం</th></tr></thead><tbody>"
        
        for md in matrix:
            md_strength = self.parser.get_planet_strength(md['md_lord'])
            html += f"<tr class='row-md'><td>🔱 {md['md_telugu']} మహాదశ</td><td>{md['span']}</td><td class='fixed-strength'>{md_strength}%</td></tr>"
            
            for ad in md['antardashas']:
                ad_lord = ad['ad_lord']
                ad_strength = self.parser.get_planet_strength(ad_lord)
                ad_score = math.ceil((md_strength + ad_strength) / 2.0)
                
                html += f"<tr class='row-ad'><td class='indent-ad'>🔸 {ad['ad_telugu']} అంతర్దశ</td><td>{ad['span']}</td><td class='fixed-strength'>{ad_score}%</td></tr>"
                
                for pd in ad['pds']:
                    pd_lord = pd['pd_lord']
                    pd_span = pd['span']
                    pd_strength = self.parser.get_planet_strength(pd_lord)
                    
                    # స్వచ్ఛమైన తెలుగు పేరు లుకప్
                    telugu_planet_name = self.parser.planet_telugu.get(pd_lord, pd_lord)
                    
                    # (MD + AD + PD) / 3 సగటు సూత్రం
                    pd_final_score = math.ceil((md_strength + ad_strength + pd_strength) / 3.0)
                    
                    html += f"<tr class='row-pd'><td class='indent-pd'>• {telugu_planet_name} ప్రత్యంతర దశ</td><td>{pd_span}</td><td class='fixed-strength'>{pd_final_score}%</td></tr>"
                    
        html += "</tbody></table>"
        return html