enum MessageType { text, status, file, error }

class MessageModel {
  final String id;
  final String content;
  final MessageType type;
  final bool isUser;
  final DateTime timestamp;

  MessageModel({
    required this.id,
    required this.content,
    required this.type,
    required this.isUser,
    required this.timestamp,
  });
}
