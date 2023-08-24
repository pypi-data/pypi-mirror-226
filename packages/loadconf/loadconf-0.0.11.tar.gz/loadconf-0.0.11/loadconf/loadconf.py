#!/usr/bin/env python3
# Copyright (C) 2022 John Dovern
#
# This file is part of loadconf <https://codeberg.org/johndovern/loadconf>.
#
# loadconf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation version 3 of the License
#
# loadconf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# loadconf.  If not, see <http://www.gnu.org/licenses/>.

import csv
import json
import os
import pathlib
import re
import sys
from typing import Optional, Iterable, List, Dict


class Config:
    def __init__(
        self,
        program: str,
    ):
        self._program = program
        platform = sys.platform
        linux = ["linux", "linux2"]
        if platform in linux:
            self._platform = "linux"
        elif platform == "darwin":
            self._platform = "macos"
        else:
            self._platform = "windows"
        self.platform = self._platform
        self.__define_dirs__()
        self.files = {}
        self.settings = {}
        self.settings_files = {}
        self.stored = {}
        self.created = {}

    def associate_settings(
        self,
        settings: List,
        file: str,
    ):
        if file in self.files.keys():
            self.settings_files[file] = {}
        for key, value in self.settings.items():
            if key in settings:
                self.settings_files[file][key] = value

    def create_files(
        self,
        create_files: List,
    ):
        """
        Test if config files exist and create them if needed.
        """
        if self.config_dir is not None:
            dir = pathlib.Path(self.config_dir)
            if not dir.is_dir() and not dir.is_file():
                dir.mkdir(parents=True, exist_ok=True)
            elif dir.is_file():
                raise ValueError(f"ERROR: loadconf: config_dir is a file: {dir}")
        files = {}
        for file in create_files:
            if file in self.files.keys():
                files[file] = self.files[file]
            elif os.path.isabs(file):
                files[file] = file
        for key, value in files.items():
            f = pathlib.Path(value)
            if not f.is_file():
                f.touch()
                self.created[key] = f

    def create_template(
        self,
        files: List,
    ):
        for key, value in self.settings_files.items():
            # If not one of the given files, or a created file skip
            if key not in files or key not in self.created.keys():
                continue
            file_path = self.created[key]
            data = ""
            for k, v in value.items():
                data += f"{k} = {v}\n"
            file_path.write_text(data)

    def define_files(
        self,
        user_files: Dict,
        config_dir: Optional[str] = "",
    ):
        """
        Define files and automatically find where they should go
        """
        # If program wants to use it's own dir then ensure it exists
        if not config_dir or not os.path.isdir(config_dir):
            config_dir = self.config_dir
        for key, value in user_files.items():
            file = os.path.join(config_dir, value)
            self.files[key] = file

    def define_settings(
        self,
        settings: Dict,
    ):
        """
        Users may not provide all settings that are relevant to your program.
        If you want to set some defaults, this makes it easy.
        Acceptable settings values include str, bool, int, and float.
        Other values will be ignored.
        """
        for key, value in settings.items():
            if not isinstance(value, (str, bool, int, float)):
                continue
            self.settings[key] = value

    def read_conf(
        self,
        user_settings: List,
        read_files: List,
        delimiter: str = "=",
        comment_char: str = "#",
    ):
        """
        Read a config file
        """
        files = []
        # File may be an actual file or a key value from defined_files
        for file in read_files:
            if file in self.files.keys():
                files.append(self.files[file])
            elif os.path.isfile(file):
                files.append(file)
        # Regex object for subbing delimiter
        r = re.compile(rf"\\{delimiter}")
        # Read the desired files
        for file in files:
            if not os.path.isfile(file):
                continue
            i = 0
            with open(file) as f:
                reader = csv.reader(
                    f,
                    delimiter=delimiter,
                    escapechar="\\",
                    quoting=csv.QUOTE_NONE,
                )
                for row in reader:
                    i += 1
                    # User did not properly escape their file
                    if len(row) > 2:
                        raise csv.Error(f"Too many fields on line {i}: {row}")
                    # Skip settings with no value
                    elif len(row) < 2:
                        continue
                    # Skip comments
                    elif row[0].startswith(comment_char):
                        continue
                    # Strip white space and sub delimiter if needed
                    setting_name = row[0].strip()
                    setting_name = r.sub(delimiter, setting_name)
                    setting_value = row[1].strip()
                    setting_value = r.sub(delimiter, setting_value)
                    # Try turning qualifying strings into bools and ints
                    try:
                        setting_value = eval(setting_value.capitalize())
                    except (NameError, SyntaxError):
                        pass
                    # Ignore user defined settings that program doesn't care about
                    if setting_name in user_settings:
                        self.settings[setting_name] = setting_value

    def store_files(
        self,
        files: Iterable,
        json_file: bool = False,
    ):
        """
        Store an entire file line by line in a list or load a json file.
        """
        # Temp dict to store at self.dict_name
        temp_dict = {}
        # Check if user gave a dict
        if isinstance(files, dict):
            read_dict = files
            read_files = files.values()
        # If user didn't give a dict ensure they have run define_files()
        elif hasattr(self, "files"):
            read_dict = self.files
            read_files = files
        # User has passed a list that does not have any meaning
        else:
            return
        # Begin reading files that user wants stored
        for key, file in read_dict.items():
            if not os.path.isfile(file):
                continue
            if not key in read_files:
                continue
            if json_file:
                try:
                    with open(file, "r") as data:
                        jdata = json.load(data)
                except json.decoder.JSONDecodeError:
                    jdata = {}
                temp_dict[key] = jdata
            else:
                with open(file) as f:
                    temp_dict[key] = []
                    for line in f:
                        temp_dict[key].append(line.rstrip())
        self.stored.update(temp_dict)

    def __define_dirs__(self):
        # Else define the locations where config files should get stored
        if self._platform == "linux":
            config_path = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            data_path = os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        elif self._platform == "macos":
            config_path = os.path.expanduser("~/Library/Preferences/")
            data_path = os.path.expanduser("~/Library/Application Support/")
        else:
            user_name = os.getlogin()
            config_path = f"C:\\Users\\{user_name}\\AppData\\Local"
            data_path = config_path
        assert config_path
        assert data_path
        self.config_path = config_path
        self.data_data = data_path
        self.config_dir = os.path.join(config_path, self._program)
        self.data_dir = os.path.join(data_path, self._program)


if __name__ == "__main__":
    # Create user object to read files and get settings
    user = Config(program="test_program")
    # Define some basic settings, files, etc.
    user_settings = {
        "test_bool": False,
        "test_str": "Some string",
        "test_int": 1,
    }
    config_files = {
        "test_rc": "test_programrc",
        "test_store": "test_program_store",
    }
    files = list(config_files.keys())
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.associate_settings(settings, "test_rc")
    user.create_files(create_files=files)
    user.create_template(["test_rc"])
    user.read_conf(user_settings=settings, read_files=["test_rc"])
    user.store_files(files=["test_store"])
    print(f"config_dir {user.config_dir}")
    print(f"files: {user.files}")
    print(f"settings: {user.settings}")
    print(f"settings_files: {user.settings_files}")
    print(f"stored: {user.stored}")
    print(f"created: {user.created}")
