import os
from kompilator import start_compiler


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
    'examples/program0.imp',  #
    'examples/program0ns.imp',  #
    'examples/program1.imp',  # 82196
    'examples/program2.imp',  # '5789975336' ' 2 3 19 1 39091943' - 6586932
    'tests/0-div-mod.imp',  # 997
    'tests/1-numbers.imp',  # 3322
    'tests/2-fib.imp',  # 5879
    'tests/3-fib-factorial.imp',  # 20061
    'tests/4-factorial.imp',  # 15836
    'tests/5-tab.imp',  # 28635
    'tests/6-mod-mult.imp',  # 274378
    'tests/7-loopiii.imp',  # 1 - 464543, 2 - 464543
    'tests/8-for.imp',  # 121731
    'tests/9-sort.imp',  # 87096
    'tests/program0.imp',  #
    'tests/program1.imp',  #
    'tests/program2.imp',  #
    'tests_lab/arithm1.imp',  # 1 - 580698, 2 - 580698
    'tests_lab/arithm2.imp',  # 1 - 571593, 2 - 571567
    'tests_lab/arithm3.imp',  # 1 - 846737, 2 - 846059
    'tests_lab/calc.imp',  # 283880208
    'tests_lab/compare.imp',  # 1 - 966, ...
    'tests_lab/cond1.imp',  # 719
    'tests_lab/cond2.imp',  # 1 - 575, 2 - 572
    'tests_lab/cond_nested.imp',  # 1 - 2597, 2 - 2695
    'tests_lab/factorial1.imp',  # 1 - 25245, 2 - 275063
    'tests_lab/factorial2.imp',  # 1 - 26860, 2 - 291978
    'tests_lab/factorial3.imp',  # 1 - 57615, 2 - 722636
    'tests_lab/loop.imp',  # 1047000825
    'tests_lab/loop_range.imp',  # 800
    'tests_lab/nestedLoop2.imp',  # 3025338
    'tests_lab/simple1.imp',  # 1 - 2914, 2 - 2999
    'tests_lab/simple2.imp',  # 1 - 4356, 2 - 4291, 3 - 4119
    'tests_lab/tab1.imp',  # 35669
    'tests_lab/tab2.imp',  # 310298
    'tests_lab/tab3.imp',  # 1 - 3103, 2 - 3103, 3 - 3187
]


def run_all():
    for f in files:
        try:
            print(f"{bcolors.OKBLUE}{f}{bcolors.ENDC}")
            start_compiler(f'programs/{f}', 'tests/test.vm')
            os.system('./maszyna_wirtualna/maszyna-wirtualna-cln ./tests/test.vm')
        except Exception as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")

        print(f"{bcolors.OKBLUE}----------------------------------------------{bcolors.ENDC}")
        input("Press enter to run next program")


def run_one(i):
    try:
        print(f"{bcolors.OKBLUE}{files[i]}{bcolors.ENDC}")
        start_compiler(f'programs/{files[i]}', 'virtual_machine/test.vm')
        os.system('./maszyna_wirtualna/maszyna-wirtualna-cln ./virtual_machine/test.vm')
    except Exception as e:
        print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")


def main():
    run_all()


if __name__ == "__main__":
    main()
