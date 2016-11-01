import getopt
import struct
import sys
from signatures import signatures

def hex_to_binary(hexstr):
  """ Takes in a string of space-separated hexadecimal numbers like this:

  00 A1 C3 00 (...)

  and converts each space-separated byte into a number. Those numbers are then
  packed into a binary string and returned."""
  non_empty = lambda x: len(x) != 0
  ascii_hex_numbers = filter(non_empty, hexstr.split(" "))
  numberify = lambda x: int(x, base=16)
  binary_numbers = map(numberify, ascii_hex_numbers)
  return struct.pack('%sB' % len(binary_numbers), *binary_numbers)

def binary_to_hex(binary):
  """ Basically, inverse of hex_to_binary() above. """
  nums = struct.unpack("B"*len(binary), binary)
  interesting = lambda x: x != None
  hexstrings = [s[2:].upper() for s in filter(interesting, map(hex, nums))]
  return " ".join(hexstrings)

def make_trie(keyvals):
  keys = [key for key in keyvals]
  trie = dict()
  for key in keys:
    current_trie = trie
    for letter in key:
      current_trie = current_trie.setdefault(letter, {})
    current_trie["value"] = keyvals[key]
  return trie

def trie_get(trie, key):
  for letter in key:
    if (letter in trie):
      trie = trie[letter]
    else:
      return None
  return trie["value"] if "value" in trie else None

def prefix_valid(trie, prefix):
  for letter in prefix:
    if (letter in trie):
      trie = trie[letter]
    else:
      return False
  return len(trie) != 0

def main():
  SHORT_HEADERS = 0
  try:
    opts, args = getopt.getopt(sys.argv, "sh", "short_headers")
  except getopt.GetoptError:
    print 'shibboleth.py [-sh | --short_headers] <file>'
    sys.exit(1)
  for opt, arg in opts:
    if (opt in ("sh", "short_headers")):
      SHORT_HEADERS = 1

  if (len(args) != 2):
    print 'shibboleth.py [-sh | --short_headers] <file>'
    sys.exit(1)

  file_sig_keyvals = {hex_to_binary(sig[1]): (sig[1], sig[0]) for sig in signatures}
  file_sig_trie = make_trie(file_sig_keyvals)

  # Possibilities is a list of tuples of the form:
  # (file offset, hex signature, description)
  possibilities = []

  index = 0
  end_reached = False

  with open(args[1], 'rb') as infile:
    cache = ""
    prefix_loc = [0, 1] # start, end (in cache)
    while (True):
      prefix = cache[prefix_loc[0]:prefix_loc[1]]
      while (prefix_valid(file_sig_trie, prefix)):
          value = trie_get(file_sig_trie, prefix)
          if (value):
            if (len(prefix) > 1 or SHORT_HEADERS):
              possibilities.append((str(index), value[0], value[1]))
          char = infile.read(1)
          if (char == ""):
            end_reached = True
            break
          cache += char
          prefix_loc[1] += 1
          prefix = cache[prefix_loc[0]:prefix_loc[1]]
      index += 1
      if (index == 1025):
        break
      prefix_loc[0] = 0
      prefix_loc[1] = 1
      cache = cache[1:]
      if (end_reached):
        break

  explanation_length = lambda x: len(x[1])
  possibilities.sort(key=explanation_length, reverse=True)

  print "File Offset\t Hex Signature\t Explanation"
  print "-"*80
  for sig in possibilities:
    position = sig[0]
    signature = sig[1]
    explanation = sig[2]
    print (position + "\t" + signature + "\t" + explanation)

if __name__ == "__main__":
  main()
