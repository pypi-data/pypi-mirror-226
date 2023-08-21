# struct2args

This is a simple Python tool to convert structured data such as `yaml`,`toml`, or `json` to command line arguments. It
is intended to allow for easy configuration of command line tools.

## Installation

Homebrew coming eventually. For now you can install it with pip:

```bash
pip install struct2args
```

or Pipx:

```bash
pipx install struct2args
```

## Usage

Usage is pretty straightforward. It reads a structured data file and outputs a list of command line arguments as a
string. The file should have the following format:

```yaml
__args__: # This is required. Each item in the list is a set of arguments.
  - _name: 'nginx-test' # The name to search for 
    name: 'nginx-test-{% gitcommit %}'
    p: '80:{% get_free_port 80 %}'
    _pos: 'nginx'
  - _name: 'nginx-detached'
    name: 'nginx-detached-{% gitcommit %}'
    p: '80:80'
    _pos:
      - '-d'
      - 'nginx'
```

Anything that starts with an underscore is a special command and won't be converted to an argument. The following
special commands are supported:

``__args__``: Required in all files. This should be a list of arguments
`_pos*`: Anything starting with `_pos` will be converted to a positional argument. If it is a list, each item will be
interpreted as a separate positional argument.

Otherwise, all other keys will be converted to command line arguments. The key name will be the argument name and the
value. So in the example above: `name` will be converted to `--name nginx-test-{% gitcommit %}`.

To use the tool you can run it two ways:

### 1. Command line to xargs
    
    ```bash
    struct2args <file> | xargs <command>
    ```


### 2. Passing in a `--cmd` argument

    ```bash
    struct2args --cmd <command> <file>
    ```

## Jinja2 Templating

The tool uses Jinja2 templating to allow for dynamic arguments. The standard functions are available as well as the ones
from [jinja2-git](https://github.com/wemake-services/jinja2-git).

In addition, there is a custom tag of `get_free_port`. This will return a free port on the host machine starting at the
port number specified. For example, `{% get_free_port 80 %}` will return a free port starting at 80. This is useful for
things like port forwarding. You can declare a maximum port number by passing in an optional second argument. For
example `{% get_free_port 80 90 %}` will return a free port between 80 and 90.
