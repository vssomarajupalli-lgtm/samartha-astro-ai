# -*- coding: utf-8 -*-
import json

def debug_json_structure():
    print("==================================================")
    print("   SAMARTHA JSON SCHEMA DIAGNOSTIC UTILITY       ")
    print("==================================================")
    
    try:
        with open("raju_canonical_content.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("\n[1] జేసన్ లోని ప్రధాన కీస్ (Top-Level Keys):")
        print(list(data.keys()))
        
        print("\n[2] మొదటి 600 అక్షరాల డేటా స్ట్రక్చర్ శాంపిల్:")
        raw_sample = json.dumps(data, indent=2, ensure_ascii=False)
        print(raw_sample[:600])
        
    except Exception as e:
        print(f"⚠️ జేసన్ రీడ్ చేయడంలో లోపం వచ్చింది: {e}")
    
    print("\n==================================================")

if __name__ == "__main__":
    debug_json_structure()