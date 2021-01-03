import os
from run import start_compiler


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


files = [
    'tests/random.imp',
    'error0.imp',
    'error1.imp',
    'error2.imp',
    'error3.imp',
    'error4.imp',
    'error5.imp',
    'error6.imp',
    'error7.imp',
    'error8.imp',
    'program0.imp',
    'program0ns.imp',
    'program1.imp',
    'program2.imp',  # ?????????????????????????????? 10: 2 1 5 1
    'tests/gebala/0-div-mod.imp',
    'tests/gebala/1-numbers.imp',
    'tests/gebala/2-fib.imp',
    'tests/gebala/3-fib-factorial.imp',
    'tests/gebala/4-factorial.imp',
    'tests/gebala/5-tab.imp',
    'tests/gebala/6-mod-mult.imp',
    'tests/gebala/7-loopiii.imp',
    'tests/gebala/8-for.imp',
    'tests/gebala/9-sort.imp',
    'tests/gebala/program0.imp',
    'tests/gebala/program1.imp',
    'tests/gebala/program2.imp',
    'tests/gotfryd/arithm1.imp',
    'tests/gotfryd/arithm2.imp',
    'tests/gotfryd/arithm3.imp',
    'tests/gotfryd/calc.imp',
    'tests/gotfryd/compare.imp',
    'tests/gotfryd/cond1.imp',
    'tests/gotfryd/cond2.imp',
    'tests/gotfryd/cond_nested.imp',
    'tests/gotfryd/error1.imp',
    'tests/gotfryd/error2.imp',
    'tests/gotfryd/error3.imp',
    'tests/gotfryd/error4.imp',
    'tests/gotfryd/error5.imp',
    'tests/gotfryd/error6.imp',
    'tests/gotfryd/error7.imp',
    'tests/gotfryd/error8.imp',
    'tests/gotfryd/error9.imp',
    'tests/gotfryd/error10.imp',
    'tests/gotfryd/error11.imp',
    'tests/gotfryd/error12.imp',
    'tests/gotfryd/error13.imp',
    'tests/gotfryd/error14.imp',
    'tests/gotfryd/error15.imp',
    'tests/gotfryd/error16.imp',
    'tests/gotfryd/factorial1.imp',
    'tests/gotfryd/factorial2.imp',
    'tests/gotfryd/factorial3.imp',
    'tests/gotfryd/loop.imp',
    'tests/gotfryd/loop_range.imp',
    'tests/gotfryd/nestedLoop2.imp',
    'tests/gotfryd/simple1.imp',
    'tests/gotfryd/simple2.imp',
    'tests/gotfryd/tab1.imp',
    'tests/gotfryd/tab2.imp',
    'tests/gotfryd/tab3.imp',
]


def run_all():
    for f in files:
        try:
            print(f"{bcolors.OKBLUE}{f}{bcolors.ENDC}")
            start_compiler(f'examples/{f}', 'virtual_machine/test.vm')
            os.system('./maszyna_wirtualna/maszyna-wirtualna-cln ./virtual_machine/test.vm')
        except Exception as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")

        print(f"{bcolors.OKBLUE}----------------------------------------------{bcolors.ENDC}")
        input("Press enter to run next program")


def run_one(i):
    try:
        print(f"{bcolors.OKBLUE}{files[i]}{bcolors.ENDC}")
        start_compiler(f'examples/{files[i]}', 'virtual_machine/test.vm')
        os.system('./maszyna_wirtualna/maszyna-wirtualna-cln ./virtual_machine/test.vm')
    except Exception as e:
        print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")


def main():
    run_one(53)


if __name__ == "__main__":
    main()
