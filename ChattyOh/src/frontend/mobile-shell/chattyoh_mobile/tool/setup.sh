#!/usr/bin/env bash
# One-time setup: generates the android/ and ios/ folders, adds permissions, icons and app names.
set -e
cd "$(dirname "$0")/.."
flutter create --org com.chattyoh --project-name chattyoh_mobile --platforms=android,ios .
flutter pub get

# Android: INTERNET permission (needed for AI calls in release builds) + app name
M=android/app/src/main/AndroidManifest.xml
grep -q 'android.permission.INTERNET' "$M" || sed -i.bak 's#<manifest xmlns:android="http://schemas.android.com/apk/res/android">#&\n    <uses-permission android:name="android.permission.INTERNET"/>#' "$M"
sed -i.bak 's#android:label="[^"]*"#android:label="ChattyOh"#' "$M" && rm -f "$M.bak"

# iOS: display name (macOS only) and minimum version
if [ -x /usr/libexec/PlistBuddy ]; then
  /usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName ChattyOh" ios/Runner/Info.plist || true
fi
[ -f ios/Podfile ] && sed -i.bak "s/^# platform :ios.*/platform :ios, '13.0'/" ios/Podfile && rm -f ios/Podfile.bak

dart run flutter_launcher_icons
echo "Done. Run: flutter run   (or: flutter build apk / flutter build ipa)"
