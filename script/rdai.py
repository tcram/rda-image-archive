#! /usr/bin/env python3
#
# 2019-07-10 
# Colton Grainger 
# Adapted from https://github.com/rbeezer/mathbook/tree/dev/script

"""
rdai utility script
"""

# fakesection: imports and function definitions {{{ # 

from rdai import *

# we also include these (otherwise private) cli-message functions

def verbose(msg):
    """Write a message to the console on program progress"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 1:
            print('RDAI: {}'.format(msg))
    except NameError:
        print('RDAI: {}'.format(msg))

def debug(msg):
    """Write a message to the console with some raw information"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 2:
            print('RDAI-DEBUG: {}'.format(msg))
    except NameError:
        print('RDAI-DEBUG: {}'.format(msg))

#  1}}} # 

# fakesection: main {{{

# Parse command line
# Deduce some paths
# Read configuration file
# Switch on command line

import os.path, sys

# grab command line arguments
args = get_cli_arguments()
debug("CLI args {}".format(vars(args)))

# Report Python version in debugging output
msg = "Python version: {}.{}"
debug(msg.format(sys.version_info[0], sys.version_info[1]))

# directory locations relative to RDAI installation
rdai_dir = get_rdai_path()
rdai_schema_dir = os.path.join(rdai_dir, "schema")
rdai_script_dir = os.path.join(rdai_dir, "script")
rdai_user_dir = os.path.join(rdai_dir, "user")
debug("schema, script, and user directories: {}".format([rdai_schema_dir, rdai_script_dir, rdai_user_dir]))

# directory location for outputs
output_dir = os.path.abspath(args.output_dir)
debug("output directory: {}".format(output_dir))

# directory location for data
data_dir = os.path.abspath(args.data_dir)
debug("data directory: {}".format(data_dir))

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
# 1}}}
