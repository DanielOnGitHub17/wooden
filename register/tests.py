from django.conf import settings
from django.core.mail import send_mail
from django.test import TestCase


class PowerAutomateEmailBackendTests(TestCase):
    """Tests for the PowerAutomateEmailBackend email backend"""

    def test_send_mail_to_dev_mails(self):
        """Test sending real email using send_mail to DEV_MAILS"""
        num_sent = send_mail(
            subject="Test Email from Django Tests",
            message="This is a real test message sent from the email backend tests.",
            from_email="noreply@example.com",
            recipient_list=settings.DEV_MAILS,
        )

        self.assertEqual(num_sent, len(settings.DEV_MAILS))
