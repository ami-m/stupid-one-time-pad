import re
import argparse


def letter_to_num(ch):
  ch = ch.lower()
  if ord(ch) not in list(range(ord('a'), ord('z')+1)):
    return -1
  return ord(ch) - 97


def char_range(c1, c2):
  """Generates the characters from `c1` to `c2`, inclusive."""
  for c in range(ord(c1), ord(c2)+1):
      yield chr(c)


def prepare_msg(msg):
  return seperate_to_five_char_groups(pad(remove_spaces(msg)))


def seperate_to_five_char_groups(msg):
  p = re.compile("(?P<five_chars>([a-z]{5}))", re.VERBOSE)
  return p.sub('\g<five_chars> ', msg)

def pad(msg):
  if 0 == len(msg) % 5:
    return msg
  return msg + ('x'*(5-(len(msg) % 5)))


def remove_spaces(msg):
  p = re.compile(' +')
  return p.sub('', msg)


def read_file(file_name):
  with open(file_name) as f:
    content = f.read()
  return [letter_to_num(ch) for ch in remove_spaces(content) if letter_to_num(ch) >= 0]


def add_otp_to_cypher(cypher, otp, decrypt):
  if len(otp) < len(cypher):
    raise Exception('pad too short')

  sign = 1
  if decrypt:
    sign = -1

  res = []
  for i in range(len(cypher)):
    res.append((cypher[i] + (sign * otp[i])) % 26)
  return res


def convert_list_of_nums_to_string(list_of_nums):
  res = [chr(n + 97) for n in list_of_nums]
  return "".join(res)


def define_and_get_console_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("cypher", help="the cypher to encrypt (or the message to decrypt)")
  parser.add_argument("pad", help="the pad to use")
  parser.add_argument("-d", "--decrypt", help="subtract the pad from the cypher instead of adding it",
                      action="store_true")
  return parser.parse_args()

args = define_and_get_console_args()

cypher = read_file(args.cypher)
otp = read_file(args.pad)

out = convert_list_of_nums_to_string(add_otp_to_cypher(cypher, otp, args.decrypt))
if not args.decrypt:
  out = prepare_msg(out)
print(out)