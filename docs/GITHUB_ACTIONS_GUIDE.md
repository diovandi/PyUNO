# GitHub Actions - Automated Cross-Platform Builds

This guide explains how to use GitHub Actions to automatically build PyUNO executables for Windows, macOS, and Linux.

## 🚀 What the Workflow Does

The GitHub Actions workflow (`.github/workflows/build.yml`) automatically:

1. **Builds on every push/PR** to `main` branch
2. **Creates executables** for Windows, macOS, and Linux
3. **Uploads artifacts** that you can download
4. **Creates releases** when you tag a version

## 📋 Build Matrix

| Platform | Executable | Launcher | Archive Format |
|----------|------------|----------|----------------|
| Windows | `PyUNO_Final.exe` | `run_pyuno_final.bat` | `.zip` |
| macOS | `PyUNO_Final.app` | `run_pyuno_final.command` | `.zip` |
| Linux | `PyUNO_Final` | `run_pyuno_final.sh` | `.tar.gz` |

## 🔄 How to Use

### Option 1: Development Builds (Every Push)

1. **Push changes** to `main` or `develop` branch
2. **GitHub Actions runs automatically**
3. **Download artifacts** from the Actions tab:
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Click on the latest workflow run
   - Scroll down to "Artifacts" section
   - Download the platform-specific builds

### Option 2: Release Builds (Version Tags)

1. **Create a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions automatically:**
   - Builds for all platforms
   - Creates a GitHub Release
   - Uploads packaged executables
   - Generates release notes

3. **Users can download** from the Releases page

## 🎯 Release Process

### Step 1: Prepare Release
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare release v1.0.0"
git push origin main
```

### Step 2: Create Tag
```bash
# Create and push version tag
git tag -a v1.0.0 -m "PyUNO v1.0.0 - First stable release"
git push origin v1.0.0
```

### Step 3: Automatic Release
- GitHub Actions builds all platforms (~10-15 minutes)
- Creates release with all executables
- Users can download immediately

## 📁 Download Locations

### Development Builds
- **Location**: Repository → Actions → Workflow Run → Artifacts
- **Retention**: 90 days
- **Format**: Individual platform artifacts

### Release Builds  
- **Location**: Repository → Releases
- **Retention**: Permanent
- **Format**: Packaged archives ready for distribution

## 🔧 Customization

### Modify Build Platforms
Edit `.github/workflows/build.yml` matrix section:
```yaml
strategy:
  matrix:
    include:
      - os: windows-latest
        platform: windows
        executable: PyUNO_Final.exe
```

### Change Python Version
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Change version here
```

### Add Build Steps
Add custom steps before or after the build:
```yaml
- name: Custom step
  run: echo "Custom build step"
```

## 🐛 Troubleshooting

### Build Fails on Linux
- **SDL dependencies** are automatically installed
- Check system packages in workflow

### Build Fails on macOS
- **Universal2 binary** creation requires proper PyInstaller version
- Icon generation might need Xcode tools

### Build Fails on Windows
- **ICO file creation** requires Pillow
- Check Windows-specific PyInstaller options

### Artifacts Not Uploading
- Check **file paths** in upload step
- Verify **executable names** in matrix

## 📊 Workflow Status

Add this badge to your README to show build status:

```markdown
![Build Status](https://github.com/YOUR_USERNAME/PyUNO/actions/workflows/build.yml/badge.svg)
```

## 🔐 Permissions

The workflow needs:
- **Read access** to repository (automatic)
- **Write access** for releases (configured in workflow)

No additional setup required - GitHub provides these automatically.

## 💡 Benefits

✅ **No local setup needed** - Build on GitHub's servers  
✅ **All platforms covered** - Windows, macOS, Linux  
✅ **Automatic releases** - Tag and forget  
✅ **Consistent builds** - Same environment every time  
✅ **Free for public repos** - GitHub Actions included  
✅ **Professional distribution** - Proper release management 