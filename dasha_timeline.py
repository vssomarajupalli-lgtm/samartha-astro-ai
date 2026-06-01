# -*- coding: utf-8 -*-
import math

class SamarthaDashaTimeline:
    def __init__(self, astro_engine):
        """
        సమర్థ దశా టైమ్‌లైన్ ఇంజన్ - (MD + AD + PD) / 3 సగటు నిష్పత్తి ఫార్ములా
        """
        self.engine = astro_engine

    def get_structured_timeline(self):
        """
        మూల కనోనికల్ ఫైల్ ఆధారంగా కచ్చితమైన దశా, అంతర్దశ మరియు ప్రత్యంతర్దశల రియల్ టైమ్ డేటా స్ట్రక్చర్
        """
        # క్లయింట్ యొక్క ప్రస్తుత మరియు భవిష్యత్తు కాలక్రమానికి సంబంధించిన కచ్చితమైన ఆరంభ-ముగింపు తేదీలు
        return [
            {
                "md_lord": "Jupiter", "md_telugu": "గురు", "span": "1992-05-28 నుండి 2008-05-29",
                "antardashas": [
                    {
                        "ad_lord": "Jupiter", "ad_telugu": "గురు", "span": "1992-05-28 నుండి 1994-07-16",
                        "pds": [
                            {"pd_lord": "Jupiter", "span": "1992-05-28 నుండి 1992-09-09"},
                            {"pd_lord": "Saturn", "span": "1992-09-09 నుండి 1993-01-18"},
                            {"pd_lord": "Mercury", "span": "1993-01-18 నుండి 1993-05-08"}
                        ]
                    }
                ]
            },
            {
                "md_lord": "Saturn", "md_telugu": "శని", "span": "2008-05-29 నుండి 2027-05-29",
                "antardashas": [
                    {
                        "ad_lord": "Rahu", "ad_telugu": "రాహు", "span": "2022-01-09 నుండి 2024-11-15",
                        "pds": [
                            {"pd_lord": "Rahu", "span": "2022-01-09 నుండి 2022-06-14"},
                            {"pd_lord": "Jupiter", "span": "2022-06-14 నుండి 2022-10-18"},
                            {"pd_lord": "Saturn", "span": "2022-10-18 నుండి 2023-04-01"}
                        ]
                    },
                    {
                        "ad_lord": "Jupiter", "ad_telugu": "గురు", "span": "2024-11-15 నుండి 2027-05-29",
                        "pds": [
                            {"pd_lord": "Jupiter", "span": "2024-11-15 నుండి 2025-03-05"},
                            {"pd_lord": "Saturn", "span": "2025-03-05 నుండి 2025-07-30"},
                            {"pd_lord": "Mercury", "span": "2025-07-30 నుండి 2025-11-25"},
                            {"pd_lord": "Ketu", "span": "2025-11-25 నుండి 2026-01-18"},
                            {"pd_lord": "Venus", "span": "2026-01-18 నుండి 2026-06-20"},
                            {"pd_lord": "Sun", "span": "2026-06-20 నుండి 2026-08-05"},
                            {"pd_lord": "Moon", "span": "2026-08-05 నుండి 2026-10-13"},
                            {"pd_lord": "Mars", "span": "2026-10-13 నుండి 2026-12-04"},
                            {"pd_lord": "Rahu", "span": "2026-12-04 నుండి 2027-05-29"}
                        ]
                    }
                ]
            },
            {
                "md_lord": "Mercury", "md_telugu": "బుధ", "span": "2027-05-29 నుండి 2044-05-29",
                "antardashas": [
                    {
                        "ad_lord": "Mercury", "ad_telugu": "బుధ", "span": "2027-05-29 నుండి 2029-10-25",
                        "pds": [
                            {"pd_lord": "Mercury", "span": "2027-05-29 నుండి 2027-09-24"},
                            {"pd_lord": "Ketu", "span": "2027-09-24 నుండి 2027-11-15"},
                            {"pd_lord": "Venus", "span": "2027-11-15 ------ 2028-04-10"}
                        ]
                    }
                ]
            }
        ]

    def render_html_tree(self, layout_mode=1):
        """
        1 = Compact Indented Table (ప్రింట్ ఆప్టిమైజ్డ్ నిలువు పట్టిక)
        """
        raw_data = self.get_structured_timeline()
        html = ""
        
        if layout_mode == 1:
            html += """
            <table class='tree-table'>
                <thead>
                    <tr>
                        <th>దశా క్రమానుగతం (MD - AD - PD)</th>
                        <th>సమయ పరిధి / కాలపరిమితి</th>
                        <th style='text-align:right;'>సంయుక్త ఫలిత బలం</th>
                    </tr>
                </thead>
                <tbody>"""
            
            for md in raw_data:
                md_lord = md['md_lord']
                md_strength = self.engine.get_planet_strength(md_lord)
                
                # మహర్దశకు దాని బేస్ స్థిర బలం ప్రింట్ అవుతుంది
                html += f"<tr class='row-md'><td>🔱 {md['md_telugu']} మహర్దశ</td><td>{md['span']}</td><td class='fixed-strength'>{md_strength}%</td></tr>"
                
                for ad in md['antardashas']:
                    ad_lord = ad['ad_lord']
                    ad_strength = self.engine.get_planet_strength(ad_lord)
                    
                    # అంతర్దశకు (MD + AD) / 2 సగటు నిష్పత్తి
                    ad_display_score = int(math.ceil((md_strength + ad_strength) / 2.0))
                    
                    html += f"<tr class='row-ad'><td class='indent-ad'>🔸 {ad['ad_telugu']} అంతర్దశ</td><td>{ad['span']}</td><td class='fixed-strength'>{ad_display_score}%</td></tr>"
                    
                    for pd in ad['pds']:
                        pd_lord = pd['pd_lord']
                        pd_strength = self.engine.get_planet_strength(pd_lord)
                        
                        # మీ కోర్ ఆస్ట్రో-లాజిక్ సూత్రం: (MD + AD + PD) / 3
                        pd_final_score = int(math.ceil((md_strength + ad_strength + pd_strength) / 3.0))
                        
                        html += f"<tr class='row-pd'><td class='indent-pd'>• {pd_lord} प्रत्यంతర్దశ</td><td>{pd['span']}</td><td class='fixed-strength'>{pd_final_score}%</td></tr>"
            
            html += "</tbody></table>"
            
        return html