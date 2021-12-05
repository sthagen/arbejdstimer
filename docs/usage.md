# Example Usage

## Is now a working day?

```console
$ arbejdstimer now --config tests/fixtures/basic/minimal-config.json
configuration is ({})
Today is weekend.
```


## Version command

```console
$ arbejdstimer version
Working hours (Danish arbejdstimer) or not? version 2021.12.5
```

## General help

```console
$ arbejdstimer
Usage: arbejdstimer [OPTIONS] COMMAND [ARGS]...

  Working hours (Danish arbejdstimer) or not?

  Given a configuration file detect if today is a work day and if at the time
  of request is a working hour.

Options:
  -V, --version  Display the arbejdstimer version and exit
  -h, --help     Show this message and exit.

Commands:
  now      Answer the question if now is a working hour.
  version  Display the arbejdstimer version and exit
```

## Help on now command

```console
$ arbejdstimer now --help
Usage: arbejdstimer now [OPTIONS]

  Answer the question if now is a working hour.

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
