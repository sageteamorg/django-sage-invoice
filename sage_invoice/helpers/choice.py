from django.db import models


class InvoiceStatus(models.TextChoices):
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
