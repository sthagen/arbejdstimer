# Example Usage

## Is now a working day?

Silent answer:

```console
❯ arbejdstimer now --config test/fixtures/basic/holidays-config.json || echo "OFF"
OFF
```

Explaining the reasons and answering:

```console
❯ arbejdstimer explain --config test/fixtures/basic/holidays-config.json || echo "OFF"
read valid configuration from (test/fixtures/basic/holidays-config.json)
consider 12 holidays:
- Day (2022-10-23) is not a holiday
- Day is weekend.
OFF
```

Another example from test fixtures:

```console
❯ arbejdstimer explain --config test/fixtures/basic/triplet-holidays-config.json
read valid configuration from (test/fixtures/basic/triplet-holidays-config.json)
consider 3 holidays:
- Day (2022-10-23) is not a holiday
- Day is weekend.
```

The same example from test fixtures with verbatim explanation mode on:

```console
❯ arbejdstimer explain -v -c test/fixtures/basic/triplet-holidays-config.json
read valid configuration from (test/fixtures/basic/triplet-holidays-config.json)
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
detected non-strict mode (no constraints on year frame from config)
effective configuration:
- given 3 holidays within [2021-12-29, 2021-12-31]:
  + 2021-12-29
  + 2021-12-30
  + 2021-12-31
- working hours:
  + [8, 17] (from configuration)
evaluation:
- Day (2022-10-23) is not a holiday
- Day is weekend.
```

The new day option to explain any valid date working day status (default non-strict mode):

```console
❯ arbejdstimer explain --day 2345-11-13
read valid configuration from (/some/user/.arbejdstimer.json)
consider 32 holidays:
- Day (2345-11-13) is not a holiday
- Day (2345-11-13) is not a weekend
- At this hour (14) is work time
```

Better call `cal`? ... looks correct (13th of November 2345 is a Tuesday):

```console
❯ cal 11 2345
   November 2345
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30
```

Trying the same working day query with strict mode enabled (and assuming no eternal configuration present):

```console
❯ arbejdstimer explain --day 2345-11-13 --strict
read valid configuration from (/some/user/.arbejdstimer.json)
consider 32 holidays:
detected strict mode (queries outside of year frame from config will fail)
- Day is not within year range of configuration
```

Still doubts on how the evaluation went? Try the verbose option:

```console
❯ python -m arbejdstimer explain --day 2345-11-13 --strict --verbose
read valid configuration from (/some/user/.arbejdstimer.json)
configuration has 76 lines of (indented) JSON content:
    1 | {
    2 |   "api": 1,
    3 |   "application": "arbejdstimer",
    4 |   "operator": "or",
    5 |   "holidays": [
    6 |     {
    7 |       "label": "some holidays 2021/2022",
    8 |       "at": [
    9 |         "2021-12-24",
   10 |         "2022-01-02"
   11 |       ]
   12 |     },
   13 |     {
   14 |       "label": "Josefstag",
   15 |       "at": [
   16 |         "2022-03-19"
   17 |       ]
   18 |     },
   19 |     {
   20 |       "label": "Ostern",
   21 |       "at": [
   22 |         "2022-04-15",
   23 |         "2022-04-18"
   24 |       ]
   25 |     },
   26 |     {
   27 |       "label": "Christi Himmelfahrt",
   28 |       "at": [
   29 |         "2022-05-26"
   30 |       ]
   31 |     },
   32 |     {
   33 |       "label": "Pfingstmontag",
   34 |       "at": [
   35 |         "2022-06-06"
   36 |       ]
   37 |     },
   38 |     {
   39 |       "label": "Fronleichnam",
   40 |       "at": [
   41 |         "2022-06-16"
   42 |       ]
   43 |     },
   44 |     {
   45 |       "label": "Nationalfeiertag Schweiz",
   46 |       "at": [
   47 |         "2022-08-01"
   48 |       ]
   49 |     },
   50 |     {
   51 |       "label": "Mariä Himmelfahrt",
   52 |       "at": [
   53 |         "2022-08-15"
   54 |       ]
   55 |     },
   56 |     {
   57 |       "label": "Allerheiligen",
   58 |       "at": [
   59 |         "2022-11-01"
   60 |       ]
   61 |     },
   62 |     {
   63 |       "label": "Mariä Empfängnis",
   64 |       "at": [
   65 |         "2022-12-08"
   66 |       ]
   67 |     },
   68 |     {
   69 |       "label": "some holidays 2022/2023",
   70 |       "at": [
   71 |         "2022-12-24",
   72 |         "2023-01-02"
   73 |       ]
   74 |     }
   75 |   ]
   76 | }
detected strict mode (queries outside of year frame from config will fail)
effective configuration:
- given 32 holidays within [2021-12-24, 2023-01-02]:
  + 2021-12-24
  + 2021-12-25
  + 2021-12-26
  + 2021-12-27
  + 2021-12-28
  + 2021-12-29
  + 2021-12-30
  + 2021-12-31
  + 2022-01-01
  + 2022-01-02
  + 2022-03-19
  + 2022-04-15
  + 2022-04-16
  + 2022-04-17
  + 2022-04-18
  + 2022-05-26
  + 2022-06-06
  + 2022-06-16
  + 2022-08-01
  + 2022-08-15
  + 2022-11-01
  + 2022-12-08
  + 2022-12-24
  + 2022-12-25
  + 2022-12-26
  + 2022-12-27
  + 2022-12-28
  + 2022-12-29
  + 2022-12-30
  + 2022-12-31
  + 2023-01-01
  + 2023-01-02
- working hours:
  + [7, 16] (application default)
evaluation:
detected strict mode (queries outside of year frame from config will fail)
- Day is not within year range of configuration
```

Retrieving a starter template for the configuration (default place is `$HOME/.arbejdstimer.json`):

```console
❯ arbejdstimer template
{
  "api": 1,
  "application": "arbejdstimer",
  "operator": "or",
  "holidays": [
    {
      "label": "public holiday",
      "at": [
        "2022-12-08"
      ]
    },
    {
      "label": "some holidays 2022/2023",
      "at": [
        "2022-12-23",
        "2023-01-02"
      ]
    }
  ],
  "working_hours": [8, 17]
}
```
... a minimal configuration not considering holidays and falling back on working hours within `[7, 16]`:

```console
❯ cat test/fixtures/basic/minimal-config.json
{
  "operator": "or"
}
```

## Version command

```console
❯ arbejdstimer version
Working hours (Danish arbejdstimer) or not? version 2022.10.22+parent.ae9945dd
```

## General help

```console
❯ arbejdstimer

 Usage: arbejdstimer [OPTIONS] COMMAND [ARGS]...

 Working hours (Danish arbejdstimer) or not?
 Given a configuration file detect if today is a work day and if at the time of request is a working hour.
 Return code of 0 indicates work time, 1 no work time, and 2 usage error.
 Additional help available per command adding the -h/--help option

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the arbejdstimer version and exit                                                                       │
│ --help     -h        Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ explain       Explain the answer to the question if now is a working hour (in addition to the return code 0 for yes, and 1 for no).  │
│ now           Silently answer the question if now is a working hour (per return code 0 for yes, and 1 for no).                       │
│ template      Write a template of a JSON configuration to standard out and exit                                                      │
│ version       Display the arbejdstimer version and exit                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Help on explain command

```console
❯ arbejdstimer explain --help

 Usage: arbejdstimer explain [OPTIONS]

 Explain the answer to the question if now is a working hour (in addition to the return code 0 for yes, and 1 for no).

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config   -c      <configpath>  Path to config file (default is $HOME/.arbejdstimer.json)                                       │
│ --day      -d      <date>        Day sought (default is today)                                                                   │
│ --strict   -s      <bool>        Enforce presence of farming dates in configuration (default is false if not provided)           │
│ --verbose  -v      <bool>        Be more verbatim providing the effective config values (default is false if not provided)       │
│ --help     -h                    Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Help on now command

```console
❯ arbejdstimer now --help

 Usage: arbejdstimer now [OPTIONS]

 Silently answer the question if now is a working hour (per return code 0 for yes, and 1 for no).

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config  -c      <configpath>  Path to config file (default is $HOME/.arbejdstimer.json)                                        │
│ --strict  -s      <bool>        Enforce presence of farming dates in configuration (default is false if not provided)            │
│ --help    -h                    Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Help on template command

```console
❯ arbejdstimer template --help

 Usage: arbejdstimer template [OPTIONS]

 Write a template of a JSON configuration to standard out and exit

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Help on version command

Why not :-)

```console
❯ arbejdstimer version --help

 Usage: arbejdstimer version [OPTIONS]

 Display the arbejdstimer version and exit

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
