#!/usr/bin/bash
# Change to the desired directory
cd /home/ubuntu/L1_App
# Set environment variables
export CL_KEYSTORE=key.p12 CL_KEYALIAS=walletalias CL_PASSWORD=welcome123
# Generate using cl-keytool
java -jar /home/ubuntu/L1_App/cl-keytool_1.9.1.jar generate
# Run the Java program
java "-Xms1024M" "-Xmx3G" "-Xss256K" -cp /home/ubuntu/L1_App/tessellation-core-assembly-1.9.1.jar org.tessellation.Main run-validator --ip 18.132.210.35 --public-port 9065 --p2p-port 9066 --cli-port 9067 -e testnet --collateral 0 &