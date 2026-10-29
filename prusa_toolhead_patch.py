# coding=utf-8

import octoprint.plugin


class prusa_toolhead_patch(octoprint.plugin.OctoPrintPlugin, octoprint.plugin.RestartNeedingPlugin):
    def process_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode and gcode not in ("M106", "M107", "M201", "M203", "M221"):
            return None

        tool = self._printer.get_current_data().get("currentTool") or "0"

        if "T" not in gcode.upper():
            cmd = f"{cmd} T{tool}"

        return cmd,

    def get_update_information(self):
        return dict(
            prusa_toolhead_patch=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,
                type="httpheader",
                header_name="ETag",
                url="https://gist.githubusercontent.com/jneilliii/5198b0e5a0057f57821459dec510a659/raw/prusa_toolhead_patch.py",
                method="single_file_plugin"
            )
        )

__plugin_name__ = "Prusa Buddy Toolhead Fix"
__plugin_pythoncompat__ = ">=3.9,<4"
__plugin_license__ = "MIT"
__plugin_description__ = (
    "A workaround for Prusa Buddy firmware changes in "
    "v6.10 and later to resolve "
    '"Invalid tool reported" errors.'
)
__plugin_author__ = "Greg Anuzelli, jneilliii"
__plugin_version__ = "1.1.0"
__plugin_url__ = "https://gist.github.com/jneilliii/5198b0e5a0057f57821459dec510a659"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = prusa_toolhead_patch()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.process_gcode,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }