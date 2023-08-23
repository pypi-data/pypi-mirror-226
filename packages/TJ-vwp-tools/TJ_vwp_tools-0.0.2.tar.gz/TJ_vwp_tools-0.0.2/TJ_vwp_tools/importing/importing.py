# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:28:51 2023

@author: anba

Import data from the vwp raw output
"""


#%% imports
import pandas as pd 
import numpy as np 
import os ,sys, datetime

#sys.path.insert(1, r'C:\Users\anba\Desktop\Projects\TJ-vwp-tools\TJ-vwp-tools\plotting')
from ..plotting.matplotlib_shell import subplots



#%%
class imports:
    class GEOKON_VWP:
        """
        Class for managing GEOKON VWP data 
        """
        def __init__(self,vwp_fpath,metadata_fpath,**kwargs):
            
            ## import the vwp file 
            logger_data, sensor_data = self.read_vwp_file(vwp_fpath)
            
            
            ## update class fields
            self.n_sensors = len(sensor_data['reading'])
            self.sensor_data = sensor_data 
            self.logger_data = logger_data
            self.name = logger_data['logger_name'][0]
            self.timestamps = self.logger_data['datetime']
            self.n_samples = len(self.timestamps)
            
            
            self.aux_data = {} # dict to store auxillary data 
            self.aux_data['density_water'] = 1000*np.ones(self.n_samples) # timeseries of water density (g/cm3
            self.aux_data['barometric_pressure'] = np.zeros(self.n_samples) # timeseries of barometric pressure (psi)
    
            
            class metadata():
                def __init__(self, VWP, meta_fpath):
                    
                    meta = self.read_vwp_metadata(meta_fpath)
                    mask = meta['Well_ID'] == VWP.name
                    meta = meta.loc[mask]
                    
                    self.well_ID = meta['Well_ID'].to_numpy()
                    self.sensor_ID= meta['Sensor_ID'].to_numpy()
                    self.serial_no= meta['Serial_No'].to_numpy()
                    self.sensor_model=meta['Sensor_Model'].to_numpy()
                    self.pressure=meta['Pressure(Mpa)'].to_numpy()
                    self.reading_zero = meta['Digit Zero Reading'].to_numpy()
                    self.temp_zero= meta['T Zero Reading (K0)'].to_numpy()
                    self.G= meta['G (psi)'].to_numpy()
                    self.K= meta['K(Psi/C)'].to_numpy()
                    self.sensor_depth= meta['Sensor Depth (ft bgs)'].to_numpy()
                    self.survey_point_no= meta['Survey Point No'].to_numpy()
                    self.northing= meta['Northing'].to_numpy()
                    self.easting= meta['Easting'].to_numpy()
                    self.elevation= meta['Elevation'].to_numpy()
                    self.desc= meta['Desc'].to_numpy()
                    
                    
                def read_vwp_metadata(self,fpath):
                    """
                    read vwp metadata spreadsheet
                    
    
                    Parameters
                    ----------
                    fpath : str
                        full path to the csv file containing metadata.
            
                    Returns
                    -------
                    df: pandas dataframe
                        parsed metadata
    
                    """
                    df = pd.read_csv(fpath)
    
                    return df
                    
                    
                    
            
            class plotting:
                def __init__(self,vwp):
                    self._vwp = vwp
                    
                    
                def timeseries(self, field_name = 'water_elevation'):
                    """
                    Generate a timeseries plot for the field
                
                    Parameters
                    ----------
                    field_name : str, optional
                        field name to plot. The default is 'water_elevation'. can plot any fields
                        by their key name in VWP.sensor_data
                
                
                    """
                  
                
                    fig,ax = subplots(figwidth = 7.5, figheight = 4)
                    
                    for i in range(self._vwp.n_sensors):
                        x = self._vwp.timestamps
                        y = self._vwp.sensor_data[field_name][i,:]
                        
                        ax.plot(x,y, label = f'Sensor {i+1}')
                    
                    ax.legend()
                    ax.set_xlabel('Time')
                    ax.set_ylabel(f'{field_name} (ft)')
                    ax.set_title(self._vwp.name)
                    
                    
            self.meta = metadata(self,metadata_fpath)
            self.plot = plotting(self)      
            
        def set_barometric_pressure(self,baro):
            """
            import barometric pressure data. 
        
            Parameters
            ----------
            baro: GEOKON_barologger
                barologger data structure
        
            """
            
        
            ## method to add pressure data 
            pressure = [] # get the closes timestep with barometric presure data for each timestep in the vwp data
            for ti in self.timestamps:
                dt = abs(ti - baro.timestamps)
                idx = np.argmin(dt)
                pressure.append(baro.pressure[idx])
                
            
            self.aux_data['barometric_pressure'] = pressure 
            
        def set_water_density(self,t,rho):
            """
            set the water density (g/cm3) 
    
            Parameters
            ----------
            t : numpy array of numpy64 timestamps
                timestamp for each density value
            rho : numpy array
                timeseries of density values 
    
            """
    
            ## method to add pressure data 
            water_density = [] # get the closes timestep with barometric presure data for each timestep in the vwp data
            for ti in self.timestamps:
                dt = abs(ti - t)
                idx = np.argmin(dt)
                water_density.append(rho[idx])
            
            self.aux_data['density_water'] = np.array(water_density)
            
            
        def calculate_water_level(self):
            """
            calculate the water depth and water elevation (in ft)from sensor data. 
            Accounts for variable water density. 
        
            """
    
            p1 = self.meta.G.T*(self.sensor_data['reading'].T - self.meta.reading_zero) + self.meta.K*(self.sensor_data['therm'].T - self.meta.temp_zero) # sensor pressure
            p0 = self.aux_data['barometric_pressure'] # ambient pressure
            p = (p1.T - p0)*6894.76 #pressure (from psi to n/cm2)
            wl = p/(self.aux_data['density_water']*9.81)*3.28084 # wl in meters  
            we = np.add(self.meta.elevation - self.meta.sensor_depth.T.T,wl.T).T
            
            self.sensor_data['water_level'] = wl
            self.sensor_data['water_elevation'] = we
            
            
    
            
        def read_vwp_file(self,fpath):
            """
            read a csv file containing the raw VWP data. 
        
            Parameters
            ----------
            fpath : str
                full path to the csv file containing raw data.
        
            Returns
            -------
            logger_data : dict
                dictionary containing the logger data (timestamps, logger name, battery
                voltage etc..). Timeseries data are stored as numpy arrays.
            sensor_data : list of dicts
                list of dictionaries containing the raw sensor data for each sensor
                (reading and thermisistor values). Timeseries data are stored as numpy 
                arrays.
        
            """

            df = pd.read_csv(fpath) # import the csv file contaiing raw vwp data
            df.dropna(how='all', axis=1, inplace=True)
            # determine the numbeer of sensors in thge file
       
            n_sensors = len([i for i in df.columns if i.startswith('Reading')])
            n_samples = len(df)
            
    
        
            ## add shared variable data (logger data)
            logger_data =  {
                            'datetime': pd.to_datetime(dict(year=df.Year, month=df.Month, day=df.Day, minute = df.Minute, hour = df.Hour, second = df.Seconds)).to_numpy(),
                            'logger_name': df['Logger Name'].to_numpy(),
                            'batt_voltage': df['Battery Voltage(v)'].to_numpy(),
                            'internal_temp ': df['Internal Temp(C)'].to_numpy()
                            }
            
            
            
            reading = np.zeros((n_sensors,n_samples))
            therm = np.zeros((n_sensors,n_samples))
            
            
            if n_sensors >1:
    
                for i in range(n_sensors):
                    data = {'reading': df[f'Reading_{str(i+1).zfill(2)} (Digits)'].to_numpy(),
                            'therm':df[f'Therm_{str(i+1).zfill(2)} (C)'].to_numpy() }
                    
                    reading[i,:] = df[f'Reading_{str(i+1).zfill(2)} (Digits)'].to_numpy()
                    therm[i,:] = df[f'Therm_{str(i+1).zfill(2)} (C)'].to_numpy()
            else:
                reading = df['Reading (Digits)'].to_numpy()
                therm = df['Thermistor (C)'].to_numpy() 
                    
            sensor_data = {'reading': reading,
                           'therm':therm}     
            
            return logger_data,sensor_data        
                
    
            
    
        
    
    class GEOKON_barologger:
        def __init__(self, fpath, G = 0.000947, zero_reading =4957.3, zero_temp = 15):
            data = self.read_barologger(fpath)
            self.data = data
            self.timestamps = self.data['datetimes']
            
            
            self.G = G # set defualt G parameter (psi/dg)
            self.zero_reading = zero_reading # zero digit at install 
            self.zero_temp = zero_temp # C zero temperature at install
            
            
    
        def set_G(self,G):
            """
            set the instrument G value psi/dg. 
            
            This gauge factor best describes the performance of the load cell at 
            moderate to higher loads This linear gauge factor describes the slope 
            of the best fit line drawn through the calibration data points and the 
            reading where the line intersects the zero load point on the load axis 
            is called the 'Regression Zero' shown on the calibration sheet. The 
            instrument's calibration report shows the data from which the linear 
            gauge factor (G) and second order polynomial coefficients are derived. 
    
    
            Parameters
            ----------
            G : float
                G  value (psi/dg).
            """
            
            
            self.G = G
            
            #re-calculate pressure when changed
            self.calculate_pressure()
            
        def set_zero_reading(self,zero_reading):
            """
            set the logger initial zero reading. 
            
            An initial zero reading establishes a baseline measurement, from which 
            all subsequent data values are calculated.In general, the initial zero 
            reading is obtained by taking a measurement of the instrument on-site,
            prior to installation. Use of this field zero reading, instead of using
            the factory zero reading, will improve the accuracy of your calculated 
            data values. On-site zero readings should closely coincide with the 
            factory zero reading provided on the instrument’s calibration report 
            (after any necessary temperature and barometric pressure corrections 
             have been made). There are several different ways of taking an initial
            zero reading, and the exact steps involved vary by instrument. Consult 
            the instruction manual provided with the instrument for specific 
            instructions.
    
            Parameters
            ----------
            zero_reading : float
                zero_reading value .
            """
            self.zero_reading = zero_reading
            
            #re-calculate pressure when changed
            self.calculate_pressure()
            
        def set_zero_temp(self,zero_temp):
            """
            set the logger zero temp value.
            
            An initial zero reading establishes a baseline measurement, from which 
            all subsequent data values are calculated.In general, the initial zero 
            reading is obtained by taking a measurement of the instrument on-site,
            prior to installation. Use of this field zero reading, instead of using
            the factory zero reading, will improve the accuracy of your calculated 
            data values. On-site zero readings should closely coincide with the 
            factory zero reading provided on the instrument’s calibration report 
            (after any necessary temperature and barometric pressure corrections 
             have been made). There are several different ways of taking an initial
            zero reading, and the exact steps involved vary by instrument. Consult 
            the instruction manual provided with the instrument for specific 
            instructions.
    
            Parameters
            ----------
            zero_temp : float
                zero_temp value .
            """
            self.zero_temp = zero_temp 
            
            
            #re-calculate pressure when changed
            self.calculate_pressure()
        
        
        def calculate_pressure(self):
            self.pressure = (self.data['sensor_reading'] - self.zero_reading)*self.G
            
            
    
        def read_barologger(self,fpath):
            """
            read the barologger data
        
            Parameters
            ----------
            fpath : TYPE
                DESCRIPTION.
        
            Returns
            -------
            data : TYPE
                DESCRIPTION.
        
            """
            baro = pd.read_csv(fpath, header = 5, encoding = "ISO-8859-1")#, names = ['type','year'])
        
            data = {
            'datetimes': (pd.TimedeltaIndex(baro['Date and Time'], unit='d') + datetime.datetime(1899, 12, 30)).to_numpy(),
            'logger_name': baro['Logger Name'].to_numpy(),
            'batt_voltage': baro['Battery Voltage(v)'].to_numpy(),
            'internal temp': baro['Internal Temp(°C)'].to_numpy(),
            'sensor_reading': baro['Sensor Reading(dg) - Channel1'].to_numpy(),
            'sensor temp': baro['Sensor Temp(°C) - Channel1'].to_numpy(),
            'array no': baro['Array #'].to_numpy()
            }
            
            
            return data    
    
    
        
            
    
    
    
