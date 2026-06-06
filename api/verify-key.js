const fs = require('fs');
const path = require('path');

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

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' });
  
  const { licenseKey } = req.body;
  const keysPath = path.join(process.cwd(), 'license_keys.json');
  
  if (!fs.existsSync(keysPath)) {
    return res.status(200).json({ valid: false, message: 'No keys found' });
  }
  
  try {
    const validKeys = JSON.parse(fs.readFileSync(keysPath, 'utf8'));
    const found = validKeys.find(k => k.key === licenseKey.trim());
    
    if (found) {
      return res.status(200).json({ valid: true, email: found.email });
    } else {
      return res.status(200).json({ valid: false, message: 'Invalid License Key' });
    }
  } catch (error) {
    console.error('Error reading keys:', error);
    return res.status(500).json({ valid: false, error: 'Internal Server Error' });
  }
}
