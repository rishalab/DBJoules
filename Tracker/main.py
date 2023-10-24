from Tracker.utils import (
    is_file_opened,
    define_carbon_index,
    get_params,
    set_params,
    NotNeededExtensionError,
)
from ram_metrics import RAM
from cpu_metrics import CPU, all_available_cpu
import os
import time
import platform
import pandas as pd
import numpy as np
import uuid
import sys
import warnings

sys.path.insert(0, ".\hardware")

# from gpu_metrics import GPU, all_available_gpu
sys.path.insert(0, "./")


FROM_mWATTS_TO_kWATTH = 1000*1000*3600
FROM_kWATTH_TO_MWATTH = 1000


class IncorrectMethodSequenceError(Exception):
    pass


"""
    This class method initializes a Tracker object and creates fields of class object
                
    Parameters
    ----------
    project_name: str
    file_name: str
    Name of file to save the the results of calculations.
    measure_period: float
    Period of power consumption measurements in seconds.
    The more period the more time between measurements.
    The default is 10
    emission_level: float
    The mass of CO2 in kilos, which is produced  per every MWh of consumed energy.
    Default is None
    alpha_2_code: str
    Default is None
    region: str
    Default is None
    cpu_processes: str
    if cpu_processes == "current", then calculates CPU utilization percent only for the current running process
    if cpu_processes == "all", then calculates full CPU utilization percent(sum of all running processes)
                
    Returns
    -------
    Tracker: Tracker
    Object of class Tracker

"""


class Tracker:
    def __init__(
        self,
        project_name=None,
        file_name=None,
        measure_period=10,
        emission_level=None,
        # alpha_2_code=None,
        # region=None,
        cpu_processes="current",
        pue=1,
        ignore_warnings=False,
    ):
        self._ignore_warnings = ignore_warnings
        if (type(measure_period) == int or type(measure_period) == float) and measure_period <= 0:
            raise ValueError("\'measure_period\' should be positive number")
        if file_name is not None:
            if type(file_name) is not str and not (file_name is True):
                raise TypeError(
                    f"'file_name' parameter should have str type, not {type(file_name)}")
            if type(file_name) is str and not file_name.endswith('.csv'):
                raise NotNeededExtensionError(
                    f"'file_name' name need to be with extension \'.csv\'")
        self._params_dict = get_params()  # define default params
        self.project_name = project_name if project_name is not None else self._params_dict[
            "project_name"]
        self.file_name = file_name if file_name is not None else self._params_dict[
            "file_name"]
        self._measure_period = measure_period if measure_period is not None else self._params_dict[
            "measure_period"]
        self._pue = pue if pue is not None else self._params_dict["pue"]
        self.get_set_params(self.project_name, self.file_name,
                            self._measure_period, self._pue)

        # self._emission_level, self._country = define_carbon_index(
        #     emission_level, alpha_2_code, region)
        self._cpu_processes = cpu_processes
        self._start_time = None
        self._cpu = None
        self._ram = None
        self._id = None
        self._consumption = 0
        self._cpu_consumption = 0
        self._ram_consumption = 0
        self.duration = 0
        self._os = platform.system()
        if self._os == "Darwin":
            self._os = "MacOS"

    # This function returns default Tracker attributes values:

    def get_set_params(
        self,
        project_name=None,
        file_name=None,
        measure_period=None,
        pue=None
    ):
        dictionary = dict()
        if project_name is not None:
            dictionary["project_name"] = project_name
        else:
            dictionary["project_name"] = "default project name"
        if file_name is not None:
            dictionary["file_name"] = file_name
        else:
            dictionary["file_name"] = "emission.csv"
        if measure_period is not None:
            dictionary["measure_period"] = measure_period
        else:
            dictionary["measure_period"] = 10
        if pue is not None:
            dictionary["pue"] = pue
        else:
            dictionary["pue"] = 1
        set_params(**dictionary)

        return dictionary

    # This method returns consumption
    def consumption(self):
        return self._consumption

    # This method returns cpu consumption
    def cpu_consumption(self):
        return self._cpu_consumption

     # This method returns ram consumption
    def ram_consumption(self):
        return self._ram_consumption

    #   The Tracker's id. id is random UUID
    def id(self):
        return self._id

    #   emission_level is the mass of CO2 in kilos, which is produced  per every MWh of consumed energy.
    # def emission_level(self):
    #     return self._emission_level

    #   Period of power consumption measurements.
    def measure_period(self):
        return self._measure_period

    #   Dictionary with all the attibutes that should be written to .csv file
    '''
      Results is a table with the following columns:
                project_name
                start_time
                duration(s)
                power_consumption(kWTh)
                CO2_emissions(kg)
                CPU_name
                GPU_name
                OS
    '''

    def _construct_attributes_dict(self,):
        attributes_dict = dict()
        attributes_dict["id"] = [self._id]
        attributes_dict["project_name"] = [f"{self.project_name}"]
        attributes_dict["start_time"] = [
            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._start_time))}"]
        attributes_dict["duration(s)"] = [f"{time.time() - self._start_time}"]
        self.duration = f"{time.time() - self._start_time}"
        # print(self.duration)
        attributes_dict["cpu_power_consumption(kWh)"] = [
            f"{self._cpu_consumption}"]
        attributes_dict["ram_power_consumption(kWh)"] = [
            f"{self._ram_consumption}"]
        attributes_dict["power_consumption(kWh)"] = [f"{self._consumption}"]
        # attributes_dict["CO2_emissions(kg)"] = [
        #     f"{self._consumption * self._emission_level / FROM_kWATTH_TO_MWATTH}"]
        attributes_dict["CPU_name"] = [f"{self._cpu.name()}"]
        attributes_dict["OS"] = [f"{self._os}"]
        # attributes_dict["region/country"] = [f"{self._country}"]

        return attributes_dict

    # This method writes to .csv file calculation results.
    def _write_to_csv(self, add_new=False,):
        attributes_dict = self._construct_attributes_dict()
        if not os.path.isfile(self.file_name):
            while True:
                if not is_file_opened(self.file_name):
                    open(self.file_name, "w").close()
                    tmp = open(self.file_name, "w")
                    pd.DataFrame(attributes_dict).to_csv(
                        self.file_name, index=False)
                    tmp.close()
                    break
                else:
                    time.sleep(0.5)

        else:
            while True:
                if not is_file_opened(self.file_name):
                    tmp = open(self.file_name, "r")
                    attributes_dataframe = pd.read_csv(self.file_name)
                    attributes_array = []
                    for element in attributes_dict.values():
                        attributes_array += element

                    if attributes_dataframe[attributes_dataframe['id'] == self._id].shape[0] == 0:
                        attributes_dataframe.loc[attributes_dataframe.shape[0]
                                                 ] = attributes_array
                    else:
                        row_index = attributes_dataframe[attributes_dataframe['id']
                                                         == self._id].index.values[-1]
                        # check, if it's necessary to add a new row to the dataframe
                        if add_new:
                            attributes_dataframe = pd.DataFrame(
                                np.vstack((
                                    attributes_dataframe.values[:row_index+1],
                                    attributes_array,
                                    attributes_dataframe.values[row_index+1:]
                                )),
                                columns=attributes_dataframe.columns
                            )
                        else:
                            attributes_dataframe.loc[row_index] = attributes_array
                    attributes_dataframe.to_csv(self.file_name, index=False)
                    tmp.close()
                    break
                else:
                    time.sleep(0.5)
        self._mode = "run time" if self._mode != "training" else "training"
        return attributes_dict

    ''' 
    This class method is a function, that gets executed when a Tracker gets started 
    "measure_period" It calculates CPU, GPU and RAM power consumption and writes results to a .csv file 
    '''

    def _func_for_sched(self, add_new=False):
        self._cpu.calculate_consumption()
        cpu_consumption = self._cpu.get_consumption()
        ram_consumption = self._ram.calculate_consumption()
        tmp_comsumption = 0
        tmp_comsumption += cpu_consumption
        tmp_comsumption += ram_consumption
        tmp_comsumption *= self._pue
        self._consumption += tmp_comsumption
        self._cpu_consumption = cpu_consumption*self._pue
        self._ram_consumption = ram_consumption*self._pue
        return self._write_to_csv(add_new)

    '''
    This  method starts the Tracker work. It initializes fields of CPU and GPU classes,
    initializes scheduler, puts the self._func_for_sched function into it and starts its work.
    '''

    def start(self):
        self._cpu = CPU(cpu_processes=self._cpu_processes,
                        ignore_warnings=self._ignore_warnings)
        self._ram = RAM(ignore_warnings=self._ignore_warnings)
        self._id = str(uuid.uuid4())
        self._mode = "first_time"
        self._start_time = time.time()

    '''
    This  method stops the Tracker work. 
    It also writes to file final calculation results.
    '''

    def stop(self, ):
        if self._start_time is None:
            raise Exception(
                "Need to first start the tracker by running tracker.start()")
        self._func_for_sched()
        self._mode = "shut down"


# decorator function
def track(func):
    def inner(*args, **kwargs):
        tracker = Tracker()
        tracker.start()
        try:
            print("tracker")
            returned = func(*args, **kwargs)
        except Exception:
            tracker.stop()
            del tracker
            raise Exception
        tracker.stop()
        print(tracker._construct_attributes_dict())
        del tracker
        return returned
    return inner
