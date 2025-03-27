// server.js
const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');

const app = express();
app.use(bodyParser.json());

// Create a transporter using your Gmail credentials
const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com', // Gmail SMTP server
  port: 587,              // TLS port
  secure: false,          // true for port 465, false for others
  auth: {
    user: 'your-email@gmail.com',      // Replace with your Gmail address
    pass: 'your-email-password-or-app-password', // Replace with your Gmail password or App Password if using 2FA
  },
});

// Endpoint to send OTP
app.post('/send-otp', async (req, res) => {
  const { email } = req.body;
  if (!email) {
    return res.status(400).json({ success: false, message: 'Email is required' });
  }

  // Generate a random 4-digit OTP
  const otpCode = Math.floor(1000 + Math.random() * 9000).toString();

  const mailOptions = {
    from: '"Tour 365" <your-email@gmail.com>',
    to: email,
    subject: 'Your OTP Code',
    text: `Your OTP code is ${otpCode}`,
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Message sent: %s', info.messageId);
    // You can store the OTP in a database or in a session for later verification.
    res.json({ success: true, message: 'OTP sent', otp: otpCode });
  } catch (error) {
    console.error('Error sending OTP email:', error);
    res.json({ success: false, message: 'Failed to send OTP' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
