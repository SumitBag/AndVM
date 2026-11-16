import json
import os
import re

def escape_xml(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("'", "\\'")
    return s

def clean_comment(s):
    return s.replace("--", "- -")

# Load all extracted translations
with open("/workspace/calm-faraday/translations/all_translations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Comprehensive dictionary of targeted English improvements
# (resource_id -> (old_english, new_english, reason))
improvements = {
    # ADB & Terminal
    "host_adb_terminal_pane_0478ffd3": (
        "Put away the keyboard",
        "Hide keyboard",
        "More natural Android UI terminology for dismissing soft keyboard"
    ),
    "host_adb_terminal_pane_627387f4": (
        "Return to latest output",
        "Jump to latest output",
        "Standard terminal UI action for scrolling down to latest output"
    ),
    "host_adb_terminal_pane_7328deeb": (
        "Connection",
        "Connect",
        "Verb action label on button instead of noun"
    ),
    "host_adb_terminal_pane_44238741": (
        "Host file access rights",
        "Host file access permissions",
        "Standard Android permission terminology"
    ),
    "host_adb_terminal_pane_666b26cb": (
        "Copy selected area/output all",
        "Copy selection / Copy all output",
        "Clearer action description"
    ),
    "host_adb_terminal_pane_80e37fe7": (
        "Authorization Download/AndVM",
        "Authorize Download/AndVM directory",
        "Proper English phrasing for granting storage permission"
    ),
    "host_adb_debug_panel_04f46a76": (
        "External wireless debugging has been turned on.",
        "External wireless ADB debugging is enabled.",
        "Clearer and more standard technical terminology"
    ),
    "host_adb_debug_panel_35eb5b12": (
        "Native ADB debugging has been turned on.",
        "Local ADB debugging is enabled.",
        "Clearer distinction between local device debugging and external wireless debugging"
    ),
    "host_adb_debug_panel_cc0c19fb": (
        "Wireless ADB is turned on",
        "Wireless ADB is enabled",
        "Standard status phrasing"
    ),
    "host_adb_debug_panel_e2fbd1a4": (
        "ADB debugging has been turned off.",
        "ADB debugging is disabled.",
        "Standard status phrasing"
    ),
    "host_adb_debug_panel_df575eb0": (
        "Turn on external wireless debugging?",
        "Enable external wireless debugging?",
        "More professional dialog prompt"
    ),
    "host_adb_debug_panel_928d80fa": (
        "ADB debugging can be turned on after starting the virtual machine.",
        "ADB debugging can be enabled after starting the virtual machine.",
        "Better verb usage"
    ),
    "host_adb_debug_panel_c248f129": (
        "A single paste supports up to 16,384 characters, please paste in sections.",
        "A single paste supports up to 16,384 characters. Please paste in smaller chunks.",
        "Improved sentence flow"
    ),

    # Gestures & Navigation
    "host_bottom_gesture_settings_79529e83": (
        "Follow the host",
        "Match host device",
        "Clearer meaning for inheriting host system settings"
    ),
    "host_bottom_gesture_settings_45688a63": (
        "Slide-up trigger area height (dp)",
        "Swipe-up trigger area height (dp)",
        "Standard gesture terminology (swipe-up instead of slide-up)"
    ),
    "host_bottom_gesture_settings_c43df18f": (
        "Expand the bottom sliding trigger area to avoid conflict with the host gesture",
        "Expand bottom swipe-up trigger area to prevent conflicts with host navigation gestures",
        "Clearer technical explanation"
    ),
    "host_bottom_gesture_settings_86dc6c3e": (
        "Gesture navigation bar optimization",
        "Gesture navigation bar optimizations",
        "Standard pluralization"
    ),

    # Advanced Options & Properties
    "host_advanced_options_642c86e0": (
        "Clear attributes",
        "Clear properties",
        "Correct Android terminology for build.prop / system properties"
    ),
    "host_advanced_options_d6f19fa7": (
        "%1$s override attributes configured",
        "%1$s override properties configured",
        "Correct Android system properties terminology"
    ),
    "host_advanced_options_b6db14ae": (
        "Fill in attribute name = value in each line, support # comment.",
        "Enter property=value on each line. Lines beginning with # are comments.",
        "Clearer instruction syntax"
    ),
    "host_advanced_options_dbb39e25": (
        "The next cold start will take effect without re-preparing the system. Restore the ROM default properties after clearing the configuration.",
        "Takes effect upon next cold start without re-preparing the system. Cleared configuration restores ROM default properties.",
        "More concise and professional phrasing"
    ),

    # Floating Windows & UX
    "host_guest_floating_window_b26bc0d8": (
        "Close the floating window, long press to pause or stop the virtual machine",
        "Tap to close floating window; long-press to pause or shut down VM",
        "Clearer touch gesture instructions"
    ),
    "host_guest_floating_window_d505a1e3": (
        "Click to close the floating window, long press and slide to pause or stop the virtual machine",
        "Tap to close floating window; long-press and drag to pause or shut down VM",
        "Standard mobile touch terminology (tap instead of click)"
    ),
    "host_vm_export_sheet_a0f9d567": (
        "Background export in progress·Click to view progress",
        "Background export in progress · Tap to view progress",
        "Fixed spacing and replaced 'Click' with 'Tap'"
    ),
    "host_vm_export_sheet_62ca2434": (
        "Click to view results",
        "Tap to view results",
        "Mobile UI convention ('Tap')"
    ),

    # Recovery, Magisk & OTA
    "host_recovery_dialog_f78c32d0": (
        "Put away file verification information",
        "Hide file checksum details",
        "Clearer technical description for collapsing checksum card"
    ),
    "host_recovery_dialog_06a813a5": (
        "View file verification information",
        "View file checksum details",
        "Consistent checksum phrasing"
    ),
    "host_recovery_dialog_399c6826": (
        "Recovery is being processed",
        "Recovery processing in progress…",
        "Better ongoing progress state message"
    ),
    "host_recovery_dialog_436073d5": (
        "Nothing installed",
        "Not flashed",
        "Correct Android custom ROM/Recovery terminology"
    ),
    "host_recovery_dialog_7d199e2d": (
        "The installation script will be actually executed in the isolated Recovery; system and data changes will be saved after success, and the original state will be retained after failure. OTA updates the system and preserves user data.",
        "The installation script executes inside an isolated Recovery environment. System and data changes are applied upon success, or rolled back on failure. OTA updates preserve user data.",
        "Cleaner and more professional technical documentation"
    ),
    "host_recovery_dialog_7973c81e": (
        "When startup fails, all patches and Magisk can be disabled and user data retained. It will take effect on the next cold start.",
        "If startup fails, all patches and Magisk can be disabled while retaining user data. Takes effect upon next cold start.",
        "Better conditional flow"
    ),
    "host_recovery_dialog_0478e3a4": (
        "Do not start the virtual machine before the operation is completed. You can switch to the background and wait.",
        "Do not start the virtual machine until this operation completes. You may switch to background while waiting.",
        "Improved sentence structure"
    ),

    # Device Mapping
    "host_device_mapping_screen_10822810": (
        "Nine abilities · Click the card to adjust",
        "9 Capabilities · Tap card to configure",
        "More natural terminology and mobile touch verb"
    ),
    "host_device_mapping_screen_00124354": (
        "Currently, it completely follows the default mapping. After modifying any item, it becomes an independent configuration of this virtual machine.",
        "Currently inherits default mapping. Modifying any item creates an independent configuration for this VM.",
        "More concise and professional"
    ),
    "host_device_mapping_screen_1f1759d5": (
        "This virtual machine has independent mapping, and the items that are not covered continue to follow the default value.",
        "This virtual machine has custom mappings; unconfigured items continue to inherit default values.",
        "Clearer inheritance behavior"
    ),
    "host_device_mapping_screen_1c060d0c": (
        "Virtual mode provides certain data by AndVM, no additional settings are required.",
        "In Virtual mode, simulated device data is generated automatically by AndVM.",
        "Accurate description of synthetic device data"
    ),
    "host_device_mapping_screen_3a51924c": (
        "One base station per row",
        "One cellular tower per line",
        "Accurate telecom terminology (cellular tower / cell station)"
    ),
    "host_device_mapping_screen_2897c077": (
        "One Wi-Fi per row",
        "One Wi-Fi network per line",
        "Clearer specification"
    ),
    "host_device_mapping_screen_8bf6ac7c": (
        "This device cannot be seen in the virtual machine after being disabled.",
        "When disabled, this device capability is hidden from the virtual machine.",
        "Clearer explanation"
    ),
    "host_device_mapping_screen_82981e71": (
        "Host mode uses Android public API, read-only mapping, and does not control the host device.",
        "Host mode uses official Android public APIs for read-only mapping without controlling the host device.",
        "Clarifies safety of host mapping"
    ),
    "host_device_mapping_screen_95a5e614": (
        "Scope of action",
        "Scope",
        "Standard UI heading"
    ),
    "host_device_mapping_screen_47fd06b6": (
        "The selection here is only used as the initial value for the newly imported virtual machine; existing virtual machines are set separately in their respective configuration pages.",
        "These choices serve as the initial default for newly imported VMs. Existing virtual machines retain their individual settings.",
        "Improved readability"
    ),
    "host_device_mapping_editors_df1fe2af": (
        "Precision radius (meter)",
        "Accuracy radius (meters)",
        "Standard GPS geolocation terminology (accuracy radius in meters)"
    ),
    "host_device_mapping_editors_eb045494": (
        "Altitude (meter)",
        "Altitude (meters)",
        "Standard plural unit"
    ),

    # Permissions & System Settings
    "host_notification_permission_request_649f160c": (
        "The system does not allow notification authorization to be turned on. Please turn on notifications in the application settings.",
        "Notification permission was not granted by the system. Please enable notifications in device App Settings.",
        "Clearer instruction for users troubleshooting permissions"
    ),
    "host_component_settings_page_07b00f3f": (
        "Remove components",
        "Streamline components",
        "Accurate translation of 精简组件 (debloading/streamlining rather than just deleting)"
    ),
}

# Generate updated English strings
app_resources = [k for k in sorted(data.keys()) if not (k.startswith("abc_") or k.startswith("mtrl_") or k.startswith("androidx_"))]

updated_count = 0
out_path = "/workspace/calm-faraday/translations/values/strings_updated.xml"
with open(out_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!-- AndVM Refined & Polished English Localization -->\n')
    f.write('<resources>\n')
    for res_id in app_resources:
        val = data[res_id].get("", "")
        zh_comment = data[res_id].get("zh", "")
        if res_id in improvements:
            old_val, new_val, reason = improvements[res_id]
            val = new_val
            updated_count += 1
            f.write(f'    <!-- ZH: {clean_comment(zh_comment)} | Refined: {reason} -->\n')
        elif zh_comment:
            f.write(f'    <!-- ZH: {clean_comment(zh_comment)} -->\n')
        
        if val:
            f.write(f'    <string name="{res_id}">{escape_xml(val)}</string>\n')
    f.write('</resources>\n')

print(f"Generated {out_path} with {updated_count} refined English translations!")

# Save report of improvements to JSON
with open("/workspace/calm-faraday/translations/improvements.json", "w", encoding="utf-8") as f:
    json.dump({k: {"old": v[0], "new": v[1], "reason": v[2]} for k, v in improvements.items()}, f, indent=2, ensure_ascii=False)
