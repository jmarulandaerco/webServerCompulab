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
        try:
            # Ejecutamos 'su -' para cambiar al usuario especificado y verificar la contraseña
            result = subprocess.run(
                ['su', '-', 'erco_config'],  # Comando para cambiar al usuario
                input=password + '\n',  # Proporcionamos la contraseña como entrada
                text=True,  # Aseguramos que el 'input' sea texto
                check=True,  # Si el comando falla, se lanzará una excepción
                stdout=subprocess.PIPE,  # Captura la salida estándar
                stderr=subprocess.PIPE   # Captura los errores
            )

            # Si llegamos aquí, la contraseña es correcta
            return True  # Contraseña correcta

        except subprocess.CalledProcessError as e:
            # Si ocurre un error, significa que la contraseña es incorrecta
            return False  # Contraseña incorrecta
