# AndVM Localization & Translation Analysis Report

## 1. Overview
- **Application Package**: `com.lerist.andvm`
- **Official Release**: `AndVM-release.apk` (v0.0.7 BETA 8)
- **Total Resource Strings**: 1,252 (including 1,205 application-specific strings)
- **Primary Source Language**: Chinese (`zh`)
- **Default Application Language**: English (`values/`)
- **Officially Supported Locales in APK**: 18 languages:
  - English (`default`)
  - Chinese Simplified (`zh`)
  - Chinese Traditional (`zh-rTW`, `zh-rHK`)
  - Hindi (`hi`)
  - Japanese (`ja`)
  - Korean (`ko`)
  - German (`de`)
  - French (`fr`)
  - Spanish (`es`)
  - Italian (`it`)
  - Portuguese (Brazil) (`pt-rBR`)
  - Russian (`ru`)
  - Turkish (`tr`)
  - Vietnamese (`vi`)
  - Thai (`th`)
  - Indonesian (`in`)
  - Arabic (`ar`)

---

## 2. Generated Assets & Files in Workspace
The following translation resources have been extracted and generated inside `/workspace/calm-faraday/translations/`:

| File | Description |
| :--- | :--- |
| [`values/strings_updated.xml`](file:///workspace/calm-faraday/translations/values/strings_updated.xml) | **Refined English strings** with natural phrasing, corrected Android terminology, and Chinese source comments. |
| [`values/strings.xml`](file:///workspace/calm-faraday/translations/values/strings.xml) | Extracted original default English strings. |
| [`values-zh/strings.xml`](file:///workspace/calm-faraday/translations/values-zh/strings.xml) | Extracted Chinese reference strings (`1,147` strings). |
| [`values-hi/strings.xml`](file:///workspace/calm-faraday/translations/values-hi/strings.xml) | Extracted Hindi strings (`1,175` strings). |
| [`all_translations.json`](file:///workspace/calm-faraday/translations/all_translations.json) | Complete JSON mapping of all string IDs across all locales. |
| [`improvements.json`](file:///workspace/calm-faraday/translations/improvements.json) | Detailed changelog of refined English phrases and rationale. |

---

## 3. Key Translation Improvements Summary

### A. Terminal & ADB Debugging
- **Soft Keyboard**: Changed `"Put away the keyboard"` $\rightarrow$ **`"Hide keyboard"`** (standard Android convention).
- **Log Scrolling**: Changed `"Return to latest output"` $\rightarrow$ **`"Jump to latest output"`**.
- **Button Labels**: Changed `"Connection"` $\rightarrow$ **`"Connect"`** (verb for interactive action).
- **Permissions**: Changed `"Host file access rights"` $\rightarrow$ **`"Host file access permissions"`**.
- **State Labels**: Changed `"Wireless ADB is turned on"` $\rightarrow$ **`"Wireless ADB is enabled"`**; `"Native ADB debugging has been turned on."` $\rightarrow$ **`"Local ADB debugging is enabled."`**.

### B. Gestures & Navigation
- **Gesture Conflict**: Changed `"Slide-up trigger area height (dp)"` $\rightarrow$ **`"Swipe-up trigger area height (dp)"`**.
- **Host Matching**: Changed `"Follow the host"` $\rightarrow$ **`"Match host device"`**.
- **Gesture Optimization**: Changed `"Gesture navigation bar optimization"` $\rightarrow$ **`"Gesture navigation bar optimizations"`**.

### C. System Properties & Advanced Options
- **build.prop terminology**: Changed `"Clear attributes"` $\rightarrow$ **`"Clear properties"`**; `"%1$s override attributes configured"` $\rightarrow$ **`"%1$s override properties configured"`**.
- **Instructions**: Changed `"Fill in attribute name = value in each line, support # comment."` $\rightarrow$ **`"Enter property=value on each line. Lines beginning with # are comments."`**.

### D. Recovery, Magisk & OTA
- **Integrity Checks**: Changed `"Put away file verification information"` $\rightarrow$ **`"Hide file checksum details"`**.
- **Status**: Changed `"Nothing installed"` $\rightarrow$ **`"Not flashed"`** (standard custom ROM/recovery terminology).
- **Progress Message**: Changed `"Recovery is being processed"` $\rightarrow$ **`"Recovery processing in progress…"`**.

### E. Device Mapping & Geolocation
- **Sensors & Radio**: Changed `"One base station per row"` $\rightarrow$ **`"One cellular tower per line"`**; `"One Wi-Fi per row"` $\rightarrow$ **`"One Wi-Fi network per line"`**.
- **GPS Units**: Changed `"Precision radius (meter)"` $\rightarrow$ **`"Accuracy radius (meters)"`**; `"Altitude (meter)"` $\rightarrow$ **`"Altitude (meters)"`**.
- **Overview Card**: Changed `"Nine abilities · Click the card to adjust"` $\rightarrow$ **`"9 Capabilities · Tap card to configure"`**.

---

## 4. How to Use & Contribute
1. **Submit Upstream**: You can submit `translations/values/strings_updated.xml` directly to the AndVM development team at `andvm.dev@gmail.com` or create a PR/issue on [AndVM-Dev/AndVM](https://github.com/AndVM-Dev/AndVM).
2. **Repository Documentation**: The repository's root [`README.md`](file:///workspace/calm-faraday/README.md) has already been populated with the full English documentation covering all features, FAQ, and use cases.
