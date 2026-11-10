# ChattyOh Mobile (Flutter: Android + iOS)

A Flutter app that hosts the ChattyOh page (`assets/web/index.html`) in a native WebView and adds mobile features around it. It is **not** a rewrite of the UI in Flutter widgets: the screens are the same HTML app, so edits to the HTML show up in the mobile app.

## Setup
Requires Flutter 3.24+ (and Xcode for iOS, Android Studio/SDK for Android).
```bash
./tool/setup.sh        # generates android/ and ios/, adds INTERNET permission, icons, app name
flutter run            # on a connected device or emulator
flutter build apk      # Android
flutter build ipa      # iOS (needs a signing team in Xcode)
```
If you can't run the script, do by hand: `flutter create --org com.chattyoh --project-name chattyoh_mobile --platforms=android,ios .`, add `<uses-permission android:name="android.permission.INTERNET"/>` to `android/app/src/main/AndroidManifest.xml`, set iOS deployment target to 13.0, then `dart run flutter_launcher_icons`.

## Mobile-specific features
- Bottom navigation (Home, Modes, Chat, Projects, More); the desktop-style bottom activity panel is hidden on phones.
- Android back button: closes dialogs and menus, then goes Home, then exits.
- Share sheet for every export/backup (works on iPad too); file picker for imports.
- API key kept in Keychain / Keystore (`flutter_secure_storage`); AI requests are made by Dart, not the page. Model id is the `_model` constant in `lib/main.dart` (default `claude-sonnet-5-5`). Replies are not streamed.
- Backup safety net: app data is mirrored to a file in the app's documents folder every few seconds and restored automatically if the WebView's storage is wiped.
- External links open in the system browser; the WebView cannot navigate away from the app page.

## Revise and test the HTML without a phone
Open `preview/chattyoh-mobile-preview.html` (it loads `preview/chattyoh-mobile.html`) in a browser. Edit `chattyoh-mobile.html`, press Reload in the preview, and when happy copy it to `assets/web/index.html` (the two files are identical).

## Not included yet
Push notifications, biometrics, store listings/signing, offline AI, streaming replies. Deployments, test runs and "connection OK" inside the app are simulated.
