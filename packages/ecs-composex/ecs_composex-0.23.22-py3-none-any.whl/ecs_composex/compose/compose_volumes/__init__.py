#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Class and functions to interact with the volumes: defined in compose files.
"""

from copy import deepcopy

from compose_x_common.compose_x_common import keyisset

from ecs_composex.common.logging import LOG
from ecs_composex.efs.efs_params import FS_REGEXP
from ecs_composex.efs.efs_params import RES_KEY as EFS_KEY

from .helpers import evaluate_plugin_efs_properties


class ComposeVolume:
    """
    Class to keep track of the Docker-compose Volumes

    When properties are defined, the priority in evaluation goes
    * x-efs
    * driver
    * driver_opts

    Assumed local when none else defined.
    """

    main_key = "volumes"
    driver_key = "driver"
    driver_opts_key = "driver_opts"
    efs_defaults = {
        "Encrypted": True,
        "LifecyclePolicies": [{"TransitionToIA": "AFTER_14_DAYS"}],
        "PerformanceMode": "generalPurpose",
    }

    def __init__(self, name, definition):
        self.name = name
        self.volume_name = name
        self.autogenerated = False
        self.definition = deepcopy(definition)
        self.is_shared = False
        self.services = []
        self.parameters = {}
        self.device = None
        self.cfn_volume = None
        self.efs_definition = {}
        self.use = {}
        self.lookup = {}
        self.type = "volume"
        self.driver = "local"
        self.external = False
        self.efs_definition = evaluate_plugin_efs_properties(
            self.definition, self.driver_opts_key
        )
        if self.efs_definition:
            LOG.info(
                f"volumes.{self.name} - Identified properties as defined by Docker Plugin"
            )
            self.type = "bind"
            self.driver = "nfs"
        elif (
            keyisset("external", self.definition)
            and keyisset("name", self.definition)
            and FS_REGEXP.match(self.definition["name"])
        ):
            LOG.warning(f"volumes.{self.name} - Identified a EFS to use")
            self.efs_definition = {"Use": self.definition["name"]}
            self.use = self.definition["name"]
        else:
            self.import_volume_from_definition()

    def import_volume_from_definition(self):
        if keyisset(EFS_KEY, self.definition):
            self.import_from_x_efs_settings()
        elif (
            not keyisset(EFS_KEY, self.definition)
            and keyisset(self.driver_key, self.definition)
            and not keyisset(self.driver_opts_key, self.definition)
        ):
            self.import_local_volume()
        else:
            self.type = "volume"
            self.driver = "local"
            self.is_shared = False

    def import_from_x_efs_settings(self):
        self.driver = "nfs"
        self.type = "bind"
        self.is_shared = True
        if keyisset("Lookup", self.efs_definition):
            self.lookup = self.efs_definition["Lookup"]
        elif keyisset("Use", self.efs_definition):
            self.use = self.efs_definition["Use"]
        if not self.use and not self.lookup:
            self.efs_definition = (
                self.definition[EFS_KEY]["Properties"]
                if keyisset("Properties", self.efs_definition)
                else self.efs_defaults
            )
            self.parameters = (
                self.definition[EFS_KEY]["MacroParameters"]
                if keyisset("MacroParameters", self.definition[EFS_KEY])
                else {}
            )

    def import_local_volume(self):
        if self.definition[self.driver_key] == "local":
            self.type = "volume"
            self.driver = "local"
            self.efs_definition = None
        elif (
            self.definition[self.driver_key] == "nfs"
            or self.definition[self.driver_key] == "efs"
        ):
            self.type = "bind"
            self.is_shared = True
            self.driver = "nfs"

    def __repr__(self):
        return self.name
