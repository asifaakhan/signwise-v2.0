import 'package:flutter/material.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

import 'splash.dart';

class LogoSplashScreen extends StatelessWidget {
  const LogoSplashScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (_) => const Splash_screen()));
      },
      child: Scaffold(
        backgroundColor: Color.fromARGB(255, 255, 254, 254),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Expanded(
                child: Align(
                  alignment: Alignment.center,
                  child: Image.asset(
                    'assets/images/spp21.png',
                    width: 280,
                    height: 280,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(bottom: 60.0),
                child: AnimatedTextKit(
                  repeatForever: true,
                  animatedTexts: [
                    ColorizeAnimatedText(
                      'SIGNWISE',
                      textStyle: TextStyle(
                        fontSize: 30.0,
                        fontWeight: FontWeight.bold,
                        fontStyle: FontStyle.italic,
                      ),
                      colors: [
                        Color.fromARGB(255, 130, 173, 208),
                        const Color.fromARGB(255, 35, 74, 107),
                        Color.fromARGB(255, 66, 12, 79),
                      ],
                    ),
                  ],
                  onTap: () {
                    print("Tap Event");
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
