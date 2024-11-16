const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { check, validationResult } = require('express-validator');

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB Atlas Connection
mongoose.connect('mongodb+srv://aqsashamraiz44:PoVFMRDxi9PGTD71@cluster0.txnffe2.mongodb.net/')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error(err));

// User Model
const User = require('./models/User');

// Middleware
app.use(bodyParser.json());

// Validation middleware
const validateRegister = [
  check('name', 'Name is required').not().isEmpty(),
  check('email', 'Please enter a valid email').isEmail(),
  check('password', 'Please enter a password with 6 or more characters').isLength({ min: 6 })
];

// Routes
app.post('/api/register', validateRegister, async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { name, email, password } = req.body;

    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ message: 'User already exists' });
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    user = new User({ name, email, password: hashedPassword }); // Include the name
    await user.save();

    res.status(201).json({ message: 'User registered successfully' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});


app.post('/api/login', [
  check('email', 'Please enter a valid email').isEmail(),
  check('password', 'Password is required').exists()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    const payload = {
      user: {
        id: user.id
      }
    };

    jwt.sign(payload, 'jwtSecret', { expiresIn: '1h' }, (err, token) => {
      if (err) throw err;
      res.json({ token });
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

let blacklist = [];

async function checkToken(req, res, next) {
  const token = req.header('x-auth-token');

  if (!token) return res.status(401).json({ message: 'No token, authorization denied' });

  if (blacklist.includes(token)) {
    return res.status(401).json({ message: 'Token is invalid, please log in again' });
  }

  try {
    const decoded = await jwt.verify(token, 'jwtSecret');

    req.user = decoded.user;
    next();
  } catch (err) {
    res.status(401).json({ message: 'Token is not valid' });
  }
}

app.get('/api/logout', checkToken, async (req, res) => {
  try {
    const token = req.header('x-auth-token');

    if (blacklist.includes(token)) {
      return res.status(401).json({ message: 'Logout unsuccessful. User is already logged out.' });
    }

    blacklist.push(token);

    res.json({ message: 'Logged out successfully' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
