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

Another example from test fixtures:

```console
$ arbejdstimer explain --config tests/fixtures/basic/triplet-holidays-config.json
read valid configuration from (tests/fixtures/basic/triplet-holidays-config.json)
consider 3 holidays:
- Today (2021-12-28) is not a holiday
- Today (2021-12-28) is not a weekend
- At this hour (8) is work time
```

The same example from test fixtures with verbatim explanation mode on:

```console
$ arbejdstimer explain -v -c tests/fixtures/basic/triplet-holidays-config.json
read valid configuration from (tests/fixtures/basic/triplet-holidays-config.json)
configuration has 19 lines of (indented) JSON content:
    1 | {
    2 |   "api": 1,
    3 |   "application": "arbejdstimer",
    4 |   "operator": "or",
    5 |   "holidays": [
    6 |     {
    7 |       "label": "triplet holiday",
    8 |       "at": [
    9 |         "2021-12-29",
   10 |         "2021-12-30",
   11 |         "2021-12-31"
   12 |       ]
   13 |     }
   14 |   ],
   15 |   "working_hours": [
   16 |     8,
   17 |     17
   18 |   ]
   19 | }
effective configuration:
- given 3 holidays within [2021-12-29, 2021-12-31]:
  + 2021-12-29
  + 2021-12-30
  + 2021-12-31
- working hours:
  + [8, 17] (from configuration)
evaluation:
- Today is a holiday.
```

Retrieving a starter template for the configuration (default place is `$HOME/.arbejdstimer.json`):

```console
$ arbejdstimer template
{
  "api": 1,
  "application": "arbejdstimer",
  "operator": "or",
  "holidays": [
    {
      "label": "public holiday",
      "at": [
        "2021-12-08"
      ]
    },
    {
      "label": "company holidays 2021/2022",
      "at": [
        "2021-12-24",
        "2022-01-02"
      ]
    }
  ],
  "working_hours": [8, 17]
}
```
... a minimal configuration not considering holidays and falling back on working hours within `[7, 16]`:

```console
$ cat tests/fixtures/basic/minimal-config.json
{
  "operator": "or"
}
```

## Version command

```console
$ arbejdstimer version
Working hours (Danish arbejdstimer) or not? version 2022.6.27
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
  explain   Explain the answer to the question if now is a working hour...
  now       Silently answer the question if now is a working hour (per...
  template  Write a template of a JSON configuration to standard out and...
  version   Display the arbejdstimer version and exit
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
  -v, --verbose              Be more verbatim providing the effective config
                             values (default is false if not provided)
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

## Help on template command

```console
$ arbejdstimer template --help
Usage: arbejdstimer template [OPTIONS]

  Write a template of a JSON configuration to standard out and exit

Options:
  -h, --help  Show this message and exit.
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
