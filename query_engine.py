# -*- coding: utf-8 -*-

class SamarthaQueryEngine:
    def __init__(self, base_parser):
        self.parser = base_parser

    def build_query_grid(self):
        db = self.parser.questions_database
        html = "<table class='master-table'><thead><tr><th>ప్రశ్న ఐడి</th><th>జీవిత ప్రశ్న వివరాలు</th><th>యాక్టివ్ సమయ పరిధి</th><th style='text-align:right;'>నిశ్చయ బలం (సంభావ్యత)</th></tr></thead><tbody>"
        
        for group_name, questions in db.items():
            html += f"<tr style='background-color: #f1f1f1; font-weight: bold;'><td colspan='4' style='color: #b38600;'>{group_name}</td></tr>"
            for q_num, data in questions.items():
                timeline = "జీవితకాలం (Lifelong)" if data["timeline"] == "None" else data["timeline"]
                score = data["score"]
                badge_class = "high-score" if score >= 70 else ("med-score" if score >= 50 else "low-score")
                
                html += f"""
                <tr>
                    <td style='font-weight: bold; text-align: center; width: 80px;'>{q_num}</td>
                    <td>{data["text"]}</td>
                    <td>{timeline}</td>
                    <td style='text-align: right;'><span class='score-badge {badge_class}'>{score}%</span></td>
                </tr>"""
        html += "</tbody></table>"
        return html