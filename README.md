# AndVM - Android Universal Kernel GSI Virtual Machine

**From Android 10 to Android 17: New possibilities for every phone.**

_**AndVM is an Android Universal Kernel GSI Virtual Machine that runs multiple versions of the Android OS on an Android device, providing an isolated execution environment for system exploration, application testing, development/debugging, and security research.**_

---

## Key Features

### 01. Multi-Version Android OS Support
Supports Android 10 through Android 17, capable of booting ROMs compatible with standard Android semantics, including:
- **AOSP** (Android Open Source Project)
- **LineageOS**
- **PixelOS**
- Other compatible Android GSI / ROM builds

Experience and explore different Android OS versions directly without needing a new device.

### 02. VM Snapshots & State Recovery
Capture and preserve the exact runtime state of your virtual machine to pause and resume whenever needed.
- **Pause & Resume**: Pause the VM and preserve its active runtime state.
- **Instant Restore**: Resume previous runtime sessions quickly on next launch.
- **Rollback**: Revert back to any previously saved snapshot state.
- **Reproducibility**: Simplify testing, bug reproduction, and system experiments.

Unlike conventional file backups, VM snapshots save the complete live execution state.

### 03. Recovery, Magisk Root & OTA
Perform system-level modifications directly inside the virtual environment:
- Flash full OTA packages.
- Install and configure **Magisk Root**.
- Apply system patches.
- Install compatible third-party components and modules.
- Check system status and perform rollbacks.

Enjoy high flexibility and deep exploration without risking your host device.

### 04. Direct ADB Connection
Connect directly to the virtual machine via ADB, utilizing standard Android development and debugging workflows:
```bash
adb connect <IP>:<PORT>
adb devices
```
Supported workflows:
- Installing and uninstalling apps.
- Executing ADB Shell commands.
- Interactive app debugging and profiling.
- Viewing system logcat streams.
- Fast file transfers.

### 05. Floating Window Mode
Run the virtual machine in a floating window on top of other host applications for seamless multitasking, eliminating disruptions caused by app switching.

### 06. Granular Device Mapping
Configure 9 distinct hardware and system capabilities independently for each virtual machine:
- **Host Real**: Use real hardware devices and states via permission granting.
- **Virtual Data**: Generate mock/virtual device identifiers and sensor data for reproducible environments.
- **Per-item Disabled**: Turn off unnecessary device sensors or capabilities.

*(Note: In Host Real mode, mapping Wi-Fi, Bluetooth, or cellular baseband info requires corresponding host system permissions.)*

---

## ROM Marketplace

Explore and select from a curated list of compatible Android ROM images:
- AOSP
- LineageOS
- PixelOS
- Other community-tested GSI builds

---

## Use Cases

| Use Case | Description |
| :--- | :--- |
| **Application Sandbox** | Run untrusted apps in an isolated Android environment with snapshot rollback. |
| **Security Analysis & Audit** | Monitor application permissions, traffic, logs, and runtime behavior. |
| **Privacy & Multi-Account** | Keep work, personal, and secondary accounts completely segregated. |
| **Development & Compatibility** | Test applications across different Android API levels (Android 10–17) on a single physical phone. |
| **OS Experience** | Test-drive new Android versions and custom ROMs without modifying host firmware. |
| **Automated Testing** | Connect CI/CD pipelines, automation scripts, and test harnesses via ADB. |

---

## Frequently Asked Questions (FAQ)

### What is AndVM?
AndVM is an Android Universal Kernel GSI Virtual Machine that allows you to run independent, fully virtualized guest Android operating system environments directly on your Android phone.

### Which Android versions and ROMs are supported?
It supports Android 10 through Android 17, and works with standard Android GSI (Generic System Image) builds such as AOSP, LineageOS, and PixelOS.

### Can older devices run newer Android versions?
AndVM provides cross-version virtualization capabilities. However, real-world performance depends on the host device's hardware specifications (CPU, RAM, GPU), host kernel, and ROM compatibility.

### What is the difference between snapshots and standard backups?
A standard backup only saves files and application data. A virtual machine snapshot preserves the active execution memory and CPU state, allowing you to freeze an active app or OS state and resume exactly where you left off.

---

## Downloads

Download the latest official APK builds from the [GitHub Releases](https://github.com/AndVM-Dev/AndVM/releases) page.

- **Official Website**: [https://andvm.cn/](https://andvm.cn/)
- **English Portal**: [https://andvm.cn/en/](https://andvm.cn/en/)
