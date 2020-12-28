import os
from run import start_compiler

files = [
    'tests/random.imp',
    'error0.imp',
    'error1.imp',
    'error2.imp',
    'error3.imp',
    'error4.imp',  # TODO parser/lekser
    'error5.imp',
    'error6.imp',  # ??? my mamy niezadeklarowaną zmienną
    'error7.imp',  # podobnie jw
    'error8.imp',  # TODO (for)
]

try:
    start_compiler(f'examples/{files[0]}', 'virtual_machine/test.vm')
    os.system('./maszyna_wirtualna/maszyna-wirtualna ./virtual_machine/test.vm')
except Exception as e:
    print(e)
