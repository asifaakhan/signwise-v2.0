import 'package:flutter/material.dart';
import 'package:project_signwise/splash.dart';
import 'package:project_signwise/splash2.dart';

class Splash_screen1 extends StatelessWidget {
  const Splash_screen1({Key? key});

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
            right: screenWidth * 0.05,
            child: GestureDetector(
              onTap: () {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const Splash_screen2()),
                );
              },
              child: Container(
                height: screenHeight * 0.05,
                width: screenWidth * 0.26,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(screenHeight * 0.03),
                  border: Border.all(color: Colors.black),
                ),
                child: Center(
                  child: Text(
                    'Next',
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
            bottom: screenHeight * 0.05,
            left: screenWidth * 0.05,
            child: GestureDetector(
              onTap: () {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const Splash_screen()),
                );
              },
              child: Container(
                height: screenHeight * 0.05,
                width: screenWidth * 0.26,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(screenHeight * 0.03),
                  border: Border.all(color: Colors.black),
                ),
                child: Center(
                  child: Text(
                    'Back',
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
            top: screenHeight * 0.0,
            left: screenWidth * 0.05,
            right: screenWidth * 0.05,
            child: Image.asset(
              'assets/images/spp1.png',
              width: screenWidth * 0.16,
              height: screenHeight * 0.8,
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
                _buildDot(active: false),
                _buildDot(active: true),
                _buildDot(active: false),
              ],
            ),
          ),
          Positioned(
            top: screenHeight * 0.55,
            right: screenWidth * 0.05,
            left: screenWidth * 0.05,
            child: Center(
              child: Text(
                'Signs to Scripts in Seconds!',
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
            top: screenHeight * 0.65,
            left: screenWidth * 0.05,
            right: screenWidth * 0.05,
            child: Center(
              child: Text(
                'Instantly convert sign language gestures into understandable Urdu text on your mobile screen, bridging communication gaps effortlessly.',
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

  Widget _buildDot({required bool active}) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 5),
      width: 10,
      height: 80,
      decoration: BoxDecoration(
        color: active ? Color.fromRGBO(29, 166, 184, 1) : Colors.grey,
        shape: BoxShape.circle,
      ),
    );
  }
}
