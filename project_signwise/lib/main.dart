import 'package:flutter/material.dart';
import 'package:project_signwise/logo_splash_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color(0xFF1DA6B8),
        ),
        useMaterial3: true,
      ),
      home: LogoSplashScreen(),
    );
  }
}
