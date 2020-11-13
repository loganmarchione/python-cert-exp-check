#!/usr/bin/env python3

import datetime
import ssl
import socket
from cryptography import x509
from prettytable import PrettyTable
x = PrettyTable()

now = datetime.datetime.utcnow()

print("#####\nScript starting!\n#####")
print("STATE: Reading input file at", now)
array = []
with open('hosts.txt') as file:
    array = file.read().splitlines()


def ssl_get_cert(h: str, p: int) -> bytes:
    '''
    Takes in host and port, returns certificate information as dict

    Parameters:
        h (str):    Host to check (can be a hostname or IP address)
        p (int):    Port to check

    Returns:
        bytes       DER-encoded X509 certificate
    '''

    try:
        context = ssl.create_default_context()
        # Needed to check self-signed certs
        context.check_hostname = False
        # Needed for certificates that have already expired
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((h, p)) as sock:
            with context.wrap_socket(sock, server_hostname=h) as sslsock:
                # True=return a DER-encoded certificate, False=return a dict
                # Need to use True to get the DER certificate and then decode it
                print("STATE: Getting cert for", h, "on port", p)
                r = sslsock.getpeercert(True)
                return r
    except Exception as err:
        print("ERROR: Error connecting to", h, err)


def ssl_get_exp_date(c: bytes) -> datetime.datetime:
    '''
    Takes in certficate, returns formatted expiration date

    Parameters:
        c (bytes):    Certificate to check

    Returns:
        datetime      Timestamp in format that can be added/subtracted
                      After:  2021-01-31 12:19:01
    '''

    r = x509.load_der_x509_certificate(c).not_valid_after
    print("STATE: Expiration date is", r)
    return r


def convert_to_days(t: datetime.datetime) -> int:
    '''
    Takes in timestamp, returns days between then and now

    Parameters:
        t (datetime):   Datetime

    Returns:
        int:            Positive or negative number of days until expiration
    '''

    # Get number of days remaining
    r = (t - now).days
    print("STATE: ", r, " days until expiration")
    return r


def build_table() -> str:
    '''Takes no input, just a for loop that builds the table '''

    x.field_names = ["Host", "Port", "Expiration date", "Day(s) remaining"]
    x.sortby = "Day(s) remaining"
    x.align = "l"
    for i in array:
        host = i.split(':')[0]
        port = int(i.split(':')[1])
        cert = ssl_get_cert(host, port)
        exp_date = ssl_get_exp_date(cert)
        days = convert_to_days(exp_date)
        x.add_row([host, port, exp_date, days])
    print("STATE: ASCII version of the table is below")
    print(x)


build_table()
