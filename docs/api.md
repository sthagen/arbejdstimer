# API

## Configuration Data API

Default configuration at `$HOME/.arbejdstimer.json` content from example at
`tests/fixtures/basic/holidays-config.json`:
```json
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

### JSON Schema for Version 1

The configuration API schema is available at
https://github.com/sthagen/arbejdstimer/api/1/arbejdstimer-configuration-schema.json: 
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema#",
  "$id": "https://github.com/sthagen/arbejdstimer/api/1/arbejdstimer-configuration-schema.json",
  "title": "Working hours (Danish arbejdstimer) or not?",
  "description": "Representation of configuration information as a JSON document.",
  "type": "object",
  "$defs": {
    "dates": {
      "title": "Dates - Range or Set",
      "description": "Two dates are an inclusive range and 1, 3, or more dates represent a set of dates.",
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "string",
        "format": "date",
        "examples": [
          "2021-12-08"
        ],
        "default": ""
      },
      "additionalItems": false
    },
    "holidays_type": {
      "title": "Holidays",
      "description": "Optionally labeled dates of non-working days.",
      "type": "array",
      "minItems": 0,
      "uniqueItems": true,
      "items": {
        "type": "object",
        "properties": {
          "label": {
            "type": "string",
            "examples": [
              "public holiday"
            ],
            "default": ""
          },
          "at": {
            "$ref": "#/$defs/dates"
          }
        },
        "required": [
          "at"
        ]
      },
      "additionalItems": false
    },
    "working_hours_type": {
      "title": "Working Hours",
      "description": "Inclusive range of 24 hour start and end integer values.",
      "type": "array",
      "minItems": 2,
      "maxItems": 2,
      "items": {
        "type": "integer",
        "default": 0,
        "minimum": 0,
        "maximum": 23
      },
      "additionalItems": false
    }
  },
  "properties": {
    "api": {
      "title": "API Version",
      "description": "API version of the application this configuration targets.",
      "type": "integer",
      "default": 1,
      "minValue": 1
    },
    "application": {
      "title": "Application Name",
      "description": "Name of the application this configuration targets.",
      "type": "string",
      "default": "arbejdstimer",
      "enum": [
        "arbejdstimer"
      ]
    },
    "operator": {
      "title": "Logic for Combination with Default Values",
      "description": "Logic combining the given specific values with the application defaults.",
      "type": "string",
      "enum": [
        "and",
        "or",
        "xor"
      ]
    },
    "holidays": {
      "$ref": "#/$defs/holidays_type"
    },
    "working_hours": {
      "$ref": "#/$defs/working_hours_type"
    }
  },
  "required": [
      "operator"
  ]
}
```

## Commandline API

### `arbejdstimer`

Working hours (Danish arbejdstimer) or not?

Given a configuration file detect if today is a work day and
if at the time of request is a working hour.

Return code of 0 indicates work time, 1 no work time, and 2 usage error.

Additional help available per command adding the -h/--help option

**Usage**:

```console
$ arbejdstimer [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-V, --version`: Display the arbejdstimer version and exit  [default: False]
* `-h, --help`: Show this message and exit.

**Commands**:

* `explain`: Explain the answer to the question if now is...
* `now`: Silently answer the question if now is a...
* `template`: Write a template of a JSON configuration to...
* `version`: Display the arbejdstimer version and exit

#### `explain`

Explain the answer to the question if now is a working hour
(in addition to the return code 0 for yes, and 1 for no).

**Usage**:

```console
$ arbejdstimer explain [OPTIONS]
```

**Options**:

* `-c, --config <configpath>`: Path to config file [default: $HOME/.arbejdstimer.json]
* `-v, --verbose`: Be more verbatim providing the effective config values [default: False]
* `-h, --help`: Show this message and exit.

#### `now`

Silently answer the question if now is a working hour (per return code 0 for yes, and 1 for no).

**Usage**:

```console
$ arbejdstimer now [OPTIONS]
```

**Options**:

* `-c, --config <configpath>`: Path to config file [default: $HOME/.arbejdstimer.json]
* `-h, --help`: Show this message and exit.

#### `template`

Write a template of a JSON configuration to standard out and exit

**Usage**:

```console
$ arbejdstimer template [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

#### `version`

Display the arbejdstimer version and exit

**Usage**:

```console
$ arbejdstimer version [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

