# Example Usage

## Is now a working day?

Silent answer:

```console
$ arbejdstimer now --config tests/fixtures/basic/holidays-config.json || echo "OFF"
OFF
```

Explaining the reasons and answering:

```console
$ arbejdstimer explain --config tests/fixtures/basic/holidays-config.json || echo "OFF"
read valid configuration from (tests/fixtures/basic/holidays-config.json)
consider 11 holidays:
- Today is a holiday.
OFF
```

## Version command

```console
$ arbejdstimer version
Working hours (Danish arbejdstimer) or not? version 2021.12.28
```

## General help

```console
$ arbejdstimer
Usage: arbejdstimer [OPTIONS] COMMAND [ARGS]...

  Working hours (Danish arbejdstimer) or not?

  Given a configuration file detect if today is a work day and if at the time
  of request is a working hour.

  Return code of 0 indicates work time, 1 no work time, and 2 usage error.

  Additional help available per command adding the -h/--help option

Options:
  -V, --version  Display the arbejdstimer version and exit
  -h, --help     Show this message and exit.

Commands:
  explain  Explain the answer to the question if now is a working hour...
  now      Silently answer the question if now is a working hour (per...
  version  Display the arbejdstimer version and exit
```

## Help on explain command

```console
$ arbejdstimer explain --help
Usage: arbejdstimer explain [OPTIONS]

  Explain the answer to the question if now is a working hour (in addition to
  the return code 0 for yes, and 1 for no).

Options:
  -c, --config <configpath>  Path to config file (default is
                             $HOME/.arbejdstimer.json)
  -h, --help                 Show this message and exit.
```

## Help on now command

```console
$ arbejdstimer now --help
Usage: arbejdstimer now [OPTIONS]

  Silently answer the question if now is a working hour (per return code 0 for
  yes, and 1 for no).

Options:
  -c, --config <configpath>  Path to config file (default is
                             $HOME/.arbejdstimer.json)
  -h, --help                 Show this message and exit.
```

## Help on version command

Why not :-)

```console
$ arbejdstimer version --help
Usage: arbejdstimer version [OPTIONS]

  Display the arbejdstimer version and exit

Options:
  -h, --help  Show this message and exit.
```
