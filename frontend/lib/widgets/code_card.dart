import 'package:flutter/material.dart';
import '../models/message_model.dart';

class CodeCard extends StatelessWidget {
  final String code;
  const CodeCard({super.key, required this.code});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(8)),
      child: Text(code, style: const TextStyle(fontFamily: 'monospace', color: Colors.greenAccent)),
    );
  }
}
