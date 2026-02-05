from email.headerregistry import Address, AddressHeader

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.utils.encoding import force_str, punycode


class PowerAutomateEmailBackend(BaseEmailBackend):
    """
    Email Backend that uses Microsoft Power Automate Email Notification to send emails in Django
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently, **kwargs)
        self.api_url = settings.POWER_AUTOMATE_URL

    def sendmail(self, subject, recipients, message: str):
        """
        Makes the post request to Power Automate
        Works with one recipient email for now
        """

        body = {"subject": subject, "recipient": recipients[0], "message": message}
        try:
            response = requests.post(self.api_url, json=body)
            if response.status_code != 200:
                raise Exception(
                    "Response is not 200, email must have failed to send, check power automate flow logs"
                )
        except Exception as e:
            # Do exponential back-off retry later
            raise

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0

        num_sent = 0
        try:
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        finally:
            if num_sent == len(email_messages):
                print("SENT!")
            else:
                print("FALSE!")

        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False

        recipients = [*map(self.prep_address, email_message.recipients())]
        message = email_message.body
        subject = email_message.subject
        try:
            self.sendmail(subject, recipients, message)
        except Exception:
            if not self.fail_silently:
                raise
            return False
        return True

    def prep_address(self, address, force_ascii=True):
        """
        Return the addr-spec portion of an email address. Raises ValueError for
        invalid addresses, including CR/NL injection.

        If force_ascii is True, apply IDNA encoding to non-ASCII domains, and
        raise ValueError for non-ASCII local-parts (which can't be encoded).
        Otherwise, leave Unicode characters unencoded (e.g., for sending with
        SMTPUTF8).
        """
        address = force_str(address)
        parsed = AddressHeader.value_parser(address)
        defects = set(str(defect) for defect in parsed.all_defects)
        # Django allows local mailboxes like "From: webmaster" (#15042).
        defects.discard("addr-spec local part with no domain")
        if not force_ascii:
            # Non-ASCII local-part is valid with SMTPUTF8. Remove once
            # https://github.com/python/cpython/issues/81074 is fixed.
            defects.discard("local-part contains non-ASCII characters)")
        if defects:
            raise ValueError(f"Invalid address {address!r}: {'; '.join(defects)}")

        mailboxes = parsed.all_mailboxes
        if len(mailboxes) != 1:
            raise ValueError(f"Invalid address {address!r}: must be a single address")

        mailbox = mailboxes[0]
        if force_ascii and mailbox.domain and not mailbox.domain.isascii():
            # Re-compose an addr-spec with the IDNA encoded domain.
            domain = punycode(mailbox.domain)
            return str(Address(username=mailbox.local_part, domain=domain))
        else:
            return mailbox.addr_spec
