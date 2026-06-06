export default async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { licenseKey } = req.body;

  if (!licenseKey) {
    return res.status(400).json({ valid: false, message: 'License key is required' });
  }

  try {
    // قائمة المفاتيح الصالحة
    const validKeys = [
      // أضف مفاتيح الاختبار هنا
      "FL-DCDC28BA7863ECD0",
      // سيتم إضافة المفاتيح الجديدة بعد كل عملية شراء
    ];

    const isValid = validKeys.includes(licenseKey.trim());

    return res.status(200).json({
      valid: isValid,
      message: isValid ? 'License key validated' : 'Invalid license key'
    });
  } catch (error) {
    console.error('Verification error:', error);
    return res.status(500).json({ valid: false, error: 'Internal server error' });
  }
}
