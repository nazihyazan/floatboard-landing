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

  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  const LEMON_SQUEEZY_API_KEY = process.env.LEMON_SQUEEZY_API_KEY;
  const LEMON_SQUEEZY_STORE_ID = '99219';
  const LEMON_SQUEEZY_VARIANT_ID = '118249';

  if (!LEMON_SQUEEZY_API_KEY) {
    console.error('LEMON_SQUEEZY_API_KEY is not set in environment variables');
    return res.status(500).json({ error: 'Server configuration error' });
  }

  try {
    const response = await fetch('https://api.lemonsqueezy.com/v1/checkouts', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': `Bearer ${LEMON_SQUEEZY_API_KEY}`
      },
      body: JSON.stringify({
        data: {
          type: 'checkouts',
          attributes: {
            checkout_data: { email: email },
            product_options: {
              redirect_url: 'https://floatboard.xyz' // Redirecting back to landing page
            }
          },
          relationships: {
            store: { data: { type: 'stores', id: LEMON_SQUEEZY_STORE_ID } },
            variant: { data: { type: 'variants', id: LEMON_SQUEEZY_VARIANT_ID } }
          }
        }
      })
    });
    
    if (!response.ok) {
      throw new Error(`Lemon Squeezy API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!data.data || !data.data.attributes || !data.data.attributes.url) {
        throw new Error("Invalid response from Lemon Squeezy");
    }

    return res.status(200).json({
      url: data.data.attributes.url
    });
  } catch (error) {
    console.error('Error creating checkout:', error);
    return res.status(500).json({ error: 'Failed to create checkout URL' });
  }
}
