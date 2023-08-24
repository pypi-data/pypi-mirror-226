from setuptools import setup

description = """

# simple2encrypt

`simple2encrypt` is a Python library that provides utility functions for encryption and file operations. It 
includes functionalities for encrypting and decrypting data using the AES algorithm, generating encryption keys, 
reading and writing binary data from/to files, and handling user input.

## Installation

You can install `simple2encrypt` using `pip`:

```
pip install simple2encrypt
```

## Usage

### Encryption

The `Encryption` class in `simple2encrypt` allows you to easily encrypt and decrypt data using the AES algorithm. Here's how you can use it:

```
from simple2encrypt import Encryption

# Initialize the Encryption object with the key and data
key = b'mysecretpassword'  # Encryption key
data = b'mydata'  # Data to be encrypted or decrypted
encryption = Encryption(key, data)

# Encrypt the data
encrypted_data = encryption.encrypt()
print("Encrypted data:", encrypted_data)

# Decrypt the data
decrypted_data = encryption.decrypt()
print("Decrypted data:", decrypted_data)
```

### Folder Encryption and Decryption

The `WalkDirs` class in the library provides functions for bulk encryption and decryption of files within a specified folder using the AES algorithm. For example:

```
from simple2encrypt import WalkDirs

folder_path = '/path/to/folder'
key = b'mysecretpassword'
walker = WalkDirs(folder_path, key)

# Encrypt files within the folder
walker.encrypt()

# Decrypt files within the folder
walker.decrypt(key)
```

### Generating Encryption Keys

You can generate encryption keys based on passwords using the `generate_key` function. Here's an example:

```
from simple2encrypt import FileIO

password = 'mysecretpassword'  # Password for key generation
length = 32  # Key length (choose from [16, 24, 32])
key = FileIO.generate_key(password, length)
path_key = 'key.bin'
print("Generated key:", key)
FileIO.write_binary(path_key, key)
```

### Reading and Writing Binary Data

The `read_binary` and `write_binary` functions can be used to read and write binary data from and to files. For instance:

```
from simple2encrypt import FileIO

file_path = 'file.bin'

# Read binary data from a file
data = FileIO.read_binary(file_path)
print("Read data:", data)

# Write binary data to a file
data_to_write = b'mydata'
FileIO.write_binary(file_path, data_to_write)
print("Data written to file successfully.")
```

### Handling User Input

The `custom_input` function allows you to prompt users for input and retrieve their responses:

```
from simple2encrypt import custom_input

question = "Enter your name: "
user_name = custom_input(question)
print("User name:", user_name)
```

### Creating Encryption Key (Command Line)

The library also provides a command-line interface for creating a new encryption key. Here's an example usage:

```
aes-key [file name] [secret-password]
```
This will create a new encryption key file named `key.bin` based on the provided password.

```
aes-message  [key_file] # Executes the main function from example_message module
```

To encrypt a file:
```
aes-encrypt [file_path] [key_path]
```

To decrypt a file:
```
aes-decrypt [file_path] [key_path]
```

## Version

The current version of `simple2encrypt` is 1.6.2

## License

This library is distributed under the [MIT License](https://github.com/nhman-python/crypto-utils/blob/main/LICENSE). 
See the `LICENSE` file for more information.
```
"""

setup(
    name='simple2encrypt',
    version='1.6.2',
    description='Utility functions for encryption and file operations',
    author='nhman-python',
    author_email='wbgblfix@duck.com',
    url='https://github.com/nhman-python/crypto-utils',
    license='MIT',
    long_description=description,
    long_description_content_type='text/markdown',
    py_modules=['simple2encrypt', 'example_message', 'example_encrypt', 'example_decrypt'],
    install_requires=[
        'pycryptodome',  # Dependency on pycryptodome package
    ],
    entry_points={
        'console_scripts': ['aes-key = encryption_utils:main', 'aes-message = example_message:main',
                            'aes-encrypt = example_encrypt:main', 'aes-decrypt = example_decrypt:main'],
    },
)
