import 'package:flutter/material.dart';
import '../models/message_model.dart';
import 'code_card.dart';

class MessageCard extends StatelessWidget {
  final MessageModel message;

  const MessageCard({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    Color bubbleColor;
    switch (message.type) {
      case MessageType.error:
        bubbleColor = Colors.red.shade100;
        break;
      case MessageType.status:
        bubbleColor = Colors.amber.shade100;
        break;
      default:
        bubbleColor = message.isUser ? Colors.blue.shade100 : Colors.grey.shade200;
    }

    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 10),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: bubbleColor,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Contextual Rendering
            message.type == MessageType.text && message.content.contains('```') 
              ? CodeCard(code: message.content)
              : Text(message.content, style: const TextStyle(fontSize: 16)),

            if (message.type != MessageType.status) ...[
              const SizedBox(height: 5),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextButton(onPressed: () {}, child: const Text('Copy', style: TextStyle(fontSize: 10))),
                  TextButton(onPressed: () {}, child: const Text('Share', style: TextStyle(fontSize: 10))),
                ],
              )
            ]
          ],
        ),
      ),
    );
  }
}

