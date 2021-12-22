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
