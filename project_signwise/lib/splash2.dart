import 'package:flutter/material.dart';
import 'package:project_signwise/login_screen.dart';

class Splash_screen2 extends StatelessWidget {
  const Splash_screen2({Key? key});

  @override
  Widget build(BuildContext context) {
    final Size screenSize = MediaQuery.of(context).size;
    final double screenWidth = screenSize.width;
    final double screenHeight = screenSize.height;

    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            height: screenHeight * 0.06,
            child: Container(
              color: Color.fromRGBO(29, 166, 184, 1),
            ),
          ),
          Positioned(
            bottom: screenHeight * 0.05,
            right: screenWidth * 0.23,
            child: GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                );
              },
              child: Container(
                height: screenHeight * 0.05,
                width: screenWidth * 0.54,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(screenHeight * 0.025),
                  border: Border.all(color: Colors.black),
                ),
                child: Center(
                  child: Text(
                    'Get Started',
                    style: TextStyle(
                      fontSize: screenHeight * 0.02,
                      color: Colors.black,
                    ),
                  ),
                ),
              ),
            ),
          ),
          Positioned(
            top: screenHeight * 0.05,
            left: 0,
            right: 0,
            child: Image.asset(
              'assets/images/spl25.png',
              width: screenWidth * 0.9,
              height: screenHeight * 0.7,
              fit: BoxFit.contain,
            ),
          ),
          Positioned(
            bottom: screenHeight * 0.13,
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildDot(active: false, screenHeight: screenHeight),
                _buildDot(active: false, screenHeight: screenHeight),
                _buildDot(active: true, screenHeight: screenHeight),
              ],
            ),
          ),
          Positioned(
            top: screenHeight * 0.57,
            left: screenWidth * 0.05,
            right: screenWidth * 0.05,
            child: Center(
              child: Text(
                'Hand Movements to Written Words!',
                style: TextStyle(
                  fontSize: screenHeight * 0.035,
                  fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.bold,
                  color: Color.fromARGB(255, 112, 119, 127),
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
          Positioned(
            top: screenHeight * 0.68,
            left: screenWidth * 0.05,
            right: screenWidth * 0.05,
            child: Center(
              child: Text(
                'Join us on a journey where gestures speak volumes, creating a world where everyone can communicate with ease.',
                style: TextStyle(
                  fontSize: screenHeight * 0.02,
                  fontStyle: FontStyle.italic,
                  color: Color.fromARGB(255, 112, 119, 127),
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDot({required bool active, required double screenHeight}) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 5),
      width: 10,
      height: screenHeight * 0.05,
      decoration: BoxDecoration(
        color: active ? Color.fromRGBO(29, 166, 184, 1) : Colors.grey,
        shape: BoxShape.circle,
      ),
    );
  }
}
