import razorpay
from app.core.config import settings
from fastapi import HTTPException
import hmac
import hashlib

class PaymentService:
    def __init__(self):
        if settings.RAZORPAY_KEY_ID:
            self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        else:
            self.client = None

    def create_order(self, amount: float, currency: str = "INR", notes: dict = {}) -> dict:
        """
        Creates a Razorpay Order. Amount is in main currency unit (e.g. 500 INR),
        Razorpay expects paise (50000).
        """
        if not self.client:
            return {"id": "order_mock_123", "amount": amount * 100, "currency": currency}

        amount_paise = int(amount * 100)
        
        data = {
            "amount": amount_paise,
            "currency": currency,
            "notes": notes, # Can store campaign_id here for easy mapping
            "payment_capture": 1 
        }
        
        try:
            order = self.client.order.create(data=data)
            return order
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Payment Gateway Error: {str(e)}")

    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        """
        Verifies that the webhook came solely from Razorpay using the Secret.
        """
        if not settings.RAZORPAY_KEY_SECRET:
            return True # Dev mode fallback

        try:
            self.client.utility.verify_webhook_signature(
                body.decode('utf-8'),
                signature,
                settings.RAZORPAY_KEY_SECRET
            )
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

payment_service = PaymentService()
