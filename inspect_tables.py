# -*- coding: utf-8 -*-
import json

def inspect_raw_tables():
    print("==================================================")
    print("   SAMARTHA LAYOUT TABLE STRUCTURAL INSPECTOR     ")
    print("==================================================")
    
    try:
        with open("raju_canonical_content.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        pages = data.get("pages", [])
        print(f"మొత్తం పేజీల సంఖ్య: {len(pages)}")
        
        table_count = 0
        # పేజీల లోపల టేబుల్ స్ట్రక్చర్స్ కోసం డీప్ సెర్చ్
        for p_idx, page in enumerate(pages):
            blocks = page.get("content_blocks", page.get("blocks", []))
            for b_idx, block in enumerate(blocks):
                # బ్లాక్ లోపల టేబుల్ లేదా రోస్ డేటా ఉంటే పట్టుకోవడం
                if isinstance(block, dict) and ("table" in block or "rows" in block or block.get("type") == "table"):
                    table_count += 1
                    print(f"\n[💥] పేజీ {p_idx+1} లో {table_count}వ పట్టిక దొరికింది!")
                    # ఆ టేబుల్ యొక్క మొదటి 1500 క్యారెక్టర్ల స్ట్రక్చర్ ని ప్రింట్ చేయడం
                    print(json.dumps(block, indent=2, ensure_ascii=False)[:1500])
                    print("\n--------------------------------------------------")
                    if table_count >= 2:
                        break
            if table_count >= 2:
                break
                
        if table_count == 0:
            print("\n⚠️ జేసన్ లో నిర్దిష్టమైన 'table' కీ దొరకలేదు. రా టెక్స్ట్ బ్లాక్స్ ఎలా ఉన్నాయో చూద్దాం:")
            print(json.dumps(pages[0], indent=2, ensure_ascii=False)[:1000])
            
    except Exception as e:
        print(f"⚠️ ఫైల్ ఇన్‌స్పెక్షన్ లో లోపం: {e}")

if __name__ == "__main__":
    inspect_raw_tables()