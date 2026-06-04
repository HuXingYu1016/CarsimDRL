""" normal vehicle model """
import os
from rich import print
from rich.panel import Panel
from rich.text import Text
from pycarsimlib.logger import initialize_logging
logger = initialize_logging(__name__)


class NormalVehicle:
    """ class to define normal vehicle model """
    def __init__(self) -> None:
        logger.info("Vehicle type : NormalVehicle")
        self._define_import_params()
        self._define_export_params()
        self.echo_command_for_carsim_gui()

    def _define_import_params(self):
        """ define control inputs """
        self.import_label_array = [
            "IMP_STEER_SW",
            "IMP_MY_OUT_D1_L",
            "IMP_MY_OUT_D1_R",
            "IMP_MY_OUT_D2_L",
            "IMP_MY_OUT_D2_R"
        ]

    def _define_export_params(self):
        """ define variables to be observed """
        # TODO: Set CarSim outputs
        self.export_label_array = [
            'Lat_Veh',
            "Vx",
            "Vy",
            "AVz",
            "Rho_Road",
            "Station",
            "Beta",
            "Steer_L1",
            "Steer_R1",
            "Steer_SW",
            "Fx_L1",
            "Fx_R1",
            "Fx_L2",
            "Fx_R2",
            "Steer_DM",
            "VxTarget",
            "MyRR_L1",
            "MyRR_R1",
            "MyRR_L2",
            "MyRR_R2",
            "Roll",
            "Yaw",
            "X_DM_10",
            "Y_DM_10",
            "Xo",
            "Yo"
        ]

    def get_import_labels(self):
        """ getter of import value labels """
        return self.import_label_array.copy()

    def get_export_labels(self):
        """ getter of export value labels """
        return self.export_label_array.copy()

    def echo_command_for_carsim_gui(self):
        """ input those commands into 'Additional Data' in the carsim gui. """
        logger.warn("Do not forget to set following variables on carsim gui.")

        # generate command for carsim gui
        _cmd = os.linesep

        # add commands for import variables
        for imp in self.import_label_array:
            _cmd += "IMPORT " + imp + " Replace 0.0! 1" + os.linesep

        # add commands for export variables
        for exp in self.export_label_array:
            _cmd += "EXPORT " + exp + " Replace 0.0! 1" + os.linesep

        panel = Panel(Text(_cmd))
        print(panel)

