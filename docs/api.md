# API

## Configuration API

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

## JSON Schema for Configuration API version 1

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
