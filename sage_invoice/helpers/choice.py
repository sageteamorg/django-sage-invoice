from django.db import models


class InvoiceStatus(models.TextChoices):
    """
    This class defines the possible statuses for an invoice in the system.

    - **DRAFT**: The invoice is saved but has not yet been sent to the customer. 
        This is the initial state when an invoice is being created and hasn't been 
        finalized or issued.

    - **OVERDUE**: The invoice was sent, but the payment due date has passed, and 
        payment has not been received. It indicates that the customer is late in making 
        the payment.

    - **PAID**: The invoice has been fully paid by the customer. No further action is 
        required from either party.

    - **UNPAID**: The invoice has been sent to the customer (via email or manual download). 
        It has not been paid yet, but it is now awaiting customer action. The invoice 
        is still pending and has not yet been paid. This status includes invoices that
        are still within  the payment period and those that might require follow-up 
        (before they become overdue).
    """
    DRAFT = ("draft", "DRAFT")
    OVERDUE = ("overdue", "OVERDUE")
    PAID = ("paid", "PAID")
    UNPAID = ("unpaid", "UNPAID")


class Currency(models.TextChoices):
    USD = ("USD", "US Dollar")
    EUR = ("EUR", "Euro")
    GBP = ("GBP", "British Pound")
    JPY = ("JPY", "Japanese Yen")
    AUD = ("AUD", "Australian Dollar")
    CAD = ("CAD", "Canadian Dollar")
    CHF = ("CHF", "Swiss Franc")
    CNY = ("CNY", "Chinese Yuan")
    INR = ("INR", "Indian Rupee")
    RUB = ("RUB", "Russian Ruble")
    AED = ("AED", "UAE Dirham")
    SAR = ("SAR", "Saudi Riyal")
    TRY = ("TRY", "Turkish Lira")
    BRL = ("BRL", "Brazilian Real")
    ZAR = ("ZAR", "South African Rand")
    NZD = ("NZD", "New Zealand Dollar")
    KRW = ("KRW", "South Korean Won")
    SGD = ("SGD", "Singapore Dollar")
    MXN = ("MXN", "Mexican Peso")
    IRR = ("IRR", "Iranian Rial")
    TOMAN = ("TOMAN", "Iranian Toman")
    QAR = ("QAR", "Qatari Riyal")
    KWD = ("KWD", "Kuwaiti Dinar")
    BHD = ("BHD", "Bahraini Dinar")
    OMR = ("OMR", "Omani Rial")
    EGP = ("EGP", "Egyptian Pound")
