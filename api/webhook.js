export default async function handler(req, res) {
  // 1. كنتأكدو بلي الطلب جاي من Paddle (POST Request)
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    // 2. كنجبدو الإيميل ديال الكليان اللي خلص في Paddle
    const eventData = req.body.data;
    // إيلا مالقاش الإيميل لأي سبب، غيستعمل إيميل افتراضي باش ما يحبسش
    const customerEmail = eventData?.customer?.email || 'test@example.com'; 

    // 3. كنتواصلو مع Keygen باش نصاوبو كود التفعيل (License Key)
    const keygenResponse = await fetch(`https://api.keygen.sh/v1/accounts/${process.env.KEYGEN_ACCOUNT_ID}/licenses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': `Bearer ${process.env.KEYGEN_PRODUCT_TOKEN}`
      },
      body: JSON.stringify({
        data: {
          type: 'licenses',
          attributes: {},
          relationships: {
            policy: {
              data: { type: 'policies', id: process.env.KEYGEN_POLICY_ID }
            }
          }
        }
      })
    });

    const keygenData = await keygenResponse.json();
    
    // إيلا وقع شي مشكل في إنشاء الكود
    if (keygenData.errors) {
        console.error('Keygen Error:', keygenData.errors);
        return res.status(500).json({ error: 'Failed to create license' });
    }

    // هادا هو الكود اللي غيتعطى للكليان
    const licenseKey = keygenData.data.attributes.key;

    // 4. كنصيفطو الكود في الإيميل للكليان عبر منصة Resend
    const resendResponse = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`
      },
      body: JSON.stringify({
        from: 'FloatBoard <onboarding@resend.dev>', // إيميل التجريب ديال Resend
        to: [customerEmail],
        subject: 'FloatBoard Premium - Your License Key 🚀',
        html: `
          <div style="font-family: sans-serif; color: #333;">
            <h2>Thank you for your purchase! 🎉</h2>
            <p>Your payment was successful. Here is your Lifetime Premium License Key for FloatBoard:</p>
            <h3 style="background: #f4f4f5; padding: 15px; border-radius: 8px; display: inline-block; letter-spacing: 2px;">
              ${licenseKey}
            </h3>
            <p>Keep this key safe. You can use it to activate the premium features in the app.</p>
            <p>Enjoy! <br> - FloatBoard Team</p>
          </div>
        `
      })
    });

    // 5. كنجاوبو Paddle بلي العملية دازت بنجاح باش يسدو الطلب
    return res.status(200).json({ message: 'Webhook processed successfully!', key: licenseKey });

  } catch (error) {
    console.error('Webhook Error:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
