# ============================================================================
# NSIS configuration definitions. Generated from config.nsh.in.
# ============================================================================

# Do not prefix comments with ";". They will be removed by CMake.

# MUST match "<Product ... Name=" in wix/Wireshark.wxs.
!define PROGRAM_NAME "Wireshark"
!define TOP_SRC_DIR "C:\Development\eceld-wireshark-master-3.2"
!define WIRESHARK_TARGET_PLATFORM win64
!define TARGET_MACHINE x64
!define EXTRA_INSTALLER_DIR "C:\Users\Rocio\source\repos\eceld-wireshark\wireshark-win64-libs-3.2"
!define NPCAP_PACKAGE_VERSION 0.9991
!define USBPCAP_PACKAGE_VERSION 1.5.4.0
!define VERSION 3.2.5
!define VERSION_MAJOR 3
!define VERSION_MINOR 2
!define PRODUCT_VERSION 3.2.5.0

!define VCREDIST_EXE "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Redist\MSVC\14.27.29016\vcredist_x64.exe"

# Optional components

!define MMDBRESOLVE_EXE TRUE

!define DOCBOOK_DIR "C:\Development\wsbuild64\docbook"

!define SMI_DIR "C:/Users/Rocio/source/repos/eceld-wireshark/wireshark-win64-libs-3.2/libsmi-svn-40773-win64ws"

!define QT_DIR "${STAGING_DIR}"
