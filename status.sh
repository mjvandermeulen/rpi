#!/bin/bash

# Help menu
print_help() {
cat <<-HELP
This script is used to quickly get the status of the Automation project on the Raspberry Pi

Usage: ./${0##*/}
Optional arguments: --email -e --help -h
Example: ./${0##*/} --email
HELP
exit 0
}

main(){
    echo
    echo %%%%%%%%%%%%%%%%%%%% git status  %%%%%%%%%%%%%%%%
    git status

    echo %%%%%%%%%%%%%%%%%%%% py.test %%%%%%%%%%%%%%%%%%%%
    echo NO TESTING YET!!! # py.test # no -v: keep it short underneath git status
    echo
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
        ;;
    --email|-e)
        run_test_email=true
        ;;
    *)
      printf "************************************************************\n"
      printf "* Error: Invalid argument, run --help for valid arguments. *\n"
      printf "************************************************************\n"
      exit 1
  esac
  shift
done

main

if [[ $run_test_email = "true" ]]; then
   test_email
fi
