# API

## Configuration API

Default configuration at `$HOME/.arbejdstimer.json` content from example at
`tests/fixtures/basic/holidays-config.json`:
```json
{
  "_meta": {
    "application": "arbejdstimer",
    "configuration_api_version": "1",
    "combination_with_defaults": "or"
  },
  "holidays": [
    {
      "label": "public holiday",
      "date_range": [
        "2021-12-08"
      ]
    },
    {
      "label": "company holidays 2021/2022",
      "date_range": [
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
  "additionalProperties": false,
  "$defs": {
    "_meta_type": {
      "title": "Meta",
      "description": "Properties to ensure applicability of configuration data to the specific application and version.",
      "type": "object",
      "properties": {
        "application": {
          "title": "Application Name",
          "description": "Name of the application this configuration targets.",
          "type": "string",
          "default": "arbejdstimer",
          "enum": [
            "arbejdstimer"
          ]
        },
        "configuration_api_version": {
          "title": "Application API Version",
          "description": "API version of the application this configuration targets.",
          "type": "string",
          "default": "1",
          "enum": [
            "1"
          ]
        },
        "combination_with_defaults": {
          "title": "Logic for Combination with Default Values",
          "description": "Logical operation to use when combining the given specific values with the application defaults.",
          "type": "string",
          "default": "or",
          "enum": [
            "and",
            "or",
            "xor"
          ]
        }
      },
      "required": [
        "application",
        "configuration_api_version"
      ],
      "additionalProperties": false
    },
    "date_range_type": {
      "title": "Date Ranges",
      "description": "Two dates are interpreted as inclusive range and 1, 3, or more dates are interpreted as a set of dates.",
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
      "description": "The optional labels shall aid editing of the configuration but only the date_range members impact the run time.",
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
          "date_range": {
            "$ref": "#/$defs/date_range_type"
          }
        },
        "required": [
          "date_range"
        ],
        "additionalProperties": false
      },
      "additionalItems": false
    },
    "working_hours_type": {
      "title": "Working Hours",
      "description": "The mandatory two entries are interpreted as inclusive range of 24 hour start and end integer values.",
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
    "_meta": {
      "$ref": "#/$defs/_meta_type"
    },
    "holidays": {
      "$ref": "#/$defs/holidays_type"
    },
    "working_hours": {
      "$ref": "#/$defs/working_hours_type"
    }
  }
}
```
