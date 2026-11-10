import 'dart:convert';
import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ChattyOhApp());
}

class ChattyOhApp extends StatelessWidget {
  const ChattyOhApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'ChattyOh',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(colorSchemeSeed: const Color(0xFF0A5BD9), useMaterial3: true),
        home: const Shell(),
      );
}

class Shell extends StatefulWidget {
  const Shell({super.key});

  @override
  State<Shell> createState() => _ShellState();
}

class _ShellState extends State<Shell> {
  // Change this if your account uses a different model id.
  static const _model = 'claude-sonnet-5-5';
  // Gives the page a real https origin so localStorage behaves normally.
  static const _origin = 'https://app.chattyoh.local/';

  final _secure = const FlutterSecureStorage();
  late final WebViewController _wv;
  bool _dark = false;

  @override
  void initState() {
    super.initState();
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light);
    _wv = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF0A5BD9))
      ..addJavaScriptChannel('Native', onMessageReceived: (m) => _onMessage(m.message))
      ..setNavigationDelegate(NavigationDelegate(
        onNavigationRequest: (r) {
          // Keep the app on its own page; send real links to the system browser.
          if (r.url.startsWith(_origin) || r.url == 'about:blank') return NavigationDecision.navigate;
          if (r.url.startsWith('https://')) {
            launchUrl(Uri.parse(r.url), mode: LaunchMode.externalApplication);
          }
          return NavigationDecision.prevent;
        },
      ));
    _load();
  }

  Future<void> _load() async {
    final html = await rootBundle.loadString('assets/web/index.html');
    await _wv.loadHtmlString(html, baseUrl: _origin);
  }

  // ---- JS <-> Dart bridge -------------------------------------------------
  Future<void> _reply(int id, Object? value) =>
      _wv.runJavaScript('window.__native_reply($id, ${jsonEncode(value)})');

  Future<File> _backupFile() async =>
      File('${(await getApplicationDocumentsDirectory()).path}/chattyoh-backup.json');

  Future<void> _onMessage(String raw) async {
    final Map<String, dynamic> m;
    try {
      m = jsonDecode(raw) as Map<String, dynamic>;
    } catch (_) {
      return;
    }
    final id = (m['id'] as num?)?.toInt() ?? 0;
    try {
      switch (m['type']) {
        case 'snapshot':
          await (await _backupFile()).writeAsString(m['data'] as String);
          break;
        case 'backup':
          final f = await _backupFile();
          await _reply(id, await f.exists() ? await f.readAsString() : null);
          break;
        case 'theme':
          if (mounted) setState(() => _dark = m['dark'] == true);
          break;
        case 'save':
          await _reply(id, await _save(m['name'] as String, m['text'] as String));
          break;
        case 'open':
          await _reply(id, await _open());
          break;
        case 'hasKey':
          final k = await _secure.read(key: 'anthropic_key');
          await _reply(id, k != null && k.isNotEmpty);
          break;
        case 'setKey':
          final key = (m['key'] as String).trim();
          key.isEmpty
              ? await _secure.delete(key: 'anthropic_key')
              : await _secure.write(key: 'anthropic_key', value: key);
          await _reply(id, true);
          break;
        case 'ai':
          await _reply(id, await _ai((m['messages'] as List).cast<Map>(), m['system'] as String?));
          break;
      }
    } catch (e) {
      if (id != 0) await _reply(id, {'ok': false, 'error': e.toString()});
    }
  }

  Future<Map<String, dynamic>> _save(String name, String text) async {
    final safe = name.split(RegExp(r'[\\/]')).last;
    final file = File('${(await getTemporaryDirectory()).path}/$safe');
    await file.writeAsString(text);
    final box = context.findRenderObject() as RenderBox?; // iPad needs an anchor rect
    await Share.shareXFiles(
      [XFile(file.path)],
      sharePositionOrigin: box == null ? null : box.localToGlobal(Offset.zero) & box.size,
    );
    return {'ok': true};
  }

  Future<Map<String, dynamic>?> _open() async {
    final r = await FilePicker.platform.pickFiles(
        type: FileType.custom, allowedExtensions: ['json', 'txt', 'md', 'csv'], withData: true);
    final f = r?.files.single;
    if (f == null || f.bytes == null) return null;
    if (f.size > 5 * 1024 * 1024) return {'error': 'File is larger than 5 MB'};
    return {'name': f.name, 'text': utf8.decode(f.bytes!, allowMalformed: true)};
  }

  Future<Map<String, dynamic>> _ai(List<Map> msgs, String? system) async {
    final key = await _secure.read(key: 'anthropic_key');
    if (key == null || key.isEmpty) return {'ok': false, 'error': 'no-key'};
    final list = msgs.length > 20 ? msgs.sublist(msgs.length - 20) : msgs;
    final r = await http
        .post(
          Uri.parse('https://api.anthropic.com/v1/messages'),
          headers: {
            'content-type': 'application/json',
            'x-api-key': key,
            'anthropic-version': '2023-06-01',
          },
          body: jsonEncode({
            'model': _model,
            'max_tokens': 1024,
            if (system != null) 'system': system,
            'messages': [
              for (final x in list)
                {
                  'role': x['role'] == 'assistant' ? 'assistant' : 'user',
                  'content': '${x['content']}'.length > 20000
                      ? '${x['content']}'.substring(0, 20000)
                      : '${x['content']}',
                }
            ],
          }),
        )
        .timeout(const Duration(seconds: 60));
    final j = jsonDecode(utf8.decode(r.bodyBytes)) as Map<String, dynamic>;
    if (r.statusCode != 200) {
      return {'ok': false, 'error': (j['error']?['message'] ?? 'HTTP ${r.statusCode}').toString()};
    }
    final text = (j['content'] as List)
        .where((b) => b['type'] == 'text')
        .map((b) => b['text'])
        .join();
    return {'ok': true, 'text': text};
  }

  // ---- UI -----------------------------------------------------------------
  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false, // Android back: let the page handle it first, exit only from Home
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        final r = await _wv.runJavaScriptReturningResult(
            'window.__mobileBack ? window.__mobileBack() : false');
        if (r.toString() != 'true') SystemNavigator.pop();
      },
      child: Scaffold(
        backgroundColor: const Color(0xFF0B3C8C),
        body: SafeArea(
          bottom: false,
          child: Container(
            color: _dark ? const Color(0xFF050E1D) : const Color(0xFFF1F7FE),
            child: SafeArea(top: false, child: WebViewWidget(controller: _wv)),
          ),
        ),
      ),
    );
  }
}
