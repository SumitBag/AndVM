import os
import sys
import xml.etree.ElementTree as ET

def patch_strings(target_file, source_file):
    if not os.path.exists(target_file):
        print(f"Target file {target_file} not found; skipping.")
        return
    if not os.path.exists(source_file):
        print(f"Source file {source_file} not found; skipping.")
        return

    src_tree = ET.parse(source_file)
    src_strings = {
        elem.attrib.get("name"): elem.text
        for elem in src_tree.getroot().findall("string")
        if elem.attrib.get("name")
    }

    target_tree = ET.parse(target_file)
    target_root = target_tree.getroot()

    updated_count = 0
    for elem in target_root.findall("string"):
        name = elem.attrib.get("name")
        if name in src_strings and src_strings[name] is not None:
            elem.text = src_strings[name]
            updated_count += 1

    target_tree.write(target_file, encoding="utf-8", xml_declaration=True)
    print(f"Successfully patched {updated_count} strings in {target_file}")

if __name__ == "__main__":
    decompiled_dir = sys.argv[1] if len(sys.argv) > 1 else "apk_decompiled"
    
    # Patch default (English) strings
    patch_strings(
        os.path.join(decompiled_dir, "res", "values", "strings.xml"),
        "translations/values/strings_updated.xml"
    )

    # Patch Hindi strings if target exists
    patch_strings(
        os.path.join(decompiled_dir, "res", "values-hi", "strings.xml"),
        "translations/values-hi/strings.xml"
    )
