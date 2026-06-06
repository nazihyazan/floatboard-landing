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

  const LEMON_SQUEEZY_API_KEY = process.env.LEMON_SQUEEZY_API_KEY;

  if (!LEMON_SQUEEZY_API_KEY) {
    console.error('LEMON_SQUEEZY_API_KEY is not set in environment variables');
    return res.status(500).json({ valid: false, error: 'Server configuration error' });
  }

  try {
    const response = await fetch('https://api.lemonsqueezy.com/v1/licenses/validate', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': `Bearer ${LEMON_SQUEEZY_API_KEY}`
      },
      body: JSON.stringify({ license_key: licenseKey.trim() })
    });
    
    const data = await response.json();
    const isValid = data.valid === true;

    return res.status(200).json({
      valid: isValid,
      message: isValid ? 'License key validated' : 'Invalid license key'
    });
  } catch (error) {
    console.error('Verification error:', error);
    return res.status(500).json({ valid: false, error: 'Internal server error' });
  }
}
