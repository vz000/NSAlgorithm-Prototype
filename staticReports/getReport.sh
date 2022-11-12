#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
AUTH="API_KEY" # not including this in the remote repo :-)
UPLOAD=$(curl -F file=@/home/v/Repo/Safe/$1 http://127.0.0.1:8001/api/v1/upload -H Authorization:$AUTH)
echo "$UPLOAD" # ONLY FOR TROUBLESHOOTING, THIS MUST NOT BE INCLUDED IN THE FINAL VERSION.
UPLOAD_STATUS=$(jq -r ".status" <<<$UPLOAD)
FILE_NAME=$(jq -r ".file_name" <<<$UPLOAD)
FILE_TYPE=$(jq -r ".scan_type" <<<$UPLOAD) # ALSO KNOWN AS SCAN_TYPE
HASH=$(jq -r ".hash" <<<$UPLOAD)

if [[ $UPLOAD_STATUS == "success" ]];
then
	echo -e "\nUpload was ${GREEN}successful${NC} for file ${FILE_NAME} of type ${FILE_TYPE}\n"
else
	echo -e "\n${RED}Upload failed for file ${FILE_NAME}"
	echo -e "\n${RED}File couldn't be analyzed"
	echo "$1" >> deletedAPKs.txt
	REMOVE="./Safe/$1"
	rm $REMOVE
	exit 1
fi

STATIC_SCAN=$(curl -X POST --url http://127.0.0.1:8001/api/v1/scan --data scan_type="$FILE_TYPE&file_name=$FILE_NAME&hash=$HASH" -H Authorization:$AUTH)
echo "$STATIC_SCAN" > analyze.json # RAW AND UGLY
SAVE_STATIC_SCAN=$(python -m json.tool < analyze.json)
echo "$SAVE_STATIC_SCAN" > analyze.json # FORMATTED
# ALL THE JSON ATTRIBUTES ARE NOT GOING TO BE USED.
EXTRACTION_RESULT=$(python get_attributes.py)
rm analyze.json
JSON_FILE="$HASH.json"
if [[ $EXTRACTION_RESULT = "success" ]];
then
	echo -e "\n${GREEN}Successful analysis"
	DESTINATION="./JSONReports/$JSON_FILE"
	echo -e "${NC}JSON file: $JSON_FILE"
	mv $JSON_FILE $DESTINATION
	echo ${FILE_NAME} >> saveAPKs.txt
else
	echo -e "\n${RED}File couldn't be analyzed"
	echo "$1" >> deletedAPKs.txt
	REMOVE="./Safe/$1"
	rm $REMOVE
fi
