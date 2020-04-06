Class Based Logger for Python

# Installation

```bash
pip install tdlogging
```

## Usage
tdlogger.txt
- `exception` log exceptions
- `count` log count
- `time` log time elapsed
- `return` log return value
- `exec` log all
- `poll` whether to poll for tdlogger.txt changes
- `poll_period` seconds between each poll

TDLogger
- `file_path` path of tdlogger.txt
- `config` custom config that overrides tdlogger.txt
- `alias` a name for your logger

```python
# fib.py

from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="Fib Logger")


@logger.config()
class Fib:

    @staticmethod
    def get_n(n):
        a = 0
        b = 1

        if n == 0:
            return a
        elif n == 1:
            return b
        else:
            for i in range(2, n):
                c = a + b
                a = b
                b = c
            return b


print(Fib.get_n(5))

```

```text
# tdlogger.txt

exception= False
count = False
exec = True
time = False
return = False
poll = True
poll_period = 5

```

```bash
> python fib.py

┎────────────────────────┒
┃   --Configuration--    ┃
┃ New Configuration: {   ┃
┃     'exception': False ┃
┃     'count': False     ┃
┃     'exec': True       ┃
┃     'time': False      ┃
┃     'return': False    ┃
┃     'poll': True       ┃
┃     'poll_period': 5   ┃
┃ }                      ┃
┃               tdlogger ┃
┖────────────────────────┚

┎────────────────────────────┒
┃    --Method Execution--    ┃
┃ Alias: Fib Logger          ┃
┃ Class: Fib                 ┃
┃ Method: get_n              ┃
┃ Count: 1                   ┃
┃ Exec Time: 0.000s          ┃
┃ Return Value: 3            ┃
┃ Return Type: <class 'int'> ┃
┃ Arguments: {               ┃
┃     'n': 5                 ┃
┃ }                          ┃
┃                   tdlogger ┃
┖────────────────────────────┚

3

```