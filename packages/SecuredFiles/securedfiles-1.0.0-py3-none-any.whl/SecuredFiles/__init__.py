import os
import pathlib
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox
from cryptography.fernet import Fernet

_keypath = "~/.keys/SecuredFilesKey.key"


def _confirm_overwrite(filename):
    """
    Displays a confirmation dialog for overwriting a file.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if confirmed to overwrite, False otherwise.
    """
    app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle("Confirmation")
    msg_box.setText(
        filename + " already exists at this location.\nAre you sure you want to overwrite the current data?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.No)

    result = msg_box.exec_()
    return result == QMessageBox.Yes


class _Key:
    """
    Class for managing encryption and decryption keys.
    """

    def __init__(self, path: pathlib.Path = ...):
        """
        Initializes the _Key instance.

        Args:
            path (pathlib.Path, optional): Path to the key file. Defaults to generating a key at the default path.
        """
        if path is ...:
            path = pathlib.Path(os.path.expanduser(_keypath))

        self.path = path

        if not self.path.parent.exists() or not self.path.exists():
            if not self.path.parent.exists():
                self.path.parent.mkdir(parents=True)
            open(self.path, 'bw').write(Fernet.generate_key())
            print("The secure key was generated correctly.")

        self.key = Fernet(open(self.path, 'br').read())

    def encrypt(self, message: str):
        """
        Encrypts a message.

        Args:
            message (str): The message to be encrypted.

        Returns:
            bytes: The encrypted message.
        """
        return self.key.encrypt(message.encode())

    def decrypt(self, message: bytes):
        """
        Decrypts a message.

        Args:
            message (bytes): The encrypted message.

        Returns:
            str: The decrypted message.
        """
        return self.key.decrypt(message).decode()


class File:
    """
    Base class for file handling.
    """

    def __new__(cls, filepath):
        """
        Creates a new File instance based on the file extension.

        Args:
            filepath (str): Path to the file.

        Returns:
            File.SecureFile or File.UnsecureFile: An instance of SecureFile or UnsecureFile based on the file extension.
        """
        if filepath.endswith('.lck'):
            return cls.SecureFile(filepath)
        else:
            return cls.UnsecureFile(filepath)

    class SecureFile:
        """
        Class for handling encrypted files.
        """

        def __init__(self, filepath):
            """
            Initializes the SecureFile instance.

            Args:
                filepath (str): Path to the encrypted file.
            """
            self.path = filepath
            self._data = open(filepath, 'br').read()

        def __str__(self):
            """
            Returns a string representation of the SecureFile instance.

            Returns:
                str: The string representation of the encrypted data.
            """
            return str(self.data)

        def save(self):
            """
            Saves the encrypted data to the file.
            """
            open(self.path, 'bw').write(self._data)

        @property
        def data(self):
            """
            Decrypts and returns the data.

            Returns:
                str: The decrypted data.
            """
            return _Key().decrypt(self._data)

        @data.setter
        def data(self, value):
            """
            Encrypts and sets the data.

            Args:
                value (str): The data to be encrypted and set.
            """
            self._data = _Key().encrypt(value)

        def unlock(self):
            """
            Unlocks the file and returns an UnsecureFile instance.

            Returns:
                File.UnsecureFile: The unlocked unsecure file instance.
            """
            if self.path.removesuffix('.lck') not in os.listdir(pathlib.Path(self.path).parent) or _confirm_overwrite(
                    self.path.removesuffix('.lck')):
                key = _Key()
                open(self.path.removesuffix('.lck'), 'w').write(key.decrypt(self._data))
                os.remove(self.path)
                unlocked_file = File.UnsecureFile(self.path.removesuffix('.lck'))
                del self
                return unlocked_file

    class UnsecureFile:
        """
        Class for handling unencrypted files.
        """

        def __init__(self, filepath):
            """
            Initializes the UnsecureFile instance.

            Args:
                filepath (str): Path to the unencrypted file.
            """
            self.path = filepath
            self.data = open(filepath, 'r').read()

        def __str__(self):
            """
            Returns a string representation of the UnsecureFile instance.

            Returns:
                str: The string representation of the unencrypted data.
            """
            return str(self.data)

        def save(self):
            """
            Saves the unencrypted data to the file.
            """
            open(self.path, 'w').write(self.data)

        def lock(self):
            """
            Locks the file and returns a SecureFile instance.

            Returns:
                File.SecureFile: The locked secure file instance.
            """
            if self.path + ".lck" not in os.listdir(pathlib.Path(self.path).parent) or _confirm_overwrite(
                    self.path + ".lck"):
                key = _Key()
                open(self.path + ".lck", 'bw').write(key.encrypt(self.data))
                os.remove(self.path)
                locked_file = File.SecureFile(self.path + ".lck")
                del self
                return locked_file
