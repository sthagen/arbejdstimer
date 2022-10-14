# Change History

## 2022.10.14

* Added function to calaculate the remaining workdays of a year given a day and constraining months
* Extended constraint month parameters with default values to allow for less noisy call sites

## 2022.10.13

* Added service functions for monthly and yearly workday counts in between constraints

## 2022.10.9

* Added functions day_count, day_count_from_date, date_from_fractional_year, and fractional_year_from_date
 
## 2022.10.5

* Added API method to query the count of working days per month of a year

## 2022.10.3

* Added API methods to query all working days of a year
* Migrated to pyproject.toml based packaging

## 2022.7.24

* Bumped dependencies for development and test
* Moved documentation to https://codes.dilettant.life/docs/arbejdstimer
* Moved tracker to https://todo.sr.ht/~sthagen/arbejdstimer
* Moved normative source repo to https://git.sr.ht/~sthagen/arbejdstimer

## 2022.6.27

* Updated dependencies

## 2021.12.29

* Created a way to directly display the active configuration (values) by adding a -v/--verbose flag to the explain command (implements #11)
* Enhanced the failed parse of configuration file error report (implements #15)
* Prepared programmatic API by providing defaults as named module level values (implements #16)

## 2021.12.28

* Provided the CLI template command to generate an example configuration (implements #4)
* Added tests to cover the new functionalities
* Updated documentation

## 2021.12.27

* Replaced the current configuration loading with model based approach (implements #12)
* Increased test (branch) coverage

## 2021.12.22

* Started a data driven configuration validation behind the moon (not yet active) 
* Split the now command into silent and verbose (#9)
* Make the daily working hours configurable ("Make the daily working hours configurable" #8)
* Fixed regression ("Recover usability with no holidays" #7)

## 2021.12.21

* Added configuration handling (using the holidays defined within)

## 2021.12.5

* Initial release on PyPI
