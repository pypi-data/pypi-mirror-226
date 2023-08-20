import ast
import os.path
import re
from collections import defaultdict
from configparser import ConfigParser
from copy import deepcopy
from mymulti_key_dict import MultiKeyDict

import touchtouch
from flatten_any_dict_iterable_or_whatsoever import fla_tu, set_in_original_iter

nested_dict = lambda: defaultdict(nested_dict)


def parse_data_from_config_file(
    cfgfile: str, encoding: str = "utf-8", onezeroasboolean: bool = False
):
    """
    Parses data from a configuration file and returns values, keys, and a MultiKeyDict object.

    Args:
        cfgfile (str): Path to the configuration file or the config as string.
        encoding (str, optional): Encoding of the file. Defaults to "utf-8".
        onezeroasboolean (bool, optional): Treat "1" and "0" as boolean values. Defaults to False.

    Returns:
        tuple: A tuple containing:
            - list: List of tuples containing keys and values extracted from the configuration.
            - MultiKeyDict: A MultiKeyDict object containing the extracted data.
    """

    def load_config_file_vars(cfgfile: str, onezeroasboolean: bool = False) -> tuple:
        """
        Loads variables from a configuration file and returns a tuple of copied dictionary and list of flattened data.

        Args:
            cfgfile (str): Path to the configuration file or the config as string.
            onezeroasboolean (bool, optional): Treat "1" and "0" as boolean values. Defaults to False.

        Returns:
            tuple: A tuple containing:
                - dict: A copied dictionary of configuration sections and values.
                - list: List of flattened data.
        """
        pars2 = ConfigParser()
        if os.path.exists(cfgfile):
            pars2.read(cfgfile, encoding=encoding)
        else:
            pars2.read_string(cfgfile)

        cfgdictcopy, cfgdictcopyaslist = copy_dict_and_convert_values(
            pars2, onezeroasboolean=onezeroasboolean
        )
        return cfgdictcopy, cfgdictcopyaslist

    def copy_dict_and_convert_values(
        pars: ConfigParser, onezeroasboolean: bool = False
    ):
        r"""
        converts configuration data from the configparser format into a more convenient structure (MultiKeyDict)
        that allows for efficient data manipulation using multi-level keys. This transformation can make it
        simpler to access and update configuration values. Besides that, it handles type conversions

        Parses data from a configuration file and returns values, keys, and a MultiKeyDict object.

        Args:
            cfgfile (str): Path to the configuration file.
            encoding (str, optional): Encoding of the file. Defaults to "utf-8".
            onezeroasboolean (bool, optional): Treat "1" and "0" as boolean values. Defaults to False.

        Returns:
            tuple: A tuple containing:
                - list[tuple]: List of tuples containing keys and values extracted from the configuration.
                - MultiKeyDict: A MultiKeyDict object containing the extracted data.

        Example:
            from konfigleser import write_config_file,parse_data_from_config_file
            example = '''
            [DEFAULT]
            ServerAliveInterval = 45
            Compression = yes
            CompressionLevel = 9
            ForwardX11 = yes

            [forge.example]
            User = hg

            [topsecret.server.example]
            Port = 50022
            ForwardX11 = no
            '''

            cfgtestfile = 'c:\\testestest.ini'
            cfgtestfileoutput = 'c:\\testestestout.ini'

            # Create example configuration file
            with open(cfgtestfile, mode='w', encoding='utf-8') as f:
                f.write(example)

            # Parse, modify, and write configuration data
            valuesandkeys, configdict = parse_data_from_config_file(cfgfile=cfgtestfile)

            valuesandkeys, configdict = parse_data_from_config_file(cfgfile=example) # also possible
            print(f'{valuesandkeys=}')
            print(f'{configdict=}')
            for ra in range(4):
                configdict[[f"cat1{ra}", "value1"]] = ra * 2
                configdict[[f"othercat1{ra}", "value2"]] = ra * ra
                configdict[[f"cat1{ra}", "value3", 'value31']] = ra * 2
                configdict[[f"othercat1{ra}", "value4",'value31']] = ra * ra
                configdict[[f"cat1{ra}", "value5", 'value31','value21']] = ra * 2
                configdict[[f"othercat1{ra}", "value6",'value31','value21']] = ra * ra
            write_config_file(d=configdict, filepath=cfgtestfileoutput)
            print('----------------------------------------------------')

            valuesandkeys, configdict = parse_data_from_config_file(cfgfile=cfgtestfileoutput)
            print(f'{valuesandkeys=}')
            print(f'{configdict=}')

            print('----------------------------------------------------')

            #output:

            valuesandkeys=[('hg', ('forge.example', 'user')), (50022, ('topsecret.server.example', 'port')), (False, ('topsecret.server.example', 'forwardx11')), ('45', ('DEFAULT', 'serveraliveinterval')), ('yes', ('DEFAULT', 'compression')), ('9', ('DEFAULT', 'compressionlevel')), ('yes', ('DEFAULT', 'forwardx11'))]
            configdict={'DEFAULT': {'compression': 'yes',
             'compressionlevel': '9',
             'forwardx11': 'yes',
             'serveraliveinterval': '45'},
             'forge.example': {'user': 'hg'},
             'topsecret.server.example': {'forwardx11': False,
             'port': 50022}}
            ----------------------------------------------------
            valuesandkeys=[('hg', ('forge.example', 'user')), (50022, ('topsecret.server.example', 'port')), (False, ('topsecret.server.example', 'forwardx11')), (0, ('cat10', 'value1')), (0, ('cat10', 'value3', 'value31')), (0, ('cat10', 'value5', 'value31', 'value21')), (0, ('othercat10', 'value2')), (0, ('othercat10', 'value4', 'value31')), (0, ('othercat10', 'value6', 'value31', 'value21')), (2, ('cat11', 'value1')), (2, ('cat11', 'value3', 'value31')), (2, ('cat11', 'value5', 'value31', 'value21')), (1, ('othercat11', 'value2')), (1, ('othercat11', 'value4', 'value31')), (1, ('othercat11', 'value6', 'value31', 'value21')), (4, ('cat12', 'value1')), (4, ('cat12', 'value3', 'value31')), (4, ('cat12', 'value5', 'value31', 'value21')), (4, ('othercat12', 'value2')), (4, ('othercat12', 'value4', 'value31')), (4, ('othercat12', 'value6', 'value31', 'value21')), (6, ('cat13', 'value1')), (6, ('cat13', 'value3', 'value31')), (6, ('cat13', 'value5', 'value31', 'value21')), (9, ('othercat13', 'value2')), (9, ('othercat13', 'value4', 'value31')), (9, ('othercat13', 'value6', 'value31', 'value21')), ('45', ('DEFAULT', 'serveraliveinterval')), ('yes', ('DEFAULT', 'compression')), ('9', ('DEFAULT', 'compressionlevel')), ('yes', ('DEFAULT', 'forwardx11'))]
            configdict={'DEFAULT': {'compression': 'yes',
             'compressionlevel': '9',
             'forwardx11': 'yes',
             'serveraliveinterval': '45'},
             'cat10': {'value1': 0,
             'value3': {'value31': 0},
             'value5': {'value31': {'value21': 0}}},
             'cat11': {'value1': 2,
             'value3': {'value31': 2},
             'value5': {'value31': {'value21': 2}}},
             'cat12': {'value1': 4,
             'value3': {'value31': 4},
             'value5': {'value31': {'value21': 4}}},
             'cat13': {'value1': 6,
             'value3': {'value31': 6},
             'value5': {'value31': {'value21': 6}}},
             'forge.example': {'user': 'hg'},
             'othercat10': {'value2': 0,
             'value4': {'value31': 0},
             'value6': {'value31': {'value21': 0}}},
             'othercat11': {'value2': 1,
             'value4': {'value31': 1},
             'value6': {'value31': {'value21': 1}}},
             'othercat12': {'value2': 4,
             'value4': {'value31': 4},
             'value6': {'value31': {'value21': 4}}},
             'othercat13': {'value2': 9,
             'value4': {'value31': 9},
             'value6': {'value31': {'value21': 9}}},
             'topsecret.server.example': {'forwardx11': False,
             'port': 50022}}
            ----------------------------------------------------
            # file:
            [DEFAULT]
            serveraliveinterval = 45
            compression = yes
            compressionlevel = 9
            forwardx11 = yes

            [forge.example]
            user = hg

            [topsecret.server.example]
            port = 50022
            forwardx11 = False

            [cat10]
            value1 = 0
            value3 = {'value31': 0}
            value5 = {'value31': {'value21': 0}}

            [othercat10]
            value2 = 0
            value4 = {'value31': 0}
            value6 = {'value31': {'value21': 0}}
            ....
        """
        copieddict = deepcopy(pars.__dict__["_sections"])
        try:
            if "_defaults" in pars.__dict__:
                copieddict["DEFAULT"] = deepcopy(pars.__dict__["_defaults"])
        except Exception:
            pass
        flattli = fla_tu(pars.__dict__["_sections"])
        for value, keys in flattli:
            if not re.search(r"^(?:[01])$", str(value)):
                try:
                    valuewithdtype = pars.getboolean(*keys)
                except Exception:
                    try:
                        valuewithdtype = ast.literal_eval(pars.get(*keys))
                    except Exception:
                        valuewithdtype = pars.get(*keys)
            else:
                if onezeroasboolean:
                    valuewithdtype = pars.getboolean(*keys)
                else:
                    valuewithdtype = ast.literal_eval(pars.get(*keys))

            set_in_original_iter(iterable=copieddict, keys=keys, value=valuewithdtype)

        g = list(fla_tu(copieddict))
        return copieddict, g

    dictmulti, valuesandkeys = load_config_file_vars(
        cfgfile=cfgfile, onezeroasboolean=onezeroasboolean
    )
    return valuesandkeys, MultiKeyDict(dictmulti)


def write_config_file(d, filepath, encoding="utf-8"):
    """
    Writes the data from a dictionary into a configuration file.

    Args:
        d (dict): The dictionary containing the data to be written.
        filepath (str): Path to the output configuration file.
        encoding (str): encoding - defaults to "utf-8"
    """
    parser = ConfigParser()
    parser.read_dict(d)
    touchtouch.touch(filepath)

    with open(filepath, "w", encoding=encoding) as configfile:
        parser.write(configfile)


