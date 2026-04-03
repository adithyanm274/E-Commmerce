import logging
import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

logger = logging.getLogger(__name__)

class ResendEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        resend.api_key = settings.RESEND_API_KEY
        logger.info("ResendEmailBackend initialized")

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        num_sent = 0
        for message in email_messages:
            try:
                params = {
                    "from": sanitize_address(message.from_email, message.encoding),
                    "to": [sanitize_address(addr, message.encoding) for addr in message.to],
                    "subject": message.subject,
                    "html": message.body,
                }
                logger.info(f"Sending email to {params['to']} via Resend")
                resend.Emails.send(params)
                num_sent += 1
                logger.info("Email sent successfully")
            except Exception as e:
                logger.error(f"Resend email failed: {type(e).__name__} - {str(e)}")
                if not self.fail_silently:
                    raise e
        return num_sent