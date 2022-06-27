# Change History

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
