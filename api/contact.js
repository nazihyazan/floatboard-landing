export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, message } = req.body;
    
    if (!message || !email) {
      return res.status(400).json({ error: 'Email and message are required' });
    }

    // Forward the email to FormSubmit using the secure random string
    const response = await fetch('https://formsubmit.co/ajax/5f7a532cf82e3d1eb01c14d4e84c52ca', {
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
