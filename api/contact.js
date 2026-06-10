export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, message } = req.body;
    
    if (!message || !email) {
      return res.status(400).json({ error: 'Email and message are required' });
    }

    // Forward the email to FormSubmit to hide the recipient email address
    const response = await fetch('https://formsubmit.co/ajax/nazihyazan7@gmail.com', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        name: name || 'FloatBoard User',
        email: email,
        message: message,
        _subject: 'New Support Request for FloatBoard'
      })
    });

    if (response.ok) {
      return res.status(200).json({ success: true });
    } else {
      console.error('FormSubmit Error:', await response.text());
      return res.status(500).json({ error: 'Failed to send message' });
    }
  } catch (error) {
    console.error('Contact API Error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
