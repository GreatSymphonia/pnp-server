# Changelog

## [V1.0]

### Added

-	Added persistent logging feature to save ZTP running-logs
-	Added a toggle switch to enable/disable persistent logging by flipping the flag ‘log_tofile = False’ in the script
-	Starting IOS XE 17.2.x and above the persistent log files will be saved under '/flash/guest-share/ztp.log' , In older version logs will be located at '/flash/ztp.log'
-	Skipped MD5 checksum on software versions where it is unsupported due to a known limitation(see Troubleshooting / Known Issues below)
-	Minor stability improvements 


### Changed

- None

### Fixed

- None


#############################################################

  changes by thl-cmk@outlook.com
 
#############################################################

2022-11-03: moved print to log_info/log_critical function
            splitted software_images in models and software_images --> can reuse images for more than one models
            start convert strings to fStrings
            
