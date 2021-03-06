#!/usr/bin/env python3

# In this sample you will see how the settings of an ethernet network
# interfaces on a server host can be retrieved and updated using the
# REST API. The difference between the 5.0 and 6.0 API is the
# is_cable_linked attribute changes from a boolean to a enum. The
# string value of the enum is one of: YES, NO, UNKNOWN.
# Unknown means we cannot detect if the interface has a physical
# cable linked to it because some reason such as the interface is
# down atm. You can use the sample to set an interface to down status
# by choosing disabled role.  Then call the sample again and see the
# value of is_cable_linked attribute is set to UNKNOWN.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # First we have to create our client
    client = client_module.RestApiClient(version='6.0')

    # Have the user input the server Id.
    server_Id = input(
        'Please enter the Id of the server. The Id needs to be an integer.\n')

    # Have the user input the device name.
    iface = input(
        'Please enter the device name of the ethernet interface. ' +
        'The current role of the interface needs to be regular, monitor or ' +
        'disabled for the updating API to work.\n')

    # Send in the Get request
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/ethernet?filter=device_name=' + \
        iface
    SampleUtilities.pretty_print_request(client, endpoint, 'GET')
    response = client.call_api(endpoint, 'GET')

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if (response.code != 200):
        print('Failed to retrieve the network interface')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # get the current settings
    response_body = json.loads(response.read().decode('utf-8'))
    if (len(response_body) == 0):
        print('The network interface ' + iface + " does not exists.")
        sys.exit(1)
    print('Current settings:')
    print(json.dumps(response_body, indent=4))

    # update the settings
    proceed = input(
        'Continue running this sample will guide you to change the  ' +
        'settings of the network interface. ' +
        'Are your sure to continue (Y/N)? ')

    if (proceed != 'Y'):
        sys.exit(1)
    # Have the user input the new settings.
    role = input(
        'Please enter the role (regular, monitor or disabled) ' +
        'of the network interface.\n')
    ipversion = None
    ip = None
    mask = None
    isAutoIP = "N"
    ipversion = input('Please enter the version (ipv4 or ipv6) ' +
                      'of the new IP.\n')
    if (role == "regular"):

        if (ipversion == "ipv4"):
            ip = input('Please enter the new IP.\n')
            mask = input('Please enter the new netmask.\n')
        else:
            isAutoIP = input(
                'Do you want the IP to be automatically assigned (Y/N)? ')
            if (isAutoIP != "Y"):
                ip = input('Please enter the new IP.\n')

    ifaceObj = {"role": role, "ipversion": ipversion,
                "ip": ip, "mask": mask,
                "is_auto_ip": isAutoIP == "Y"}
    print("update the settings to: ")
    print(json.dumps(ifaceObj))
    headers = {}
    headers['Content-Type'] = 'application/json'
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/ethernet/' + iface
    SampleUtilities.pretty_print_request(
        client, endpoint, 'POST', headers=headers)
    response = client.call_api(
        endpoint, 'POST', headers=headers, data=json.dumps(ifaceObj).encode())
    if (response.code != 200):
        print('Failed to update the network interface ' + iface)
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    else:
        print(iface + ' is successfully updated\n')

if __name__ == "__main__":
    main()
