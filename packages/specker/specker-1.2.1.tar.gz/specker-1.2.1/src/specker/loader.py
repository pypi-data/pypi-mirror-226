# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Specker JSON Specification Validator,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import os
import re
import json
import typing
import logging
from pathlib import Path

# from specker import content

if __name__ == "loader":
    # pylint: disable=import-error
    from content import SpecContent
    # pylint: enable=import-error
else:
    from .content import SpecContent

class SpecLoader:
    """Spec Loader and Handler
    """
    _specs:dict[str,dict[str,SpecContent]]
    _output:list[str]
    logger:logging.Logger

    @property
    def spec_names(self) -> list[str]:
        """Property: Spec Names
        @retval list[str] List of loaded Spec Names
        """
        return list(self._specs.keys())

    def __init__(self,spec_root:Path,debug:bool = False) -> None:
        """Initializer
        @param Path \c spec_root Location where .spec files are located
        @param bool \c debug Enable logging.DEBUG (logging.ERROR if False)
        """
        self.logger = logging.Logger("specker.loader.SpecLoader")
        self.logger.setLevel(logging.ERROR)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self._specs = {}

        specs_raw:dict[str,typing.Any] = {}
        spec_name:str = ""
        spec:dict[str,typing.Any] = {}

        self._output:list[str] = [
            "# Configuration Options",
            "Auto generated from .spec files"
        ]

        # pylint: disable=unused-variable
        for root, subdirs, files in os.walk(spec_root.resolve().as_posix()):
            spec_path:Path = Path(root).resolve()
            for file in files:
                if not file.endswith(".spec"):
                    continue
                self.logger.debug(f"Loading: {file}")
                try:
                    with open(spec_path.joinpath(file), "r", encoding="utf-8") as f:
                        spec = json.loads(f.read())
                except BaseException as e:
                    self.logger.error(f"Failed loading: {file}, {e}")
                    self.logger.debug(e,exc_info=True)
                    continue
                spec_name = re.sub(r'\.spec',"",file)
                specs_raw[spec_name] = spec
        for spec_file_name,spec_data in specs_raw.items():
            self._specs[spec_file_name] = {}
            for spec_name,spec in spec_data.items():
                spec["name"] = spec_name
                self._specs[spec_file_name][spec_name] = SpecContent(spec)
        # pylint: enable=unused-variable

    def compare(self,spec_file_name:str,content:dict[str,typing.Any]) -> bool:
        """Compare a Spec against Content
        @param str \c spec_file_name Spec File Name to pull
        @param dict[str,typing.Any] \c content Content to compare against Spec
        @retval bool Whether Check passed successfully
        """
        spec_file:dict[str,SpecContent] = self.get(spec_file_name)
        spec_keys:list[str] = list(spec_file.keys())
        config_keys:list[str] = list(content.keys())

        spec_pass:bool = True
        for k in content.keys():
            if k not in spec_keys:
                spec_pass = False
                self.logger.error(f"{k}: fail, invalid option")
                continue
        for k,spec in spec_file.items():
            if spec.get("name") not in config_keys and not spec.get("required"):
                self.logger.debug(f"{k} was not defined, using default value")
                content[k] = spec.get("default")
            elif spec.get("name") not in config_keys and spec.get("required"):
                spec_pass = False
                self.logger.error(f"{k}: fail, missing required option")
                continue
            if not spec.get("required") and content[k] is None:
                self.logger.debug(f"{k}: pass, not required, but is empty")
                continue
            if spec.get("spec_chain") is not None:
                spec_chain:str = spec.get("spec_chain")
                logging.debug(f"{k}: Contained Spec Chain, {spec_chain}. Checking")
                spec_pass = self.compare(spec_chain,content[k])
            if spec.type != type(content[k]) and spec.type != typing.Any:
                spec_pass = False
                self.logger.error(f"{k}: fail, must be {str(spec.type)}, got: {str(type(content[k]))}")
            else:
                self.logger.debug(f"{k}: pass, type match; need:{str(spec.type)}, got:{str(type(content[k]))}")
            value_pass:bool = self._check_valid_values(spec=spec,content=content[k],key_name=k)
            if not value_pass:
                spec_pass = False
        return spec_pass

    def _check_valid_values(self,spec:SpecContent,content:typing.Any,key_name:str) -> bool:
        """Compare Content against Spec
        @param SpecContent \c spec Spec to Check against
        @param Any \c content Content to Validate
        @param str \c key_name Name of Key content came from, for logging output
        @retval bool Whether value is a valid value
        """
        valid_values:list[typing.Any] = spec.get("values")
        if len(valid_values) > 0:
            values:str = ""
            for v in valid_values:
                values += f",{str(v)}"
            values = values.lstrip(",")
            if content not in valid_values:
                self.logger.error(f"{key_name}: fail, invalid value; must be one of: {values}")
                return False
            self.logger.debug(f"{key_name}: pass, value match, need:{values}, got:{str(content)}")
        return True

    def defaults(self,spec_file_name:str) -> dict[typing.Any,typing.Any]:
        """Get any Defined Defaults from a Spec
        @param str \c spec_file_name Spec File Name to pull
        @retval dict[Any,Any] Spec Defaults
        """
        spec_file:dict[str,SpecContent] = self.get(spec_file_name)
        content:dict[typing.Any,typing.Any] = {}

        for k,spec in spec_file.items():
            try:
                content[k] = spec.get("default")
                if spec.get("spec_chain") is not None:
                    spec_chain:str = spec.get("spec_chain")
                    content[k] = self.defaults(spec_chain)
            except AttributeError:
                continue
        return content

    def get(self,spec_file_name:str) -> dict[str,SpecContent]:
        """Get Spec Content for a Config
        @param str \c spec_file_name Name of Spec to Get
        @retval dict[str,SpecContent] Configuration Spec
        """
        return self._specs[spec_file_name]

    def write(self,output_file:Path) -> None:
        """Write Loaded Specs to a Markdown file
        @param Path \c output_file Target File Path
        """

        for spec_file_name,spec_data in self._specs.items():
            self._output.append(f"## Spec for {spec_file_name}\n")
            for spec in spec_data.values():
                self._output.append(str(spec))

        output_path:Path = output_file.resolve()
        output_file_str:str = output_path.as_posix()
        self.logger.info(f"Writing to file {output_file_str}")
        with open(output_path,"w", encoding="utf-8") as f:
            f.write("\n".join(self._output))
