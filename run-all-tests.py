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
    ('error0.imp', True),
    ('error1.imp', True),
    ('error2.imp', True),
    ('error3.imp', True),
    ('error4.imp', True),  # TODO parser/lekser
    ('error5.imp', True),
    ('error6.imp', True),  # ??? my mamy niezadeklarowaną zmienną
    ('error7.imp', True),  # podobnie jw
    ('error8.imp', True)  # TODO (for)
]

gotfryd = [
    ('error1.imp', True),
    ('error2.imp', True),
    ('error3.imp', True),
    ('error4.imp', True),
    ('error5.imp', True),
    ('error6.imp', True),
    ('error7.imp', True),
    ('error8.imp', True),
    ('error9.imp', True),
    ('error10.imp', True),
    ('error11.imp', True),
    ('error12.imp', True),
    ('error13.imp', True),
    ('error14.imp', True),
    ('error15.imp', True),
    ('error16.imp', True)
]


def run_test(tab, f, path):
    for t in tab:
        print('-----------------------')
        print(t[0])
        f.write(f"{t[0]} - ")
        if t[1]:
            try:
                start_compiler(f'{path}{t[0]}', 'virtual_machine/test.vm')
            except Exception as e:
                print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")
                f.write(f"{e}")
        else:
            f.write('skipped')
        f.write('\n')


def print_separator(title):
    print('##################')
    print(title)
    print('##################')


def main():
    with open('my-results.txt', 'w') as f:
        print_separator('TESTS')
        run_test(files, f, 'examples/')

        print_separator('GOTFRYD')
        run_test(gotfryd, f, 'examples/tests/gotfryd/')

    points = 0
    max_points = 0
    with open('my-results.txt', 'r') as f1:
        with open('examples/results.txt', 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            for i in range(0, len(lines2)):
                max_points += 1
                if lines1[i] == lines2[i]:
                    points += 1

    print(f"{bcolors.OKBLUE}Passed tests: {points}/{max_points}{bcolors.ENDC}")


if __name__ == "__main__":
    main()
