#!/bin/bash

# I could of course write status.sh in python... TODO

# Help menu
print_help() {
cat <<-HELP
This script is used to quickly get the status of the Automation project on the Raspberry Pi

Usage: ./${0##*/}
Optional arguments: --email -e --help -h
Example: ./${0##*/} --email
HELP
}

main(){
    echo %%% TODOs preceded or trailed by 4 or 5 asterisks %%%
    git grep -n '\*\*\*\*\sTODO|TODO\s\*\*\*\*'
    # alternative: https://github.com/ggreer/the_silver_searcher

    echo %%%%%%%%%%%%%%%%%%%% py.test %%%%%%%%%%%%%%%%%%%%
    echo pytest --ignore=adventures # TODO use string to do exactly what is shown here TODO no -v: keep it short underneath git status
    echo
    pytest --ignore=adventures # not needed anymore, but left here as example.

    echo
    echo %%%%%%%%%%%%%%%%%%%% git status  %%%%%%%%%%%%%%%%
    git status

    print_help

    echo %%% trailing spaces %%%
    git grep -n '\s$'
}

# Run email test() {
test_email(){
cat <<-EMAIL
%%%%%%%%%%%%%%%%%%%% emails %%%%%%%%%%%%%%%%%%%%%
NO EMAIL TESTING CONFIGURED YET!!

EMAIL
}
# read -r -p "Send test email to mjvandermeulen's phone? [y/yes] " response
# response=${response,,}    # tolower
# if [[ "$response" =~ ^(yes|y)$ ]]
# then
#     echo TODO change to code that sends email
# else
#     echo No email sent
# fi

# Parse Command Line Arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --arg1=*)
        arg1="${1#*=}"
        ;;
    --arg2=*)
        arg2="${1#*=}"
        ;;
    --help|-h)
        print_help
        exit 0
        ;;
    --email|-e)
        run_test_email=true
        ;;
    *)
      printf "############################################################\n"
      printf "# Error: Invalid argument, run --help for valid arguments. #\n"
      printf "############################################################\n"
      exit 1
  esac
  shift
done

main

if [[ $run_test_email = "true" ]]; then
   test_email
fi
