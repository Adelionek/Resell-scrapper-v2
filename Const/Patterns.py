import re
SIZE_PATTERN = re.compile(r"[3-4][0-9] [0-9]\/[0-9]|[3-4][0-9][,][0-9]|[3-4][0-9]")
nike = re.compile(r"[A-Z0-9]{6}[- ]{1}[A-Z0-9]{3}")
adidas = re.compile(r"[A-z]{2}[0-9]{4}|[A-z]{1}[0-9]{5}")
new_balance = re.compile(r"[A-z]{2}[0-9]{3}[A-z]{2}([0-9]|[A-z])?")
reebok = re.compile(r"[A-z]{1}[0-9]{5}|[A-z]{2}[0-9]{4}")