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
          home: InheritanceCalculator(),
        );
      }
    }

    class InheritanceCalculator extends StatefulWidget {
      @override
      _InheritanceCalculatorState createState() => _InheritanceCalculatorState();
    }

    class _InheritanceCalculatorState extends State<InheritanceCalculator> {
      //String apiUrl = 'http://127.0.0.1:8000/calculate-inheritance';
      String apiUrl = 'https://inheritance-backend-437307451072.us-west1.run.app/calculate-inheritance';
      String result = '';

      Future<void> calculateInheritance() async {
        final response = await http.post(
          Uri.parse(apiUrl),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'total_value': 100000,
            'heirs': [
              {'name': 'Alice', 'relation': 'spouse'},
              {'name': 'Bob', 'relation': 'child'},
              {'name': 'Charlie', 'relation': 'child'}
            ]
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
          appBar: AppBar(title: Text('Inheritance Calculator')),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: calculateInheritance,
                  child: Text('Calculate Inheritance'),
                ),
                SizedBox(height: 20),
                Text(result),
              ],
            ),
          ),
        );
      }
    }
