#! /usr/bin/env python3
#
# 2019-07-10 
# Colton Grainger 

"""
Module and utilities script for RDA images (RDAI).
"""

# fakesection: utilities
# Copyright 2010-2016 Robert A. Beezer
# These functions were originally part of MathBook XML.
# MathBook XML is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 or version 3 of the
# 2016-05-05: this section should run under Python 2.7 and Python 3

def _verbose(msg):
    """Write a message to the console on program progress"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 1:
            print('RDAI: {}'.format(msg))
    except NameError:
        print('RDAI: {}'.format(msg))

def _debug(msg):
    """Write a message to the console with some raw information"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 2:
            print('RDAI-DEBUG: {}'.format(msg))
    except NameError:
        print('RDAI-DEBUG: {}'.format(msg))

def get_rdai_path():
    """Returns path of root of RDAI distribution"""
    import sys, os.path
    _verbose("discovering RDAI root directory from mbx script location")
    # full path to script itself
    rdai_path = os.path.abspath(sys.argv[0])
    # split "RDAI" executable off path
    script_dir, _ = os.path.split(rdai_path)
    # split "script" path off executable
    distribution_dir, _ = os.path.split(script_dir)
    _verbose("RDAI distribution root directory: {}".format(distribution_dir))
    return distribution_dir


def get_source_path(source_file):
    """Returns path to content to be acted upon"""
    import sys, os.path
    _verbose("discovering source directory from source location")
    # split path off filename
    source_dir, _ = os.path.split(source_file)
    return os.path.normpath(source_dir)

def get_executable(config, exec_name):
    "Queries configuration file for executable name, verifies existence in Unix"
    import os
    import platform
    import subprocess

    # http://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
    # suggests  where.exe  as Windows equivalent (post Windows Server 2003)
    # which  = 'where.exe' if platform.system() == 'Windows' else 'which'

    # get the name, but then see if it really, really works
    _debug('locating "{}" in [executables] section of configuration file'.format(exec_name))
    config_name = config.get('executables', exec_name)

    devnull = open(os.devnull, 'w')
    try:
        result_code = subprocess.call(['which', config_name], stdout=devnull, stderr=subprocess.STDOUT)
    except OSError:
        print('RDAI:WARNING: executable existence-checking was not performed (e.g. on Windows)')
        result_code = 0  # perhaps a lie on Windows
    if result_code != 0:
        error_message = '\n'.join([
                        'cannot locate executable with configuration name "{}" as command "{}"',
                        'Edit the configuration file and/or install the necessary program'])
        raise OSError(error_message.format(exec_name, config_name))
    _debug("{} executable: {}".format(exec_name, config_name))
    return config_name

def get_cli_arguments():
    """Return the CLI arguments in parser object"""
    import argparse
    parser = argparse.ArgumentParser(description='RDAI utility script', formatter_class=argparse.RawTextHelpFormatter)

    verbose_help = '\n'.join(["verbosity of information on progress of the program",
                              "  -v  is actions being performed",
                              "  -vv is some additional raw debugging information"])
    parser.add_argument('-v', '--verbose', help=verbose_help, action="count")

    component_info = [
        ('metadata', 'Metadata for data files.'),
        ('uuid', 'UUIDs for data files.'),
        ('bundle', 'Bundle from metadata, UUIDs, and data files.'),
        ('database', 'Database from bundle.'),
    ]
    component_help = 'Possible components are:\n' + '\n'.join(['  {} - {}'.format(info[0], info[1]) for info in component_info])
    parser.add_argument('-c', '--component', help=component_help, action="store", dest="component")

    metadata_input_info = [
        ('csv', 'Recursively read *.csv files in data directory. Format: "key","value".'),
        ('json', 'Recursively read *.json files in data directory. Format: {"key":"value"}.'),
        ('xml', 'Read single *.xml file from root of data directory. See docs for XML Schema.'),
    ]
    metadata_input_help = 'Possible metadata input formats are:\n' + '\n'.join(['  {} - {}'.format(info[0], info[1]) for info in metadata_input_info])
    parser.add_argument('-m', '--metadata-input', help=metadata_input_help, action="store", dest='metadata_input')

    parser.add_argument('-d', '--data-dir', help='path to data directory', action="store", dest='data_dir')
    parser.add_argument('-o', '--output-dir', help='path to output directory', action="store", dest='output_dir')
    return parser.parse_args()

    # "nargs" allows multiple options following the flag
    # separate by spaces, can't use "-stringparam"
    # stringparams is a list of strings on return
    # parser.add_argument('-p', '--parameters', nargs='+', help='stringparam options to pass to XSLT extraction stylesheet (option/value pairs)',
    #                      action="store", dest='stringparams')
    # # default to an empty string, which signals root to XSL stylesheet
    # parser.add_argument('-r', '--restrict', help='restrict to subtree rooted at element with specified xml:id',
    #                      action="store", dest='xmlid', default='')
    # parser.add_argument('-s', '--server', help='base URL for server (webwork only)', action="store", dest='server')

def sanitize_directory(dir):
    """Verify directory name, or raise error"""
    # Use with os.path.join, and do not sweat separator
    import os.path
    _verbose('verifying directory: {}'.format(dir))
    if not(os.path.isdir(dir)):
        raise ValueError('directory {} does not exist'.format(dir))
    return dir

# Certificate checking is buggy, exception raised is malformed
# 2015/10/07 Turned off verification in three places
# Command line warning can be disabled, requests.packages.urllib3.disable_warnings()
def sanitize_url(url):
    """Verify a server address, append a slash"""
    _verbose('validating, cleaning server URL: {}'.format(url))
    import requests
    try:
        requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        root_cause = str(e)
        msg = "There was a problem with the server URL, {}\n".format(url)
        raise ValueError(msg + root_cause)
    # We expect relative paths to locations on the server
    # So we add a slash if there is not one already
    if url[-1] != "/":
        url = url + "/"
    return url

def sanitize_alpha_num_underscore(param):
    """Verify parameter is a string containing only alphanumeric and undescores"""
    import string
    allowed = set(string.ascii_letters + string.digits + '_')
    _verbose('verifying parameter: {}'.format(param))
    if not(set(param) <= allowed):
        raise ValueError('param {} contains characters other than a-zA-Z0-9_ '.format(param))
    return param

def get_config_info(script_dir, user_dir):
    """Return configuation in object for querying"""
    import sys,os.path
    config_filename = "rdai.cfg"
    default_config_file = os.path.join(script_dir, config_filename)
    user_config_file = os.path.join(user_dir, config_filename)
    config_file_list = [default_config_file, user_config_file]
    # ConfigParser was renamed to configparser in Python 3
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser
    config = configparser.SafeConfigParser()
    _verbose("parsing configuration files: {}".format(config_file_list))
    files_read = config.read(config_file_list)
    _debug("configuration files used/read: {}".format(files_read))
    if not(user_config_file in files_read):
        msg = "using default configuration only, custom configuration file not used at {}"
        _verbose(msg.format(user_config_file))
    return config

def copy_data_directory(source_file, data_dir, tmp_dir):
    """Stage directory from CLI argument into the working directory"""
    import os.path, shutil
    _verbose("formulating data directory location")
    source_full_path, _ = os.path.split(os.path.abspath(source_file))
    data_full_path = sanitize_directory(os.path.join(source_full_path, data_dir))
    data_last_step = os.path.basename(os.path.normpath(data_full_path))
    destination_root = os.path.join(tmp_dir, data_last_step)
    _debug("copying data directory {} to working location {}".format(data_full_path, destination_root))
    shutil.copytree(data_full_path, destination_root)

def get_platform():
    """Return a string that tells us whether we are on Windows."""
    import platform
    return platform.system()

def is_os_64bit():
    """Return true if we are running a 64-bit OS.
    http://stackoverflow.com/questions/2208828/detect-64-bit-os-windows-in-python"""
    import platform
    return platform.machine().endswith('64')

def break_windows_path(python_style_dir):
    """Replace python os.sep with msys-acceptable "/" """
    import re
    return re.sub(r"\\", "/", python_style_dir)

# fakesection: main # 
# Copyright 2010-2016 Robert A. Beezer
# These functions were originally part of MathBook XML.

# Parse command line
# Deduce some paths
# Read configuration file
# Switch on command line

import os.path, sys

# grab command line arguments
args = get_cli_arguments()
_debug("CLI args {}".format(vars(args)))

# Report Python version in debugging output
msg = "Python version: {}.{}"
_debug(msg.format(sys.version_info[0], sys.version_info[1]))

# directory locations relative to RDAI installation
rdai_dir = get_rdai_path()
rdai_schema_dir = os.path.join(rdai_dir, "schema")
rdai_script_dir = os.path.join(rdai_dir, "script")
rdai_user_dir = os.path.join(rdai_dir, "user")
_debug("schema, script, user dirs: {}".format([rdai_schema_dir, rdai_script_dir, rdai_user_dir]))

# directory location for outputs
output_dir = os.path.abspath(args.output_dir)
_debug("output directory: {}".format(output_dir))

# directory location for data
data_dir = os.path.abspath(args.data_dir)
_debug("data directory: {}".format(data_dir))

config = get_config_info(rdai_script_dir, rdai_user_dir)
plat = get_platform()

if args.component == 'metadata':
    if args.metadata_input in ['csv','json','xml']:
        # TODO if catalog exists, raise warning and minimally update
        # TODO unless forcing flag
        create_catalog(data_dir, output_dir, args.metadata_input)
    else:
        raise NotImplementedError('cannot collect metadata from "{}" format'.format(args.metadata_input))

elif args.component == 'uuid':
    # TODO if uuid_dict exists, raise warning and minimally update
    # TODO unless forcing flag
    create_uuids(data_dir, output_dir)

elif args.component == 'bundle':
    # TODO test if uuid_dict and catalog exist
    merge_uuids_into_catalog(output_dir)
    # TODO optimize the tail-recursion
    unnormalize_catalog(output_dir)
    # TODO avoid frivilous updates with rsync (or shutils?)
    rename_by_uuids(data_dir, output_dir)

elif args.component == 'database':
    # TODO test if bundle exists
    # TODO unnormalized data as a DataFrame 
    # TODO read MySQL config
    # TODO inject (or update?) DataFrame

else:
    raise ValueError('the "{}" component is not a valid RDAI option'.format(args.component))
