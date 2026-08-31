import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/message_model.dart';

// Provider for message state
final chatStateProvider = StateNotifierProvider<ChatNotifier, List<MessageModel>>((ref) {
  return ChatNotifier();
});

class ChatNotifier extends StateNotifier<List<MessageModel>> {
  ChatNotifier() : super([]);

  // In a real app, integrate WebSockets or REST here to push states
  void addMessage(MessageModel message) {
    state = [...state, message];
  }

  void updateMessageStatus(String id, MessageType newType, String newContent) {
    state = [
      for (final msg in state)
        if (msg.id == id)
          MessageModel(
            id: msg.id,
            content: newContent,
            type: newType,
            isUser: msg.isUser,
            timestamp: msg.timestamp,
          )
        else
          msg
    ];
  }
}
