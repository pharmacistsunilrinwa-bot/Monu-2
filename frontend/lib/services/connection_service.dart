import 'dart:async';

class ConnectionService {
  bool _isInternetConnected = true;
  bool _isServerConnected = true;

  final _internetController = StreamController<bool>.broadcast();
  final _serverController = StreamController<bool>.broadcast();

  Stream<bool> get internetStream => _internetController.stream;
  Stream<bool> get serverStream => _serverController.stream;

  bool get isInternetConnected => _isInternetConnected;
  bool get isServerConnected => _isServerConnected;

  ConnectionService() {
    // Simulate periodic checks
    Timer.periodic(const Duration(seconds: 5), (timer) {
      // In production, implement actual ping logic
      _serverController.add(_isServerConnected);
    });
  }

  void updateConnectionStatus(bool internet, bool server) {
    _isInternetConnected = internet;
    _isServerConnected = server;
    _internetController.add(internet);
    _serverController.add(server);
  }

  void dispose() {
    _internetController.close();
    _serverController.close();
  }
}
