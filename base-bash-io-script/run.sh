#!/usr/bin/env bash
set -e

function show_usage() {
echo "===================================================================================="
echo "=====               Runs a script with named parameters and help               ====="
echo "===================================================================================="
echo ""
echo "Usage: ./run.sh -p param -f fileParam [-o optionalParam]"
echo "-p param:                             Some help text for a required param"
echo "-f fileParam:                         Some more help text for the other required param, a file path"
echo "-o optionalParam:                     Some help text for the optional param. Defaults to 'defaultValue'"
echo ""
echo "Example:"
echo "./run.sh -p myParamValue -f \${PWD}/my-config.json -o \"My Custom Value\""
exit 1
}

colorizationRed='\033[0;31m'
colorizationWhite='\033[0;37m'
colorizationNoColor='\033[0m'
colorizationRedBg='\033[41m'
colorizationBoldBlack='\033[1;47;30m'
function red_message() {
	message=$1
	title=$2
	echo ""
	echo "========================================"
	echo -e "        ${colorizationWhite}${colorizationRedBg}  ${title}  ${colorizationNoColor}"
	echo -e "    ${message}"
	echo "========================================"
	echo ""
}

function warn() {
	message=$1
	red_message "${message}" "W A R N I N G"
}

function err() {
	message=$1
	red_message "${message}" "E R R O R"
}

function show_message() {
	message=$1
	echo ""
	echo "========================================"
	echo -e "        ${colorizationBoldBlack}${message}${colorizationNoColor}"
	echo "========================================"
	echo ""
}

function show_progress() {
	total=$1
	if [ -z "${total}" ]; then
		total=10
	fi
	time=$2
	if [ -z "${time}" ]; then
		time=3
	fi
	for i in $(seq 1 ${total}); do
		dots=$(printf '.%.0s' $(seq 1 $i))
		echo -ne "\r${dots} ${i}/${total}"
		sleep ${time}
	done
	echo ""
}

sedCmd="sed"
timeoutCmd="timeout"
if [[ "$OSTYPE" == "darwin"* ]]; then
	sedCmd="gsed"
	timeoutCmd="gtimeout"
fi

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#====== Basic Configuration
someVar="aVar"
waitLength=5
waitInterval=1
someRelativeFile="${scriptDir}/run.sh"

#====== Input and Validation
paramArg=""
fileParamArg=""
optionalParamArg="defaultValue"

while getopts ":p:f:o:" opt; do
	case $opt in
		p) paramArg="$OPTARG"
		;;
		f) fileParamArg="$OPTARG"
		;;
		o) optionalParamArg="$OPTARG"
		;;
		\?)
		err "Invalid option -$OPTARG" >&2
		show_usage
		;;
		*)
		show_usage
		;;
  esac
done

if [ -z "${paramArg}" ]; then
	err "No param provided"
	show_usage
fi

if [ -z "${fileParamArg}" ]; then
	err "No fileParam provided"
	show_usage
fi

if [ ! -f "${fileParamArg}" ]; then
	err "The file ${colorizationBoldBlack}${fileParamArg}${colorizationNoColor} does not exist."
	show_usage
fi

optionalText=""
if [ "${optionalParamArg}" != "defaultValue" ]; then
	optionalText="and '${optionalParamArg}'"
fi
show_message "Start processing '${fileParamArg}' with '${paramArg}' ${optionalText} for ${waitLength} intervals of ${waitInterval} seconds each."
show_progress ${waitLength} ${waitInterval}
show_message "Done."
