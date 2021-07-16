#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
connect to specified network(s) or create an accesspoint
"""

import network
import time


def _do_connect(station, ssid, password, timeout) -> bool:
    """
    Establish the network connection.

    :param      station:   The network object
    :type       station:   network.WLAN
    :param      ssid:      The SSID of the network to connect to
    :type       ssid:      str
    :param      password:  The password of the network
    :type       password:  str
    :param      timeout:   Seconds to establish a connection to the network
    :type       timeout:   int, optional

    :returns:   Result of connection
    :rtype:     bool
    """
    is_successfull = False

    print('Connect to network "{}" with password "{}"'.format(ssid, password))

    try:
        station.disconnect()
        station.connect(ssid, password)
    except Exception as e:
        print('Failed to connect due to: {}'.format(e))
        return is_successfull

    # get current system timestamp
    now = time.time()

    # wait for connection no longer than the specified timeout
    while (time.time() < (now + timeout)):
        if station.isconnected():
            is_successfull = True
            return is_successfull
        else:
            pass

    return is_successfull


def connect(ssid=None,
            password=None,
            networks=None,
            timeout=5,
            reconnect=False) -> bool:
    """
    Connect to the configured network

    :param      ssid:      The SSID of the network to connect to
    :type       ssid:      list or str
    :param      password:  The password of the network
    :type       password:  list or str
    :param      networks:  Networks and passwords
    :type       networks:  dict, optional
    :param      timeout:   Seconds to establish a connection to the network
    :type       timeout:   int, optional
    :param      reconnect: Reconnect/disconnect from active connection
    :type       reconnect: bool, optional

    :returns:   Result of connection
    :rtype:     bool
    """
    is_connected = False

    # configure the WiFi as station mode (client)
    station = network.WLAN(network.STA_IF)

    # activate WiFi if not yet enabled
    if not station.active():
        station.active(True)

    if station.isconnected():
        current_network = station.config('essid')
        print('Already connected to "{}"'.format(current_network))
        if reconnect:
            station.disconnect()
            print('Disconnected from "{}"'.format(current_network))
        else:
            is_connected = True
            print(station.ifconfig())

            return is_connected

    if ((type(ssid) is str) and
        (type(password) is str)):
        # user provided string of single network to connect to
        print('Connect by single network and password')

        is_connected = _do_connect(station, ssid, password, timeout)
        print('Connected to {}: {}'.format(ssid, is_connected))
    elif ((type(ssid) is list) and
          (type(password) is list)):
        # user provided list of networks to connect to
        print('Connect by list of networks and passwords')

        for idx, s in enumerate(ssid):
            is_connected = _do_connect(station, s, password[idx], timeout)
            print('Connected to {}: {}'.format(s, is_connected))
            if is_connected:
                break
    elif ((networks is not None) and
          (type(networks) is dict)):
        # user provided dict of networks and passwords
        print('Connect by dict of networks and passwords')

        for ssid, password in networks.items():
            is_connected = _do_connect(station, ssid, password, timeout)
            print('Connected to {}: {}'.format(ssid, is_connected))
            if is_connected:
                break
    else:
        print('SSID and/or password neither list nor string')

    print('Stopped trying to connect to network {}'.format(time.time()))

    if is_connected:
        print('Connection successful')
    else:
        print('Connection timeout of failed to connect')
        print('Please check configured SSID and password')

    print(station.ifconfig())

    # return True if connection has been established
    return is_connected


def create_ap(ssid, password='', channel=11, timeout=5) -> bool:
    """
    Create an Accesspoint

    :param      ssid:      The SSID of the network to create
    :type       ssid:      str
    :param      password:  The password of the accesspoint
    :type       password:  str, optional
    :param      channel:   The channel of the accesspoint
    :type       channel:   int, optional
    :param      timeout:   Seconds to create an accesspoint
    :type       timeout:   int, optional

    :returns:   Result of connection
    :rtype:     bool
    """
    is_successfull = True

    # configure the WiFi as accesspoint mode (server)
    accesspoint = network.WLAN(network.AP_IF)

    # activate accesspoint if not yet enabled
    if not accesspoint.active():
        accesspoint.active(True)

    # check for open AccessPoint configuration
    if len(password):
        _authmode = network.AUTH_WPA_WPA2_PSK
    else:
        _authmode = network.AUTH_OPEN

    print('Create AccessPoint "{}" with password "{}"'.format(ssid, password))

    accesspoint.config(essid=ssid,
                       authmode=_authmode,
                       password=password,
                       channel=channel)

    # get current system timestamp
    now = time.time()

    # wait for success no longer than the specified timeout
    while (time.time() < (now + timeout)):
        if accesspoint.active():
            is_successfull = True
            break
        else:
            pass

    print('Stopped trying to setup AccessPoint {}'.format(time.time()))

    if is_successfull:
        print('AccessPoint setup successful')
    else:
        print('Connection timeout, failed to setup AccessPoint')

    print(accesspoint.ifconfig())

    return is_successfull
