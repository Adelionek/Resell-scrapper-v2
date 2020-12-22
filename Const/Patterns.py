import re
SIZE_PATTERN = re.compile(r"[3-4][0-9] [0-9]\/[0-9]|[3-4][0-9][,][0-9]|[3-4][0-9]")
nike = re.compile(r"\b[A-Z0-9]{6}[- ]{1}[A-Z0-9]{3}\b")
adidas = re.compile(r"\b[A-z]{2}[0-9]{4}\b")
new_balance = re.compile(r"\b[A-z]{2}[0-9]{3}[A-z]{2}([0-9]|[A-z])?\b")