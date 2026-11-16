import os
import json

def escape_xml(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    # In Android strings.xml, apostrophes and quotes should be escaped
    s = s.replace("'", "\\'")
    return s

def clean_comment(s):
    # XML comments cannot contain --
    return s.replace("--", "- -")

with open("/workspace/calm-faraday/translations/all_translations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

app_resources = [k for k in sorted(data.keys()) if not (k.startswith("abc_") or k.startswith("mtrl_") or k.startswith("androidx_"))]

def generate_strings_xml(locale_key, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    count = 0
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<resources>\n')
        for res_id in app_resources:
            val = data[res_id].get(locale_key, "")
            if val:
                zh_comment = data[res_id].get("zh", "")
                if zh_comment and locale_key != "zh":
                    f.write(f'    <!-- ZH: {clean_comment(zh_comment)} -->\n')
                f.write(f'    <string name="{res_id}">{escape_xml(val)}</string>\n')
                count += 1
        f.write('</resources>\n')
    print(f"Generated {filepath} with {count} strings.")

generate_strings_xml("", "/workspace/calm-faraday/translations/values/strings.xml")
generate_strings_xml("zh", "/workspace/calm-faraday/translations/values-zh/strings.xml")
generate_strings_xml("hi", "/workspace/calm-faraday/translations/values-hi/strings.xml")
