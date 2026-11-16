import os
import shutil
import struct
import subprocess
import zipfile

def patch_arsc():
    print("Reading resources.arsc...")
    with open("/workspace/calm-faraday/resources.arsc", "rb") as f:
        orig_data = f.read()

    # ResTable_header (12 bytes)
    ctype, hsize, total_csize, pkgcount = struct.unpack("<HHIi", orig_data[:12])
    
    # StringPool chunk at offset 12
    sp_offset = 12
    sp_ctype, sp_hsize, sp_csize = struct.unpack("<HHI", orig_data[sp_offset:sp_offset+8])
    scount, stylecount, flags, sstart, stylesstart = struct.unpack("<IIIII", orig_data[sp_offset+8:sp_offset+28])
    string_offsets = struct.unpack(f"<{scount}I", orig_data[sp_offset+28:sp_offset+28+scount*4])
    strings_data_start = sp_offset + sstart

    def read_utf8_entry(data, start):
        pos = start
        c0 = data[pos]
        if c0 & 0x80:
            pos += 2
        else:
            pos += 1
        b0 = data[pos]
        if b0 & 0x80:
            byte_len = ((b0 & 0x7f) << 8) | data[pos+1]
            pos += 2
        else:
            byte_len = b0
            pos += 1
        string_bytes = data[pos:pos+byte_len]
        return string_bytes.decode("utf-8", errors="ignore")

    def encode_utf8_entry(s):
        utf8_bytes = s.encode("utf-8")
        u16_len = len(s)
        b_len = len(utf8_bytes)
        
        buf = bytearray()
        if u16_len > 0x7F:
            buf.append(((u16_len >> 8) & 0x7F) | 0x80)
            buf.append(u16_len & 0xFF)
        else:
            buf.append(u16_len & 0x7F)
            
        if b_len > 0x7F:
            buf.append(((b_len >> 8) & 0x7F) | 0x80)
            buf.append(b_len & 0xFF)
        else:
            buf.append(b_len & 0x7F)
            
        buf.extend(utf8_bytes)
        buf.append(0)
        return bytes(buf)

    # Load replacements
    import json
    with open("/workspace/calm-faraday/translations/improvements.json", "r", encoding="utf-8") as f:
        improvements = json.load(f)
    
    rep_map = {v["old"]: v["new"] for v in improvements.values()}

    all_strings = [read_utf8_entry(orig_data, strings_data_start + string_offsets[i]) for i in range(scount)]
    
    replaced_count = 0
    for i in range(len(all_strings)):
        s = all_strings[i]
        if s in rep_map:
            all_strings[i] = rep_map[s]
            replaced_count += 1

    print(f"Replaced {replaced_count} string occurrences with improved translations!")

    # Encode new StringPool
    encoded_parts = []
    new_offsets = []
    curr_off = 0
    for s in all_strings:
        new_offsets.append(curr_off)
        eb = encode_utf8_entry(s)
        encoded_parts.append(eb)
        curr_off += len(eb)

    encoded_strings_data = b"".join(encoded_parts)
    pad = (4 - (len(encoded_strings_data) % 4)) % 4
    encoded_strings_data += b"\x00" * pad

    new_offsets_bytes = struct.pack(f"<{scount}I", *new_offsets)
    new_sstart = 28 + len(new_offsets_bytes)
    new_chunk_size = new_sstart + len(encoded_strings_data)

    new_sp_header = struct.pack("<HHI", 0x0001, 28, new_chunk_size) + struct.pack("<IIIII", scount, 0, flags, new_sstart, 0)
    new_sp_chunk = new_sp_header + new_offsets_bytes + encoded_strings_data

    # Rest of resources.arsc (Chunk 2, package chunk)
    rest_data = orig_data[sp_offset + sp_csize:]
    
    # New total chunk size
    new_total_csize = 12 + len(new_sp_chunk) + len(rest_data)
    new_root_header = struct.pack("<HHIi", ctype, hsize, new_total_csize, pkgcount)

    patched_arsc = new_root_header + new_sp_chunk + rest_data
    with open("/workspace/calm-faraday/resources_patched.arsc", "wb") as f:
        f.write(patched_arsc)
    print("Saved /workspace/calm-faraday/resources_patched.arsc successfully!")

def build_apk():
    patch_arsc()

    src_apk = "/workspace/calm-faraday/AndVM-release.apk"
    unsigned_apk = "/workspace/calm-faraday/AndVM-translated-unsigned.apk"
    aligned_apk = "/workspace/calm-faraday/AndVM-translated-aligned.apk"
    final_apk = "/workspace/calm-faraday/AndVM-translated.apk"

    print("Repackaging APK with patched resources.arsc...")
    with zipfile.ZipFile(src_apk, "r") as zin:
        with zipfile.ZipFile(unsigned_apk, "w") as zout:
            for item in zin.infolist():
                # Skip old signature files
                if item.filename.startswith("META-INF/") and (item.filename.endswith(".RSA") or item.filename.endswith(".SF") or item.filename.endswith(".MF")):
                    continue
                # Replace resources.arsc
                if item.filename == "resources.arsc":
                    with open("/workspace/calm-faraday/resources_patched.arsc", "rb") as rf:
                        zout.writestr(item, rf.read(), compress_type=zipfile.ZIP_STORED)
                else:
                    zout.writestr(item, zin.read(item.filename), compress_type=item.compress_type)

    print("Creating debug signing key...")
    keystore = "/workspace/calm-faraday/debug.keystore"
    if not os.path.exists(keystore):
        cmd = [
            "keytool", "-genkey", "-v",
            "-keystore", keystore,
            "-storepass", "android",
            "-alias", "androiddebugkey",
            "-keypass", "android",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=AndVM Translated,O=Community,C=US"
        ]
        subprocess.run(cmd, check=True)

    print("Zipaligning APK...")
    zipalign_bin = "/root/android-sdk/build-tools/35.0.0/zipalign"
    env = os.environ.copy()
    env["ANDROID_DATA"] = "/tmp"

    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    cmd = [zipalign_bin, "-v", "-p", "4", unsigned_apk, aligned_apk]
    subprocess.run(cmd, check=True, env=env, stdout=subprocess.DEVNULL)

    print("Signing APK with apksigner...")
    apksigner_bin = "/root/android-sdk/build-tools/35.0.0/apksigner"
    if os.path.exists(final_apk):
        os.remove(final_apk)
    cmd = [
        apksigner_bin, "sign",
        "--ks", keystore,
        "--ks-pass", "pass:android",
        "--key-pass", "pass:android",
        "--out", final_apk,
        aligned_apk
    ]
    subprocess.run(cmd, check=True, env=env)

    print("Verifying final APK signature...")
    cmd = [apksigner_bin, "verify", "--verbose", final_apk]
    res = subprocess.run(cmd, check=True, env=env, stdout=subprocess.PIPE, text=True)
    print(res.stdout)
    print(f"SUCCESS! Output APK generated at: {final_apk}")

if __name__ == "__main__":
    build_apk()
