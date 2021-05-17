# UNO Card game simulation

Computer simulation final class project

## Project setup

Use a [virtual environment](https://click.palletsprojects.com/en/7.x/quickstart/#virtualenv) with Python `>=3.8`:

``` bash
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
$ pip install -e .
```

### Execution

You must activate virtual environment first.

* For `Player vs. Computer` use:
```bash
$ pgzrun main.py
```

* For `Computer vs. Computer` (this will execute 1 million of games for simulation statistics implementation) use:
```bash
$ pgzrun autoplayed.py
```

* To obtain simulation statistics, like best hand, use:
```bash
$ python src/analysis/statistics.py
```
