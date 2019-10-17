# Dummy Modules

## Mac

These Modules (Libraries / Classes) are needed to avoid linting errors when working on the Mac.
Include the following code in rc script of the shell that is used by VS Code on the Mac:

```
# mjvandermeulen
# Raspberry Pi Automation python path declarations, for linting on Mac.
# Make sure this path does not exist on the R Pi
if [ -d /Volumes/Home\ Directory/Programming/Automation/mac_dummy_libraries ]; then
    export PYTHONPATH=$PYTHONPATH:/Volumes/Home\ Directory/Programming/Automation/mac_dummy_libraries
fi
```

## R Pi ALERT

make sure this module is not "enabled" on the R Pi!

- don't add the path in the R Pi rc script
- make sure the module is not in the home directory, or in the sys.path
