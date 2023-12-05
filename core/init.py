import os
import sys

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
print("BASE_PATH", BASE_PATH)

COMMON_PATH = os.path.join(BASE_PATH, 'common')
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
print("COMMON_PATH", COMMON_PATH)
print("CONFIG_PATH", CONFIG_PATH)

sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)

print("sys.path", sys.path)






