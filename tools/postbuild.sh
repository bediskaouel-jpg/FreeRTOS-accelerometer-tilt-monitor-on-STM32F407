#!/bin/bash
FW_VER_PATH=../src/Main/Inc

FW_VER=$(cat     "${FW_VER_PATH}"/fw_version.h  | grep "DMAIN_FW_VER_X"     | awk '{print $3}');
FW_VER=${FW_VER//U/}
MAJOR_VER=$(cat  "${FW_VER_PATH}"/fw_version.h  | grep "DMAIN_FW_VER_MAJOR" | awk '{print $3}');
MAJOR_VER=${MAJOR_VER//U/}
MINOR_VER=$(cat  "${FW_VER_PATH}"/fw_version.h  | grep "DMAIN_FW_VER_MINOR" | awk '{print $3}');
MINOR_VER=${MINOR_VER//U/}

echo "script post build is runningg -------------------------------------------------------------------------------------------"

mkdir -p -- ../binary
cd ../binary/

if [ -f "*.bin" ]; then
        rm *.bin
fi

cd ./
echo ${FW_VER}_${MAJOR_VER}_${MINOR_VER}
echo ${FW_VER}_${MAJOR_VER}_${MINOR_VER}> ./firmwareversion.txt

cp ../Release/LAB1_F407.bin ./bin_${FW_VER}_${MAJOR_VER}_${MINOR_VER}.bin

