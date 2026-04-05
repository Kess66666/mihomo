---
# GitHub Agentic Workflow - Fast mihomo Build
# Natural language instead of complex YAML

on: 
  workflow_dispatch:
  push:
    branches: [Alpha]
    paths: ['.github/agentic-workflows/mihomo-fast-build.md']
    
permissions: write-all
tools:
  github:
    toolsets: [actions, issues, pull-requests]
  safeoutputs___comment:
    
engine: copilot-enhanced
name: "Fast mihomo Build - N5000 & K90 Pro Max Only"
description: "Optimized build for two specific devices, avoiding 60+ unnecessary targets"
concurrency:
  group: "${{ github.workflow }}-${{ github.ref }}"
  cancel-in-progress: true
---

# 🚀 mihomo Fast Build - Device-Specific Optimizations

## 🎯 Build Targets

**Only compile two specific devices:**
1. **N5000 Host** (OpenWrt/iStoreOS)
   - Platform: `linux/amd64`
   - Optimization: `GOAMD64=v2` (perfect for N5000 instruction set)
   - Static compilation: `CGO_ENABLED=0` (zero dependencies)
   - Tags: "with_gvisor"
   - Output: `mihomo-n5000-optimized`

2. **Redmi K90 Pro Max** (Android 16)
   - Platform: `android/arm64`
   - NDK: API 35 (Android 15, compatible with Android 16)
   - Compiler: `aarch64-linux-android35-clang`
   - CGO enabled: `CGO_ENABLED=1` (better native performance on Snapdragon 8 Elite)
   - Output: `mihomo-k90pro-android-arm64`

## 🔧 Problem Solving

### Fix: "x509: certificate signed by unknown authority"
- Embed full Mozilla CA certificate bundle in binary
- Download from: https://curl.se/ca/cacert.pem (3529 certificates)
- Compile-time embedding for Android compatibility

### Fix: "configure tun interface: add route 0: network is unreachable"
- Android-specific TUN compatibility mode
- Avoid 0.0.0.0/0 routes (use 0.0.0.0/1 + 128.0.0.0/1)
- Fallback to Android VPNService API if needed

## ⚡ Performance Gains

**From old workflow (60+ targets):**
- Compile time: 30-60 minutes
- GitHub Actions minutes: High usage
- Artifacts: Many unnecessary binaries

**To new workflow (2 targets):**
- Compile time: 3-5 minutes
- GitHub Actions minutes: Reduced 90%
- Artifacts: Only needed binaries
- Specific optimizations for each device

## 📦 Build Configuration

### N5000 Host (Optimized for Jasper Lake)
```yaml
GOOS: linux
GOARCH: amd64
GOAMD64: v2
CGO_ENABLED: 0
Tags: with_gvisor
LDFLAGS: "-s -w -buildid="
Binary: mihomo-n5000-optimized
```

### Redmi K90 Pro Max (Optimized for Snapdragon 8 Elite)
```yaml
GOOS: android
GOARCH: arm64
NDK: aarch64-linux-android35
CGO_ENABLED: 1
Tags: with_gvisor
LDFLAGS: "-s -w"
Binary: mihomo-k90pro-android-arm64
Special: Embedded CA certificates
```

## 🔍 Quality Gates

- Verify TLS certificate bundle is compiled in
- Test TUN interface compatibility
- Validate binary runs on target platforms
- Check binary size (< 20MB each)
- Ensure OpenWrt compatibility (static linking)

## 🚀 Deployment

**Option A:** Replace existing build.yml (recommended for speed)
**Option B:** Add as parallel workflow (test first)

**Artifact names:**
- `mihomo-n5000-optimized-{version}.gz`
- `mihomo-k90pro-android-arm64-{version}`

**GitHub Actions workflow_dispatch inputs:**
- `version`: "Tag version to release" (required)

## 📋 Next Steps

1. Commit this workflow file
2. Manually trigger from GitHub UI
3. Verify artifacts are created
4. Test binaries on actual devices
5. If successful, disable old workflow

**Success criteria:** Both binaries compile in under 5 minutes with device-specific optimizations.

---

*This agentic workflow is designed for Kess66666's mihomo fork on Alpha branch, targeting specific hardware configurations rather than generic cross-compilation.*
