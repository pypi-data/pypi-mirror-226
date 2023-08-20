# SecuredFiles

[![PyPI Version](https://img.shields.io/pypi/v/SecuredFiles.svg)](https://pypi.org/project/SecuredFiles/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

SecuredFiles is a Python library that provides a simple and secure way to work with encrypted and unencrypted files. It offers a set of classes that allow you to seamlessly lock and unlock files, making sure your sensitive data remains protected.

## Installation

You can install SecuredFiles using pip:

`pip install SecuredFiles`


## Usage

### Automatic Selection

You can use SecuredFiles in different ways, depending on your needs:

#### Option 1: Automatic File Selection

Run the following command to automatically handle file locking and unlocking:

```bash
python -m SecuredFiles your_file_name
```

This command will intelligently determine whether to unlock or lock the file based on its current state.

### Manual Selection
You can also manually select how to interact with your files in your code:

#### Option 1: General Usage
```python
import SecuredFiles

file = SecuredFiles.File('path_to_your_file')
```
The File class will decide whether to lock or unlock the file based on its current state.

#### Option 2: Secure File Usage
```python
import SecuredFiles

secure_file = SecuredFiles.File.SecureFile('path_to_your_file')
```
This will open the file as a secure (.lck) file, minimizing the chances of errors.

#### Option 3: Unsecure File Usage
```python
import SecuredFiles

unsecure_file = SecuredFiles.File.UnsecureFile('path_to_your_file')
```
This will open the file as an unsecure file without decryption.

### Modifying and Saving
Regardless of the chosen option, you can retrieve and modify the data using the .data attribute:

```python
file.data = "some new data"
data = file.data
```
Make sure to use `.save()` to push changes back to the file after modification.

### Locking and Unlocking
For `SecureFile`, use `.unlock()` to unlock the file (which will transform the .lck file and delete it).

For `UnsecureFile`, use `.lock()` to lock the file (which will transform the file and delete the non-.lck file).

Both operations will prompt a pop-up asking for confirmation if a file with the same name already exists.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.