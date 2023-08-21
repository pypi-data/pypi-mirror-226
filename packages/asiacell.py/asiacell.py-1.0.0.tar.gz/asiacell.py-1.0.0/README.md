# Unofficial Python Wrapper for Asiacell API ✨

Simplify interaction with the Asiacell API using this unofficial Python wrapper. Perform actions like retrieving transferring money, Verify transferring, Spin wheel, Get the transaction and subscriptions history.

## Installation

Install the package using pip:

```bash
pip install asiacell.py
```
## Usage
Here's a simple example of using `asiacell.py`:
```py
from asiacell import Asiacell
from asiacell.utils.models import Bundle

# Defining The Number Object To Login With
asia = Asiacell("07700000000")

# Login With The Number
pid = asia.login()  # sending code to phone number and getting the pid

code = input(f"Enter the otp code: ")  # getting the code from user

# verify login
asia.verify_login(pid, code)

# saving data for future use without login again
asia.save_auth()
asia.load_auth()
print("AUTH LOADED")
print(asia.get_account_data().balance.value)  # prints account balance

res = asia.get_subscriptions_history()
bundle: Bundle
for bundle in res.bundles:
	print(f"{bundle.bundle_name}, {bundle.amount}")

```
For more details, refer to the upcoming documentation.

## Contributing
Contributions are welcome! Report bugs or suggest features by creating GitHub issues. Contribute code by forking the repository and submitting a pull request.

## Contact
Questions or discussions about the package can be held on our [Discord community](https://discord.gg/s7qacU5YNX). Join us today!
