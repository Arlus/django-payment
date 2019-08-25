import random
from datetime import datetime
import ccy


def verify_site(site):
    """
    The site number (POS) is typically privided by the bank to the merchant
    It is required for any contact with our Sales service or Technical and client Helpdesk
    Its length should be 7 digits
    :return: bool
    """
    if len(site) == 7 and site.isdigit():
        return True
    return False


def verify_rang(rang):
    """
    This is the rank number (or « machine ») provided by the bank to the merchant
    It is required for any contact with our Sales service or Technical and client Helpdesk
    Its length should be 2 digits
    :return: bool
    """
    if len(rang) == 2 and rang.isdigit():
        return True
    return False


def verify_identifiant(identifiant):
    """
    This is the paybbox customer ID
    It is required for any contact with our Sales service or Technical and client Helpdesk
    Its length should be between 1 and 9 digits
    :return: bool
    """
    if 1 < len(identifiant) <= 9 and identifiant.isdigit():
        return True
    return False


def verify_cle(cle):
    """
    This field allows to authenticate the originator of the request and allows for additional
    security for the PPPS exchange of messages.
    The value for this parameter corresponds to the password for the merchant backoffice that is provided by the
    technical support upon the creation of the merchant account on the Paybox platform.
    Its length should be 10 characters
    :return: bool
    """
    if len(cle) == 10:
        return True
    return False


def verify_amount(amount):
    """
    Amount should be a string of digits
    :param amount: str
    :return: bool
    """
    if amount.isdigit():
        return True
    return False


def get_amount_for_paybox(amount):
    """
    Get appropriate amount for Paybox.
    Paybox requires all amounts in cents.
    The length of the amount should be 10 digits
    :param amount: str
    :return: str
    """
    paybox_amount = str(int(amount) * 100)

    return paybox_amount.zfill(10)


def get_amount_from_paybox(amount):
    """
    Get appropriate amount from Paybox.
    We divide by 100 since Paybox handles amounts in cents
    :param amount: str
    :return: str
    """
    return str(int(amount)/100)


def get_currency_for_paybox(currency):
    """
    Convert Saleor's currency format to Paybox currency format.
    Paybox currency is using numeric code (ISO 4217) while Saleor is using lowercase string.
    :param currency: str
    :return: str
    """
    currency = ccy.currency(currency)
    return currency.isonumber


def get_currency_from_paybox(currency):
    """
    Convert Paybox currency format to Saleor currency format.
    Paybox currency is using numeric code (ISO 4217) while Saleor is using lowercase string.
    :param currency: str
    :return: str
    """
    currency = ccy.currency(currency)
    return currency.code.lower()


def __uniqueid__():
    """
      generate unique id with length 17 to 21.
      ensure uniqueness even with daylight savings events (clocks adjusted one-hour backward).

      if you generate 1 million ids per second during 100 years, you will generate
      2*25 (approx sec per year) * 10**6 (1 million id per sec) * 100 (years) = 5 * 10**9 unique ids.

      with 17 digits (radix 16) id, you can represent 16**17 = 295147905179352825856 ids (around 2.9 * 10**20).
      In fact, as we need far less than that, we agree that the format used to represent id (seed + timestamp reversed)
      do not cover all numbers that could be represented with 35 digits (radix 16).

      if you generate 1 million id per second with this algorithm, it will increase the seed by less than 2**12 per hour
      so if a DST occurs and backward one hour, we need to ensure to generate unique id for twice times for the same period.
      the seed must be at least 1 to 2**13 range. if we want to ensure uniqueness for two hours (100% contingency), we need
      a seed for 1 to 2**14 range. that's what we have with this algorithm. You have to increment seed_range_bits if you
      move your machine by airplane to another time zone or if you have a glucky wallet and use a computer that can generate
      more than 1 million ids per second.

      one word about predictability : This algorithm is absolutely NOT designed to generate unpredictable unique id.
      you can add a sha-1 or sha-256 digest step at the end of this algorithm but you will loose uniqueness and enter to collision probability world.
      hash algorithms ensure that for same id generated here, you will have the same hash but for two differents id (a pair of ids), it is
      possible to have the same hash with a very little probability. You would certainly take an option on a bijective function that maps
      35 digits (or more) number to 35 digits (or more) number based on cipher block and secret key. read paper on breaking PRNG algorithms
      in order to be convinced that problems could occur as soon as you use random library :)

      1 million id per second ?... on a Intel(R) Core(TM)2 CPU 6400 @ 2.13GHz, you get :

      >>> timeit.timeit(uniqueid,number=40000)
      1.0114529132843018

      an average of 40000 id/second
    """
    mynow = datetime.now
    sft = datetime.strftime
    # store old datetime each time in order to check if we generate during same microsecond (glucky wallet !)
    # or if daylight savings event occurs (when clocks are adjusted backward) [rarely detected at this level]
    old_time = mynow()  # fake init - on very speed machine it could increase your seed to seed + 1... but we
    # have our contingency :)
    # manage seed
    seed_range_bits = 14  # max range for seed
    seed_max_value=2**seed_range_bits - 1 # seed could not exceed 2**nbbits - 1
    # get random seed
    seed = random.getrandbits(seed_range_bits)
    current_seed=str(seed)
    # producing new ids
    while True:
        # get current time
        current_time = mynow()
        if current_time <= old_time:
            # previous id generated in the same microsecond or Daylight saving time event occurs
            # (when clocks are adjusted backward)
            seed = max(1,(seed + 1) % seed_max_value)
            current_seed=str(seed)
        # generate new id (concatenate seed and timestamp as numbers)
        newid = int(''.join([sft(current_time, '%f%S%M%H%d%m%Y'), current_seed]))
        # save current time
        old_time = current_time
        # return a new id
        yield newid
