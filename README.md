# Kompilator
#### Autor: Wiktoria Salamon

## Wymagania systemowe

Aby zainstalować niezbędne do uruchomienia programu zależności (_python3_ oraz biblioteka _SLY_) można skorzystać ze skryptu **install.sh**:
```sh
$ ./install.sh
```
lub zainstalować je samodzielnie:
```sh
$ sudo apt update
$ sudo apt install python3
$ sudo apt install python3-pip
$ pip3 install sly
```

## Uruchamianie kompilatora

Aby skompilować kod źródłowy języka do kodu maszyny wirtualnej należy w katalogu głównym projektu użyć polecenia:

```sh
$ python3 kompilator.py <nazwa_pliku_wejściowego> <nazwa_pliku_wyjściowego>
```

## Pliki 

- code_generator.py
- compiler.py
- compiler_classes.py
- exceptions.py
- install.sh
- **kompilator.py**
- lexer.py
- parser.py
- README.md


