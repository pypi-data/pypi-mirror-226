# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of AccidentallyTheCables Utility Kit,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import re
import sys
import signal
import logging
import typing
from os import kill
from pathlib import Path
from json import loads as json_parse
from json import dumps as json_dump
from yaml import dump as yaml_dump
from yaml import safe_load as yaml_parse
from tomlkit import parse as toml_parse
from tomlkit import dumps as toml_dump

def toml_parser(content:str) -> dict[typing.Any,typing.Any]:
    """TOML Parse and unwrap
    @param str \c content Raw TOML string
    @retval dict[Any,Any] Dictionary from TOML
    """
    return toml_parse(content).unwrap()

class UtilFuncs:
    """Utility Functions
    """

    FILE_TYPE_MAP:dict[str,typing.Callable] = {
        ".yml": yaml_parse,
        ".yaml": yaml_parse,
        ".json": json_parse,
        ".toml": toml_parser
    }
    TYPE_OVERRIDE_MAP:dict[str,typing.Callable] = {
        "yaml": yaml_parse,
        "json": json_parse,
        "toml": toml_parser
    }
    OUTPUT_TYPE_MAP:dict[str,typing.Callable] = {
        "yaml": yaml_dump,
        "json": json_dump,
        "toml": toml_dump
    }

    shutdown:bool = False
    restart:bool = False

    @staticmethod
    def create_object_logger(obj:object) -> logging.Logger:
        """Create logging.Logger with Specified object Class Name
        @param object \c obj Object to Create Logger for
        @retval logging.Logger Logger Instance
        """
        classname:str = str(obj.__class__)
        classname = re.sub(r'^\<class \'(.*)\'>',r'\1',classname)
        return logging.getLogger(classname)

    @staticmethod
    def create_static_logger(classname:str) -> logging.Logger:
        """Create logging.Logger with Specified Name
        @param str \c classname Name of Logger to Create
        @retval logging.Logger Logger Instance
        """
        return logging.getLogger(classname)

    @staticmethod
    def dump_sstr(content:dict[typing.Any,typing.Any],output_type:str,**kwargs:typing.Any) -> str:
        """Dump Structured Data to String, Selectable Output Type.
        @param dict[Any,Any] \c content Content to dump
        @param str \c output_type Output Type, Allowed: yaml, json, toml
        @param kwargs \c kwargs kwargs passed to selected data dumper
        @retval str Structured Data as a string
        @exception LookupError Raised When Unable to Locate a a parser by file type, or the overridden type is invalid
        @exception RuntimeError Raised When Unable to Parse the specified file using the specified type (automatically, or overridden)

        kwargs:
            See the related kwargs for:
                json.dumps
                yaml.dump
                tomlkit.dumps
        """
        if output_type not in UtilFuncs.OUTPUT_TYPE_MAP.keys():
            raise LookupError("Output Type is not valid",output_type)
        dumper:typing.Callable = UtilFuncs.OUTPUT_TYPE_MAP[output_type]
        try:
            output:str = dumper(content,*kwargs)
        except BaseException as e:
            raise RuntimeError("Failed to output content",'.'.join([dumper.__class__.__name__,dumper.__name__]),e) from e
        return output

    @staticmethod
    def load_sfile(target_file:Path,override_type:str = "auto") -> dict[typing.Any,typing.Any]:
        """Load Structured Data File, automatically determining data by file extension
        @param Path \c target_file Configuration File to Load
        @param str \c override_type Input Type Override, Allowed: yaml, json, toml, auto. Default: auto
        @retval dict Dictionary of Structured Data
        @exception LookupError Raised When Unable to Locate a a parser by file type, or the overridden type is invalid
        @exception RuntimeError Raised When Unable to Parse the specified file using the specified type (automatically, or overridden)

        Accepted File Extensions:
            YAML: .yaml, .yml
            JSON: .json
            TOML: .toml
        """
        if not target_file.exists():
            raise FileNotFoundError("Cannot Locate File",target_file.as_posix())

        parser:typing.Callable
        if override_type == "auto":
            file_type:str = ''.join(target_file.suffixes)
            if file_type not in UtilFuncs.FILE_TYPE_MAP.keys():
                raise LookupError("No Parser located for file type",file_type)
            parser = UtilFuncs.FILE_TYPE_MAP[file_type]
        else:
            if override_type not in UtilFuncs.TYPE_OVERRIDE_MAP.keys():
                raise LookupError("Override Type is not valid",override_type)
            parser = UtilFuncs.TYPE_OVERRIDE_MAP[override_type]
        try:
            with open(target_file,"r",encoding="utf-8") as f:
                loaded_config:dict[typing.Any,typing.Any] = parser(f.read())
                return loaded_config
        except BaseException as e:
            raise RuntimeError("Failed to Parse file",target_file.as_posix(),'.'.join([parser.__class__.__name__,parser.__name__]),e) from e

    @staticmethod
    def scan_dir(target_path:Path,
                 callback:typing.Callable[[Path,dict[str,typing.Any]],None],
                 callback_data:dict[str,typing.Any],
                 exclude_dirs:typing.Optional[list[re.Pattern]] = None,
                 exclude_files:typing.Optional[list[re.Pattern]] = None,
                 include_files:typing.Optional[list[re.Pattern]] = None
                ) -> None:
        """Scan A Directory, and Execute callback on discovered files, that do not match the exclusions
        @param Path \c target_path Path to Scan for Files
        @param typing.Callable[[Path,dict[str,Any]],None] \c callback Callback function to execute on each file
        @param dict[str,Any] \c callback_data Data to pass to the callback function
        @param list[re.Pattern] \c exclude_dirs (optional) Regex Compiled list of directory patterns to exclude
        @param list[re.Pattern] \c exclude_files (optional) Regex Compiled list of file patterns to exclude
        @param list[re.Pattern] \c include_files (optional) Regex Compiled list of file patterns to include
        """
        files:typing.Generator[Path, None, None] = target_path.glob("*")
        skip:bool = False
        for file in files:
            file_path:Path = Path(file)
            if file_path.is_dir():
                skip = False
                if exclude_dirs is not None:
                    for reg in exclude_dirs:
                        if reg.match(file_path.name):
                            skip = True
                            break
                if not skip:
                    UtilFuncs.scan_dir(target_path=file_path,callback=callback,callback_data=callback_data,exclude_dirs=exclude_dirs,exclude_files=exclude_files)
            if file_path.is_file():
                if include_files is not None:
                    skip = True
                    for reg in include_files:
                        if reg.match(file_path.name):
                            skip = False
                            break
                if exclude_files is not None:
                    skip = False
                    for reg in exclude_files:
                        if reg.match(file_path.name):
                            skip = True
                            break
                if not skip:
                    callback(file_path,callback_data)

    @staticmethod
    def deep_sort(input:dict[str,typing.Any]) -> dict[str,typing.Any]:
        """Deep Sort Dictionaries of varying data
        @param dict[str,typing.Any] \c input Input Dictionary
        @retval dict[str,typing.Any] New Sorted Dictionary
        """
        new_dict:dict[str,typing.Any] = {}
        for k,v in input.items():
            if isinstance(v,dict):
                new_dict[k] = dict(sorted(v.items()))
            elif isinstance(v,list):
                new_list:list[typing.Any] = []
                for i in v:
                    if isinstance(i,dict):
                        new_list.append(UtilFuncs.deep_sort(i))
                    else:
                        new_list.append(i)
                new_dict[k] = new_list
            else:
                new_dict[k] = v
        return new_dict

    @staticmethod
    def check_pid(pid:int) -> bool:
        """Check if PID exists (via os.kill(..,0))
        @param int \c pid PID to check
        @retval bool Whether PID exists or not
        """
        try:
            kill(pid,0)
        except OSError:
            return False
        return True

    # pylint: disable=unused-argument
    @staticmethod
    def sighandler(signum:int, frame:typing.Any) -> None:
        """Signal Handler
        @param signal.Signals \c signum Raised Signal
        @param Any \c frame Frame which raised the signal
        @retval None Nothing
        """
        logging.warning("Signal thrown")

        restart_signals:list[signal.Signals] = []
        shut_signals:list[signal.Signals] = []
        if sys.platform == "win32":
            shut_signals = [ signal.SIGINT, signal.CTRL_C_EVENT ]
            restart_signals = [ ]
        else:
            shut_signals = [ signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGTERM ]
            restart_signals = [ signal.SIGHUP ]

        if signum in shut_signals:
            UtilFuncs.shutdown = True
            logging.info("Shutting Down")
            return
        if signum in restart_signals:
            logging.info("Reloading Service")
            UtilFuncs.restart = True
            return
    # pylint: enable=unused-argument

    @staticmethod
    def register_signals() -> None:
        """Register Signal Handlers
        @retval None Nothing
        """
        signals:list[signal.Signals] = []
        if sys.platform == "win32":
            signals = [ signal.SIGINT ]
        else:
            signals = [ signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGTERM, signal.SIGHUP ]
        for sig in signals:
            signal.signal(sig,UtilFuncs.sighandler)
