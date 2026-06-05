const nodemailer = require('nodemailer');
const crypto = require('crypto');

// دالة لتوليد مفتاح ترخيص وهمي
function generateLicenseKey() {
  return 'FL-' + crypto.randomBytes(8).toString('hex').toUpperCase();
}

export default async function handler(req, res) {
  // السماح فقط بطلبات POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { payerEmail, payerName, orderID } = req.body;

  // التحقق من وجود البريد الإلكتروني
  if (!payerEmail) {
    return res.status(400).json({ error: 'Missing payer email' });
  }

  // 1. توليد المفتاح
  const licenseKey = generateLicenseKey();

  // 2. إعداد خدمة إرسال الإيميلات (باستخدام Gmail)
  let transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER, // متغير البيئة
      pass: process.env.EMAIL_PASS  // متغير البيئة (كلمة مرور التطبيق)
    }
  });

  try {
    // 3. إرسال الإيميل
    await transporter.sendMail({
      from: '"FloatBoard" <' + process.env.EMAIL_USER + '>',
      to: payerEmail,
      subject: 'Your FloatBoard Premium License Key',
      text: `Hello ${payerName || 'there'},\n\nThank you for purchasing FloatBoard Premium! Here is your lifetime license key:\n\n${licenseKey}\n\nTo activate, open FloatBoard, go to Settings > Enter License Key, and paste this key.\n\nEnjoy unlimited access!\n\n- FloatBoard Team`,
      html: `<p>Hello ${payerName || 'there'},</p><p>Thank you for purchasing <strong>FloatBoard Premium</strong>! Here is your lifetime license key:</p><h2>${licenseKey}</h2><p>To activate, open <strong>FloatBoard</strong>, go to <strong>Settings &gt; Enter License Key</strong>, and paste this key.</p><p>Enjoy unlimited access!</p><p>- FloatBoard Team</p>`
    });

    // 4. إرسال تأكيد للمستخدم في المتصفح
    res.status(200).json({ success: true, message: 'License Key sent to your email!' });
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ success: false, error: 'Failed to send email.' });
  }
}
