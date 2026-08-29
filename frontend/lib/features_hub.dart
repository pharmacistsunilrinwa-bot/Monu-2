import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class FeaturesHubScreen extends StatefulWidget {
  final String baseUrl;
  const FeaturesHubScreen({super.key, required this.baseUrl});

  @override
  State<FeaturesHubScreen> createState() => _FeaturesHubScreenState();
}

class _FeaturesHubScreenState extends State<FeaturesHubScreen> {
  List<dynamic> _tools = [];
  List<dynamic> _filteredTools = [];
  final TextEditingController _searchController = TextEditingController();
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchTools();
  }

  Future<void> _fetchTools() async {
    try {
      final response = await http.get(Uri.parse("${widget.baseUrl}/tools"));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _tools = data['tools'];
          _filteredTools = _tools;
          _isLoading = false;
        });
      }
    } catch (e) {
      debugPrint("Error fetching tools: $e");
      setState(() => _isLoading = false);
    }
  }

  void _filterTools(String query) {
    setState(() {
      _filteredTools = _tools.where((tool) {
        return tool['name'].toString().toLowerCase().contains(query.toLowerCase()) ||
               tool['description'].toString().toLowerCase().contains(query.toLowerCase());
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: TextField(
            controller: _searchController,
            onChanged: _filterTools,
            decoration: InputDecoration(
              hintText: "Search features...",
              prefixIcon: const Icon(Icons.search),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(25)),
              filled: true,
            ),
          ),
        ),
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : ListView.builder(
                  itemCount: _filteredTools.length,
                  itemBuilder: (context, index) {
                    final tool = _filteredTools[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      child: ListTile(
                        title: Text(tool['name']),
                        subtitle: Text(tool['description'], maxLines: 2, overflow: TextOverflow.ellipsis),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () {
                          _executeTool(tool);
                        },
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }

  void _executeTool(dynamic tool) {
    final Map<String, TextEditingController> argControllers = {};
    final Map<String, dynamic> arguments = tool['arguments'] ?? {};

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Run ${tool['name']}"),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(tool['description']),
              const SizedBox(height: 10),
              ...arguments.entries.map((entry) {
                argControllers[entry.key] = TextEditingController();
                return TextField(
                  controller: argControllers[entry.key],
                  decoration: InputDecoration(labelText: entry.key),
                );
              }),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(context);
              _runToolAction(tool, argControllers);
            },
            child: const Text("Execute"),
          ),
        ],
      ),
    );
  }

  Future<void> _runToolAction(dynamic tool, Map<String, TextEditingController> argControllers) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator()),
    );

    final Map<String, String> args = {};
    argControllers.forEach((key, controller) {
      args[key] = controller.text;
    });

    try {
      final body = {
        "message": "Run tool ${tool['name']} with arguments $args",
        "user_id": "default",
      };

      final response = await http.post(
        Uri.parse("${widget.baseUrl}/chat"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      ).timeout(const Duration(seconds: 45));

      Navigator.pop(context); // Remove loader

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _showResult(tool['name'], data['response']);
      } else {
        _showResult(tool['name'], "Error: ${response.statusCode}");
      }
    } catch (e) {
      Navigator.pop(context);
      _showResult(tool['name'], "Exception: $e");
    }
  }

  void _showResult(String toolName, String result) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Result: $toolName"),
        content: SingleChildScrollView(child: Text(result)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Close")),
        ],
      ),
    );
  }
}
