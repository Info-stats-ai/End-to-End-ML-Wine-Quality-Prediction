import os
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            # this is how the reading of  the yaml file happens using safe.load
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
        


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")
    #as we are using the json.dump it will automatically convert the data into json format
    #and it will save the data in the json file
    #and it will also log the message that the json file is saved at the path


@ensure_annotations
#this is how the loading of the json file happens using json.load
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
# save bin are the binary files that are saved in the file
# we need them because we are using the joblib to save the binary files
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data
    """Nice 👍 this code is a **utility/helper module** that deals with **files, folders, and data persistence** in a structured way. Let me explain it step by step:

---

## 🔹 1. Imports

```python
import os
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError
```

* **os** → work with directories.
* **yaml** → to read `.yaml` configuration files.
* **logger** → custom logger from your earlier logging setup (to record events).
* **json** → to save/load JSON files.
* **joblib** → for saving/loading binary files (often used for ML models).
* **ensure\_annotations** → decorator that ensures your function arguments/return types follow type hints.
* **ConfigBox** → wrapper around dicts so you can access keys like attributes (`config.key` instead of `config["key"]`).
* **Path** → cleaner way to handle file paths (instead of raw strings).
* **Any** → type hint (can be any data type).
* **BoxValueError** → raised if you try to make a `ConfigBox` from empty data.

---

## 🔹 2. Reading YAML

```python
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    ...
```

* Opens a YAML file.
* Loads it into Python dict using `yaml.safe_load`.
* Converts it into a `ConfigBox` (so you can use dot notation).
* Logs success.
* Raises `ValueError` if the YAML is empty.

👉 **Use case**: Reading project configuration files (`config.yaml`).
Without it → you’d manually use `yaml.safe_load` and deal with raw dicts.

---

## 🔹 3. Creating Directories

```python
def create_directories(path_to_directories: list, verbose=True):
    ...
```

* Loops over a list of paths.
* Creates each directory (`os.makedirs(..., exist_ok=True)` so it doesn’t crash if it already exists).
* Logs a message if `verbose=True`.

👉 **Use case**: Auto-creating folders for data, logs, models, reports, etc.
Without it → you’d have to manually create directories every time, or risk errors.

---

## 🔹 4. Saving JSON

```python
def save_json(path: Path, data: dict):
    ...
```

* Opens a file in write mode.
* Dumps a dictionary as JSON (`indent=4` for readability).
* Logs success.

👉 **Use case**: Save metadata, experiment results, configs, or reports.
Without it → you’d write boilerplate `open()` + `json.dump()` every time.

---

## 🔹 5. Loading JSON

```python
def load_json(path: Path) -> ConfigBox:
    ...
```

* Reads JSON file.
* Loads into a dict with `json.load`.
* Wraps in `ConfigBox` (so you can use dot notation).
* Logs success.

👉 **Use case**: Load experiment results/configs as objects.
Without it → you’d only get raw dicts, less convenient.

---

## 🔹 6. Saving Binary Files

```python
def save_bin(data: Any, path: Path):
    ...
```

* Saves any Python object into a binary file using `joblib.dump`.
* Logs success.

👉 **Use case**: Save machine learning models, preprocessed datasets, or embeddings.
Without it → you’d need to use `pickle` (less efficient, less safe).

---

## 🔹 7. Loading Binary Files

```python
def load_bin(path: Path) -> Any:
    ...
```

* Loads binary data back using `joblib.load`.
* Logs success.

👉 **Use case**: Load ML models for inference, reload cached datasets.
Without it → same as above, you'd need more manual code.

---

## 🔹 8. Why `@ensure_annotations`?

This decorator ensures that the function arguments and return types follow the type hints you declared.
Example:

```python
read_yaml("config.yaml")  # will fail
read_yaml(Path("config.yaml"))  # works
```

👉 This makes your functions **safer and more predictable**.

---

## ✅ In Summary

This code is a **utility toolkit** for a data science project.

* **How**: Provides small reusable functions for common tasks (read/write YAML, JSON, binary, create dirs).
* **Why**: Reduces repetitive code, ensures consistent logging, improves reliability.
* **When**: Use it in any ML/data project to manage configs, results, and saved models.
* **What if not there**:

  * You’d rewrite the same `open()`, `os.makedirs()`, `json.dump()`, `joblib.dump()` code everywhere.
  * No logging, so debugging failures (like missing config files) would be harder.
  * Higher risk of errors and less maintainability.

---

👉 Do you want me to also **show a mini real-world example** of using these utilities in a project (like reading `config.yaml`, creating folders, saving model metadata as JSON, etc.)?
"""