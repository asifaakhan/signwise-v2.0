import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'login_screen.dart';

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;

  const CameraScreen({Key? key, required this.camera}) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  String _predictedLabel = '';

  final storage = FlutterSecureStorage();
  bool _isCapturing = false;
  late List<CameraDescription> _cameras;
  int _cameraIndex = 0;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    _cameras = await availableCameras();
    setState(() {}); // Don't initialize the controller until user clicks start.
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  void _startCapturing() async {
    // Initialize the camera only when user starts capturing
    _controller = CameraController(
      _cameras[_cameraIndex],
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller!.initialize();
    await _initializeControllerFuture;

    setState(() {
      _isCapturing = true;
    });

    while (_isCapturing) {
      XFile? imageFile = await _controller!.takePicture();
      List<int> imageBytes = await imageFile.readAsBytes();
      String base64Image = base64Encode(imageBytes);

      final response = await http.post(
        Uri.parse('http://192.168.18.55:5000/get_prediction'),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'image': base64Image}),
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> data = json.decode(response.body);
        String predictedLabel = data['predicted_label'];

        setState(() {
          _predictedLabel = predictedLabel;
        });
      } else {
        print('Failed to get prediction. Status code: ${response.statusCode}');
      }

      await Future.delayed(Duration(milliseconds: 500));
    }
  }

  void _stopCapturing() async {
    setState(() {
      _isCapturing = false;
    });
    // Dispose the controller when stopping capturing
    await _controller?.dispose();
  }

  void _toggleCapture() {
    if (_isCapturing) {
      _stopCapturing();
    } else {
      _startCapturing();
    }
  }

  void _logout(BuildContext context) async {
    try {
      await storage.delete(key: 'jwt_token');

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Logged out successfully'),
        ),
      );
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => LoginScreen()),
        (route) => false,
      );
    } catch (error) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to logout. Please try again.'),
        ),
      );
    }
  }

  void _toggleCamera() async {
    if (_controller != null) {
      await _controller!.dispose();
    }

    setState(() {
      _cameraIndex = (_cameraIndex + 1) % _cameras.length;
      _controller = CameraController(
        _cameras[_cameraIndex],
        ResolutionPreset.medium,
      );
      _initializeControllerFuture = _controller!.initialize();
    });

    if (_isCapturing) {
      _startCapturing();
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        return Scaffold(
          appBar: AppBar(
            title: Text(
              'Sign Recognition',
              style: TextStyle(color: Colors.white),
            ),
            backgroundColor: Color(0xFF1DA6B8),
            iconTheme: IconThemeData(color: Colors.white),
            actions: [
              IconButton(
                onPressed: _toggleCamera,
                icon: Icon(Icons.switch_camera, color: Colors.white),
              ),
            ],
          ),
          body: Stack(
            children: [
              if (_isCapturing &&
                  _controller != null &&
                  _initializeControllerFuture != null)
                Positioned.fill(
                  child: FutureBuilder<void>(
                    future: _initializeControllerFuture,
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.done) {
                        return CameraPreview(_controller!);
                      } else {
                        return Center(child: CircularProgressIndicator());
                      }
                    },
                  ),
                ),
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: Container(
                  padding:
                      EdgeInsets.symmetric(vertical: 2.0, horizontal: 20.0),
                  color: Color(0xFF1DA6B8),
                  child: Row(
                    mainAxisAlignment:
                        MainAxisAlignment.center, // Centering the label
                    children: [
                      Icon(Icons.lightbulb_outline,
                          color: Colors.white, size: 40),
                      SizedBox(
                          width:
                              10.0), // Adjust space between the icon and label
                      Text(
                        '$_predictedLabel',
                        style: TextStyle(
                          fontSize: 50,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 245, 244, 244),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Positioned(
                bottom: constraints.maxHeight * 0.1,
                left: 0,
                right: 0,
                child: Center(
                  child: ElevatedButton(
                    onPressed: _toggleCapture,
                    child: Text(
                        _isCapturing ? 'Stop Capturing' : 'Start Capturing'),
                  ),
                ),
              ),
            ],
          ),
          drawer: Drawer(
            child: Container(
              decoration: const BoxDecoration(
                gradient: LinearGradient(colors: [
                  Color(0xFF1DA6B8),
                  Color(0xFF1DA6B8),
                ]),
              ),
              child: ListView(
                padding: EdgeInsets.zero,
                children: <Widget>[
                  DrawerHeader(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(colors: [
                        Color(0xFF1DA6B8),
                        Color(0xFF1DA6B8),
                      ]),
                    ),
                    child: Row(
                      children: [
                        CircleAvatar(
                          radius: 40,
                          backgroundColor: Colors.white,
                          child: Icon(
                            Icons.person,
                            size: 60,
                            color: Color.fromARGB(255, 10, 120, 134),
                          ),
                        ),
                        SizedBox(width: 10),
                        Text(
                          'Guest',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                  ListTile(
                    leading: Icon(Icons.logout, color: Colors.white),
                    title: Text(
                      'Logout',
                      style: TextStyle(fontSize: 20, color: Colors.white),
                    ),
                    onTap: () {
                      showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AlertDialog(
                            title: Text("Logout"),
                            content: Text("Do you want to logout?"),
                            actions: [
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).pop();
                                },
                                child: Text("No",
                                    style: TextStyle(color: Colors.black)),
                              ),
                              TextButton(
                                onPressed: () {
                                  _logout(context);
                                },
                                child: Text("Yes",
                                    style: TextStyle(color: Colors.black)),
                              ),
                            ],
                          );
                        },
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
