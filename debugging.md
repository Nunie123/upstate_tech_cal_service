This is an example of debugging the data results used in app.py and outputting errors to the error log.

Near the top of the file to debug:

```
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()

import sys
from pprint import pformat
```

Example of debugging the value of an events index in a 'data' array:

```
    # logger.error("-------");
    logger.error(pformat(data.get('events')));
    logger.error("-------");
    # logger.error(events);

    sys.exit()
```
