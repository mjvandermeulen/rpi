# Dummy Modules

## Mac

These Modules (Libraries / Classes) are needed to avoid linting errors when working on the Mac.
Include the following code in the shell that is used by VS Code on the Mac:

```
# mjvandermeulen
# Raspberry Pi Automation python path declarations, for linting on Mac.
# Make sure this path does not exist on the R Pi
if [ -d /Volumes/Home\ Directory/Programming/Automation/mac_dummy_libraries ]; then
    export PYTHONPATH=$PYTHONPATH:/Volumes/Home\ Directory/Programming/Automation/mac_dummy_libraries
fi
```

## R Pi ALERT

Disable this module when running code on the R Pi!
```
