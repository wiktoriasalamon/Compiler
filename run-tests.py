import os
from run import start_compiler

try:
    start_compiler('examples/tests/random.imp', 'virtual_machine/test.vm')
    os.system('./maszyna_wirtualna/maszyna-wirtualna ./virtual_machine/test.vm')
except Exception as e:
    print(e)
