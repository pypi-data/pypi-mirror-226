# myfuncs

`myfuncs` is a Python package that provides a set of utility functions designed to streamline your code and enhance efficiency across various projects and platforms.

## Installation

You can install `myfuncs` using pip:

```bash
pip install myfuncs
```

## Usage


The functions in `myfuncs` can be imported as follows:

```python
from myfuncs import runcmd

# Example usage of the runcmd function
result = runcmd("ls -l")
print("Output:", result)
```

# Functions

## `runcmd()`

Here, `runcmd` is a utility function that runs shell commands with optional output capture. It accepts additional arguments to customize the command execution process. This function is just one example of the utilities provided by `myfuncs`.

The `runcmd` function's parameters are:

- `cmd` (str): The command to be executed.
- `output` (bool, optional): Specifies whether to capture and return the output of the command. Defaults to True.
- `*args`: Additional positional arguments passed to `subprocess.run()`.
- `**kwargs`: Additional keyword arguments passed to `subprocess.run()`.

## `is_jwt_str()`

Returns True if a str is a valid encoded jwt string else False

## `nlprint()`

Identical to print but with an additional print()

----

## Running Tests

The `myfuncs` package includes a test suite to verify the operation of its functions. To run the tests:

```bash
python -m unittest tests/*.py
```

This command executes all Python files (`*.py`) in the `tests` directory. Successful completion signifies that the functions are working as intended.

## Documentation

In-depth documentation can be accessed in the source code within docstrings. For future developments and detailed examples, please refer to the `myfuncs` [GitHub repository](https://github.com/cc-d/myfuncs).

## Contributing

Contributions to `myfuncs` are welcomed. If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/cc-d/myfuncs).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/cc-d/myfuncs/blob/main/LICENSE) file for more details.