import os


def cable(script):
   return os.system("jtag urjtag/" + script)

print cable("detect_chain.urj")
