import os
import sys
import logging

logging_str="[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
#

log_dir="logs"
log_filepath=os.path.join(log_dir,"logging.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    #it will print the logging in the file
   

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
        #it will print the logging in the console

    ]
)

logger=logging.getLogger("datasciencelogger")
"""Perfect question 👌 You don’t just want to know *what* the code is doing, but also *why*, *when*, and *what happens if you don’t use it*. Let’s break it down in plain terms.

---

## 🔹 What is Logging?

Logging is a way for your program to **record events while running**. Think of it like a diary of what happened:

* When did something happen?
* Was it successful, a warning, or an error?
* Which part of the code was responsible?

---

## 🔹 Why use logging (instead of just `print`)?

✅ **Advantages of logging**

* **More informative** → Each log has a timestamp, severity level, and module name.
* **Separation of outputs** → Errors, warnings, and info can be filtered.
* **Persistent** → Logs are saved to a file (`logging.log`), so you can review them later. `print()` messages are gone once the program ends.
* **Scalable** → In large projects, logging helps you debug without scattering `print()` everywhere.
* **Professional practice** → Production systems (web apps, data pipelines, ML models) always rely on logs.

🚫 **If you don’t use logging**

* You’ll rely only on `print()` → no timestamps, no levels, no persistent record.
* Debugging large projects becomes painful.
* In production, you lose visibility of what went wrong after the program finishes.

---

## 🔹 How does your code help?

* By using **two handlers**:

  1. `FileHandler` → Saves logs into a file (`logs/logging.log`) for long-term analysis.
  2. `StreamHandler` → Shows logs in the console immediately, so you can watch things in real time.

That’s why you’re doing:

```python
handlers=[
    logging.FileHandler(log_filepath),
    logging.StreamHandler(sys.stdout)
]
```

Without one of them:

* **No FileHandler** → You can see logs only in the console, but nothing is saved.
* **No StreamHandler** → You won’t see real-time logs in the console; you’ll have to open the log file to check.

---

## 🔹 When to use logging?

* **During development**: To debug your code with INFO/DEBUG logs.
* **In production**: To monitor errors, performance issues, or unexpected behavior.
* **In long-running jobs**: (e.g., machine learning training, ETL pipelines) → logs track progress and failures without babysitting the terminal.
* **In team projects**: Everyone can look at the same log file instead of relying on personal `print()` messages.

---

## 🔹 Example (with vs without logging)

### Without logging (only `print`):

```python
print("Data loaded")
print("Model training started")
print("Error: learning rate too high")
```

❌ Problems:

* No timestamp → when did it happen?
* No severity → is this just info or a real error?
* No persistence → output is lost when program ends.

---

### With logging:

```python
logger.info("Data loaded")
logger.info("Model training started")
logger.error("Learning rate too high")
```

Output in console (and also saved in `logging.log`):

```
[2025-09-12 15:30:01,456: INFO: my_module: Data loaded]
[2025-09-12 15:30:02,123: INFO: my_module: Model training started]
[2025-09-12 15:30:02,789: ERROR: my_module: Learning rate too high]
```

✅ Now you know **when, what, where, and how severe** the message is.

---

👉 So to summarize:

* **How**: You set up logging with format + handlers (file + console).
* **Why**: For debugging, monitoring, and professional development.
* **When**: In both development (to debug) and production (to monitor).
* **What if not there**: You lose timestamps, severity levels, persistence, and debugging becomes much harder.

---

Do you want me to also explain the **different logging levels** (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) with examples? That usually makes it crystal clear when to use which.
Got it 👍 Let me break this down step by step so you understand **exactly what your code is doing** and why.

---

### 1. Importing modules

```python
import os
import sys
import logging
```

* **os** → lets you work with the file system (paths, directories).
* **sys** → gives access to system-related objects (like `stdout` = standard output, i.e. the console).
* **logging** → Python’s built-in module for logging messages (info, warning, error, etc.).

---

### 2. Defining log message format

```python
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
```

* This defines how each log entry will look.
* `%(asctime)s` → timestamp (when the log happened).
* `%(levelname)s` → log level (INFO, ERROR, etc.).
* `%(module)s` → the module (file) where the log was created.
* `%(message)s` → the actual log message.

So a log might look like:

```
[2025-09-12 10:30:45,123: INFO: my_module: Data loaded successfully]
```

---

### 3. Setting up log file directory

```python
log_dir = "logs"
log_filepath = os.path.join(log_dir, "logging.log")
os.makedirs(log_dir, exist_ok=True)
```

* `log_dir = "logs"` → all logs will go into a folder called `logs`.
* `log_filepath` → `"logs/logging.log"`.
* `os.makedirs(..., exist_ok=True)` → creates the folder if it doesn’t already exist (so no errors happen if you run the script multiple times).

---

### 4. Configuring logging

```python
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)
```

This is the **heart of the setup**:

* `level=logging.INFO` → minimum level of logs to capture. (INFO, WARNING, ERROR will show; DEBUG won’t unless you lower it).
* `format=logging_str` → use the format we defined earlier.
* `handlers=[...]` → where logs should go:

  * `logging.FileHandler(log_filepath)` → write logs into `logs/logging.log` file.
  * `logging.StreamHandler(sys.stdout)` → also print logs live to the terminal (console output).

👉 This is why you see the same log in **both the console and the log file**.

---

### 5. Creating a logger object

```python
logger = logging.getLogger("datasciencelogger")
```

* This creates a named logger called `"datasciencelogger"`.
* Instead of calling `logging.info()`, you’ll now use `logger.info()`, `logger.error()`, etc.
* This is useful when you have **multiple loggers** in different modules (helps organize logs).

---

✅ **In short:**

* You are creating a logging system that writes logs **both to a file and the console**.
* The format is structured for readability and debugging.
* A named logger (`datasciencelogger`) is created for consistency across your project.

---

👉 Do you want me to also show you an **example run** (where I log some messages and show how they appear in console and file)?
"""