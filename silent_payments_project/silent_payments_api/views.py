from django.shortcuts import render

# Create your views here.
# silent_payments_api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import hashlib
import ecdsa
from bech32 import bech32_encode, convertbits

# Constants
G = ecdsa.SECP256k1.generator
N = ecdsa.SECP256k1.order

def sha256(data):
    return hashlib.sha256(data).digest()

def hash_bip352_label(data):
    tag = sha256(b"BIP0352/Label")
    return sha256(tag + tag + data)

def generate_private_key():
    return os.urandom(32)

def generate_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return vk.to_string("compressed")

def tweak_public_key(public_key, tweak):
    point = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1).pubkey.point
    tweak_point = int.from_bytes(tweak, byteorder='big') * G
    new_point = point + tweak_point
    new_pubkey = ecdsa.VerifyingKey.from_public_point(new_point, curve=ecdsa.SECP256k1)
    return new_pubkey.to_string("compressed")

def generate_silent_payment_address(bscan, bscan_priv, bm, label=None):
    # Calculate Bm with optional label
    if label is not None:
        tweak = hash_bip352_label(bscan_priv.to_bytes(32, 'big') + label.to_bytes(4, 'big'))
        bm = tweak_public_key(bm, tweak)

    # Create Bech32m address
    hrp = "sp"
    version_byte = 0
    data = bytes([version_byte]) + bscan + bm
    converted = convertbits(data, 8, 5)
    return bech32_encode(hrp, converted)

def final_address():
    # Generate bscan (scan public key) and bscan_priv (scan private key)
    bscan_priv = int.from_bytes(generate_private_key(), byteorder='big')
    bscan = generate_public_key(bscan_priv.to_bytes(32, 'big'))

    # Generate bspend (spend public key)
    bspend_priv = int.from_bytes(generate_private_key(), byteorder='big')
    bspend = generate_public_key(bspend_priv.to_bytes(32, 'big'))

    # Generate silent payment address
    label = 1  # Optional label
    silent_payment_address = generate_silent_payment_address(bscan, bscan_priv, bspend, label)

    print("Silent Payment Address:", silent_payment_address)
    return silent_payment_address


@api_view(['GET'])
def generate_silent_payment(request):
    
    address = final_address()
    return Response({'address': address})
