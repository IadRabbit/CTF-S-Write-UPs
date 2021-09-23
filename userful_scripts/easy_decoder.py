#!/usr/bin/python3

from base64 import b64decode
from argparse import ArgumentParser

encoder_avalaibles = (
	"base64", "ascii", "hex"
)

parser = ArgumentParser(
	description = "A python cyberchef"
)

parser.add_argument(
	"encoder",
	help = "String encode",
	choices = encoder_avalaibles
)

parser.add_argument(
	"string",
	help = "String to decode"
)

args = parser.parse_args()
encoder = args.encoder
to_decode = args.string

def base64_decode(to_decode):
	decoded = b64decode(to_decode).decode()

	return decoded

def ascii_decode(to_decode):
	l_chars = (
		map(
			int, to_decode.split(" ")
		)
	)

	decoded = ""

	for char in l_chars:
		decoded += chr(char)

	return decoded

def hex_decode(to_decode):
	l_chars = (
		map(
			str, to_decode.split(" ")
		)
	)

	decoded = ""

	for char in l_chars:
		ascii_num = int(char, 16)
		decoded += chr(ascii_num)

	return decoded

if encoder == encoder_avalaibles[0]:
	decoder_func = base64_decode
elif encoder == "hex":
	decoder_func = hex_decode
elif encoder == "ascii":
	decoder_func = ascii_decode

decoded = decoder_func(to_decode)
print("\n#DECODED :)\n")
print(decoded)