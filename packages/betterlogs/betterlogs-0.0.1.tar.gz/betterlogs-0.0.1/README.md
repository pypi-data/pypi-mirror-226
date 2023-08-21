# BetterLogs

BetterLogs is a improved logging package for python

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install betterlogs.

```bash
pip install betterlogs
```

## Usage

```python

from betterlogs import logger
from colorama import Fore, Style

logger = logger.Logger(name="BetterLogs", base_color=Fore.BLUE, base_style=Style.DIM,
                       time=True, time_color=Fore.BLUE, time_style=Style.BRIGHT)

logger.log("test")
logger.debug("test")
logger.warning("test")
logger.error("test")
logger.critical("test")

```
Result
![Result](images/result.png)



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)