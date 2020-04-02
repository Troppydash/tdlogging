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
- `exec` log count, time, and return
- `poll` whether to poll for tdlogger.txt changes
- `poll_period` seconds between each poll



```python
# fib.py

from tdlogging.tdlogger import create_logger

logger = create_logger(path="/path/to/tdlogger.txt/")

@logger.get_logger()
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

Fib.get_n(9)
```
```bash
> python fib.py

┎──────────TDLogger──────────┒
┃  --Method get_n Executed-- ┃
┃ Arguments: {               ┃
┃     'n': 9,                ┃
┃ }                          ┃
┃ Times Executed: 1          ┃
┃ Execution Time: 0.000s     ┃
┃ Return Value: 21           ┃
┃ Return Type: <class 'int'> ┃
┖────────────────────────────┚
```