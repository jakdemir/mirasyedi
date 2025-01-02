import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: FamilyTreePage(),
    );
  }
}

class FamilyTreePage extends StatefulWidget {
  @override
  _FamilyTreePageState createState() => _FamilyTreePageState();
}

class _FamilyTreePageState extends State<FamilyTreePage> {
  //final String apiUrl = 'http://127.0.0.1:8000/calculate-inheritance';
  final String apiUrl = 'https://inheritance-backend-437307451072.us-west1.run.app/calculate-inheritance';
  List<Map<String, String>> familyMembers = [];
  String result = '';

  void _addFamilyMember() {
    setState(() {
      familyMembers.add({'name': 'New Member', 'relation': 'child'});
    });
  }

  Future<void> _calculateInheritance() async {
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'total_value': 100000,
        'heirs': familyMembers,
      }),
    );

    if (response.statusCode == 200) {
      setState(() {
        result = response.body;
      });
    } else {
      setState(() {
        result = 'Error: ${response.statusCode}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Family Tree')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: familyMembers.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(familyMembers[index]['name'] ?? ''),
                  subtitle: Text(familyMembers[index]['relation'] ?? ''),
                );
              },
            ),
          ),
          ElevatedButton(
            onPressed: _addFamilyMember,
            child: Text('Add Family Member'),
          ),
          ElevatedButton(
            onPressed: _calculateInheritance,
            child: Text('Calculate Inheritance'),
          ),
          Text(result),
        ],
      ),
    );
  }
}
