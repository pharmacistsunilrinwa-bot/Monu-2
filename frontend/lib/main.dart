import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/message_model.dart';
import 'services/connection_service.dart';
import 'services/chat_notifier.dart';
import 'widgets/message_card.dart';

void main() {
  runApp(const ProviderScope(child: MonuAIApp()));
}

class MonuAIApp extends StatelessWidget {
  const MonuAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MONU AI',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const MasterWorkspace(),
    );
  }
}

class MasterWorkspace extends ConsumerStatefulWidget {
  const MasterWorkspace({super.key});

  @override
  ConsumerState<MasterWorkspace> createState() => _MasterWorkspaceState();
}

class _MasterWorkspaceState extends ConsumerState<MasterWorkspace> {
  final ConnectionService _connectionService = ConnectionService();
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _connectionService.dispose();
    super.dispose();
  }

  void _sendMessage() {
    if (_controller.text.isEmpty) return;
    
    // Add User Message
    ref.read(chatStateProvider.notifier).addMessage(MessageModel(
        id: DateTime.now().toString(),
        content: _controller.text,
        type: MessageType.text,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    final messages = ref.watch(chatStateProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('MONU AI'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(40),
          child: StreamBuilder<bool>(
              stream: _connectionService.serverStream,
              builder: (context, snapshot) {
                final isServerConnected = snapshot.data ?? true;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _buildStatus('Internet', true),
                      const SizedBox(width: 20),
                      _buildStatus('Server', isServerConnected),
                    ],
                  ),
                );
              }),
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: messages.length,
              itemBuilder: (context, index) => MessageCard(message: messages[index]),
            ),
          ),
          _buildChatbox(),
        ],
      ),
    );
  }

  Widget _buildStatus(String label, bool connected) {
    return Row(children: [
      Icon(Icons.circle, color: connected ? Colors.green : Colors.red, size: 10),
      const SizedBox(width: 4),
      Text('$label: ${connected ? 'Connected' : 'Disconnected'}', style: const TextStyle(fontSize: 12)),
    ]);
  }

  Widget _buildChatbox() {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(color: Colors.white, border: Border(top: BorderSide(color: Colors.grey.shade300))),
      child: Row(
        children: [
          IconButton(icon: const Icon(Icons.add), onPressed: () {}),
          IconButton(icon: const Icon(Icons.mic), onPressed: () {}),
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(hintText: 'Type message...', border: InputBorder.none),
            ),
          ),
          IconButton(icon: const Icon(Icons.send), onPressed: _sendMessage),
        ],
      ),
    );
  }
}
