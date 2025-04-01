from dataclasses import dataclass
import subprocess
from dotenv import load_dotenv
import os


@dataclass
class DataBaseMenu:
    """
    A class for managing authentication using an environment-stored passkey.

    This class loads the passkey from an environment variable upon initialization
    and provides a method to check if a given password matches the stored passkey.
    """

    def __post_init__(self):
        try:
            """
            Post-initialization method that loads the passkey from environment variables.

            It attempts to retrieve the `PASS` key from the environment. If an error occurs,
            the `passkey` is set to an empty string.
            """
            load_dotenv()
            self.passkey = os.getenv("PASS")
        except Exception as e:
            self.passkey = ""

    def check_password(self, password):
        """
        Checks if the provided password matches the stored passkey.

        Args:
            password (str): The user-entered password.

        Returns:
            bool: `True` if the password is correct, otherwise `False`.
        """

        load_dotenv()
        passkey = os.getenv("PASS")
        print(passkey)
        print("Holi")
        if self.passkey == "":
            return False

        if password == self.passkey:
            return True
        else:
            return False

    def check_password_erco_config(self, password):
        command = f"echo '{password}' | sudo -S -u erco_config true"

        try:
            # Ejecutar el comando
            result = subprocess.run(
                command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Si el comando fue exitoso, el código de retorno será 0
            print(result)
            if result.returncode == 0:
                print(True)
            else:
                print(False)

        except subprocess.CalledProcessError as e:
            # Si el comando falla, esto captura el error
            print(
                f"Hubo un error al ejecutar el comando. Código de salida: {e.returncode}")
            print(f"Error: {e.stderr.decode()}")
            return False
