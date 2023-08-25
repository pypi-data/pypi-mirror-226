# -*- coding: utf-8 -*-
import pandas as pd
from simpledbf import Dbf5
from pathlib import Path
import numpy as np
from email.mime import base
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename
import os
import arcpy
from os.path import exists
import random, shutil,configparser
from tkinter import *
from tkinter import messagebox
from tkinter.tix import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

class autocorrect:
    @staticmethod
    def process_all():

        mxd = arcpy.mapping.MapDocument("Current")
        mxd.author = "Avirtech"
        arcpy.env.workspace = "CURRENT"
        global df
        df = arcpy.mapping.ListDataFrames(mxd)[0]


        ws = Tk()
        ws.title('Input Data')
        ws.geometry('380x450')

        ##  Mode Data
        label1 = Label(ws, text="Pilih Mode Data", font= ('Helvetica 12'))
        label1.pack(pady=5)
        # global mode_altitude,submitValues, submitValues2, submitValues3, output1, entry_1, entry_2, entry_3         #seharusnya dihapus
        def mode_altitude():
            # global mode, output1, choice_mode                                                                       #seharusnya dihapus
            choice_mode = mode.get()
            global output1
            if choice_mode == 10:
                output1 = "Flat Altitude"
            elif choice_mode == 20:
                output1 = "Adding DSM Altitude"
            elif choice_mode == 30:
                output1 = "Adding Local Altitude"
        mode = IntVar()
        Radiobutton(ws, text="Flat Altitude", variable=mode, value=10, command=mode_altitude).pack()
        Radiobutton(ws, text="Adding DSM Altitude", variable=mode, value=20, command=mode_altitude).pack()
        Radiobutton(ws, text="Adding Local Altitude", variable=mode, value=30, command=mode_altitude).pack()

        ##  Tinggi Pohon
        label2 = Label(ws, text="Perkiraan Tinggi Pohon", font= ('Helvetica 12'))
        label2.pack(pady=5)
        entry_1 = tk.StringVar()
        entry_widget_1 = tk.Entry(ws, textvariable=entry_1)
        entry_widget_1.pack()
        def submitValues():
            # print(entry_1.get())
            lbl.config(text = "Perkiraan Tinggi Pohon: {} meter".format(entry_1.get()))
        submit = tk.Button(ws, text="Input", command=submitValues)

        lbl = tk.Label(ws, text = "")
        lbl.pack()
        submit.pack()

        ## Local Altitude
        label3 = Label(ws, text="Local Altitude", font= ('Helvetica 12'))
        label3.pack(pady=5)
        entry_2 = tk.StringVar()
        entry_widget_2 = tk.Entry(ws, textvariable=entry_2)
        entry_widget_2.pack()
        def submitValues2():
            # print(entry_1.get())
            lbl2.config(text = "Local Altitude: {} meter".format(entry_2.get()))
        submit2 = tk.Button(ws, text="Input", command=submitValues2)

        lbl2 = tk.Label(ws, text = "")  
        lbl2.pack()
        submit2.pack()



        ##  Jarak Tinggi Terbang Drone terhadap Pohon/DSM
        label4 = Label(ws, text="Jarak Tinggi Terbang Drone Terhadap Pohon/DSM", font= ('Helvetica 12'))
        label4.pack(pady=5)

        entry_3 = tk.StringVar()
        entry_entry_3 = tk.Entry(ws, textvariable=entry_3)
        entry_entry_3.pack()
        def submitValues3():
            # print(entry_1.get())
            lbl3.config(text = "Jarak Tinggi Terbang Drone Terhadap Pohon/DSM {} meter".format(entry_3.get()))
        submit3 = tk.Button(ws, text="Input", command=submitValues3)

        lbl3 = tk.Label(ws, text = "")  
        lbl3.pack()
        submit3.pack()

        ws.mainloop()

        print("  ")
        print("  ")
        print("Mode Terbang Terpilih Adalah {}".format(output1))
        print("Perkiraan Tinggi Pohon Adalah {} meter".format(float(entry_1.get())))
        print("Local Altitude Adalah {} meter".format(float(entry_2.get())))
        print("Tinggi Terbang Terdahap Pohon/DSM Adalah {} Meter".format(float(entry_3.get())))
        print("  ")
        print("  ")





        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("","Lokasi data Jalur Terbang (.shp) dan data DSM Bila ada(.tif) ?")
        lokasi_dsm_shp = filedialog.askdirectory()
        messagebox.showinfo("","Lokasi output  ?")
        lokasi_output = filedialog.askdirectory()
        root.destroy

        entry_1 = float(entry_1.get())
        entry_2 = float(entry_2.get())
        entry_3 = float(entry_3.get())
        sum_flat_alt_height = ((entry_1)+(entry_3))
        sum_local_alt_height = ((entry_1)+(entry_2)+(entry_3))


        def flat_altitude():

            lokasi_output_folder = os.path.join(lokasi_output, "lokasi_output")
            os.mkdir(lokasi_output_folder)


            data_jalur_terbang = []
            for file in os.listdir(lokasi_dsm_shp):
                if file.endswith('.shp'):
                    data_jalur_terbang.append(os.path.join(lokasi_dsm_shp, file))


            arcpy.FeatureVerticesToPoints_management(data_jalur_terbang[0], os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), "ALL")

            arcpy.AddXY_management(os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'))

            arcpy.CalculateField_management(os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), "Id", "autoIncrement()", "PYTHON", "rec=0 \\ndef autoIncrement(): \\n global rec \\n pStart = 1  \\n pInterval = 1 \\n if (rec == 0):  \\n  rec = pStart  \\n else:  \\n  rec += pInterval  \\n return rec")

            arcpy.AddField_management("pt_vertice_pohon", "ketinggian", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("pt_vertice_pohon", "ketinggian", "{}".format(sum_flat_alt_height), "VB", "")


            data_dbf_xyval = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_vertice_pohon.dbf' in file:
                    data_dbf_xyval.append(os.path.join(lokasi_output_folder, file))

            path_dbf = Dbf5(data_dbf_xyval[0])
            df = path_dbf.to_dataframe()

            df['start_x'] = df['POINT_X']
            df['end_x'] = df.iloc[1:, :].loc[:, 'start_x']
            df['end_x2'] = df['end_x'].shift(periods=-1)
            df = df.drop(['end_x'], axis=1)
            df['start_y'] = df['POINT_Y']
            df['end_y'] = df.iloc[1:, :].loc[:, 'start_y']
            df['end_y2'] = df['end_y'].shift(periods=-1)
            df = df.drop(['end_y'], axis=1)

            ketinggiane_akhir = df["ketinggian"].iloc[-1]

            df2 = df.drop(df.index[len(df)-1])
            # df2['Tinggi Terbang'] = df2['ketinggian']+(entry_3)
            df2['Tinggi Terbang'] = df2['ketinggian']

            colomn_tabel = df2

            colomn_tabel["end_dsm"] = colomn_tabel.iloc[1:, :].loc[:, 'ketinggian']
            colomn_tabel["end_dsm2"] = colomn_tabel['end_dsm'].shift(periods=-1)
            colomn_tabel = colomn_tabel.drop(['end_dsm'], axis=1)
            colomn_tabel['selisih'] = (colomn_tabel['ketinggian'] - colomn_tabel['end_dsm2']).abs()
            colomn_tabel = colomn_tabel[["Id", "ketinggian", "selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel.columns = ["no_titik", "DSM", "Selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]


            ''''''
            fig, ax = plt.subplots()
            ax2 = ax.twinx()
            ax.plot(colomn_tabel['no_titik'], colomn_tabel['Tinggi Terbang'], 'ro', color='blue', markersize='2')
            ax.xaxis.set_major_locator(MultipleLocator(150))
            ax2.plot(colomn_tabel['no_titik'], colomn_tabel['Selisih'], color='grey',alpha=0.2)
            ax2.set_ylabel('Selisih Ketinggian', fontsize=15)
            ax2.set_ylim([0, 5])
            ax.set_ylabel('Ketinggian', fontsize=15)
            ax.set_xlabel('No titik', fontsize=15)
            ax.grid(True)
            ax.plot(colomn_tabel['no_titik'], colomn_tabel['DSM'], color='red', alpha=0.8)
            # plt.plot(colomn_tabel['no_titik'])
            ax.legend(loc= 2, fontsize="small")
            # ax2.legend(loc= "upper right")
            plt.gcf().set_size_inches((18,10))
            plt.title("Scatter Plot Titik DSM, Tinggi Terbang, ", fontsize=20)
            # plt.show()

            colomn_tabel.columns = [["Id", "ketinggian", "Selisih","Tinggi_Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel = colomn_tabel.drop(['Selisih'], axis=1)

            df = colomn_tabel

            ''' '''
            df['start_elev'] = df['ketinggian']
            df['end_elev'] = df.iloc[1:, :].loc[:, 'start_elev']
            df['end_elev2'] = df['end_elev'].shift(periods=-1)
            df = df.drop(['end_elev'], axis=1)
            df.at[len(df)-1, 'end_elev2'] = ketinggiane_akhir
            df2 = df
            # print(df2.tail(10))

            df2.to_csv(os.path.join(lokasi_output_folder,'final_dbf_siap_to_SCRIPTmasREY.csv')) 


            data_line_split = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_vertice_pohon.shp' in file:
                    data_line_split.append(os.path.join(lokasi_output_folder, file))

            data_csv = []
            for file in os.listdir(lokasi_output_folder):
                if file.endswith('.csv'):
                    data_csv.append(os.path.join(lokasi_output_folder, file))

            output_keluaran = os.path.join(lokasi_output_folder, "output_keluaran")
            os.mkdir(output_keluaran)


            # Process: Make XY Event Layer
            arcpy.MakeXYEventLayer_management(data_csv[0], "POINT_X", "POINT_Y", 'z_layer_xy_point_shp', "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "")

            # Process: Feature Class To Shapefile (multiple)
            arcpy.FeatureClassToShapefile_conversion("'z_layer_xy_point_shp'", output_keluaran)

            data_ptcsv = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv.append(os.path.join(output_keluaran, file))

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_ptcsv[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            arcpy.XYToLine_management(data_csv[0], os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "start_x", "start_y", "end_x2", "end_y2", "0", "Id", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision")

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_line_split[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")
            # Process: Add Attribute Index
            arcpy.AddIndex_management(os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            data_ptcsv_scan2 = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv_scan2.append(os.path.join(output_keluaran, file))


            arcpy.JoinField_management(data_ptcsv_scan2[0], "Id", data_ptcsv_scan2[1], "Id", "ketinggian;Tinggi_Ter;start_elev;end_elev2")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d"))

            arcpy.AddField_management("ln_ready_to_3d", "start_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.AddField_management("ln_ready_to_3d", "end_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("ln_ready_to_3d", "start_elv", "float(!start_elev!)", "PYTHON", "")
            arcpy.CalculateField_management("ln_ready_to_3d", "end_elv", "float(!end_elev2!)", "PYTHON", "")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d_fixx.shp"))

            arcpy.FeatureTo3DByAttribute_3d("ln_ready_to_3d_fixx", os.path.join(lokasi_output_folder,"3d_jalur_terbang.shp"), "start_elv", "end_elv")

            arcpy.management.CopyFeatures("3d_jalur_terbang", os.path.join(lokasi_output,"3d_jalur_terbang_fixxx"))

        def dsm_altitude ():
                
            lokasi_output_folder = os.path.join(lokasi_output, "lokasi_output")
            os.mkdir(lokasi_output_folder)

            data_dsm = []
            for file in os.listdir(lokasi_dsm_shp):
                if file.endswith('.tif'):
                    data_dsm.append(os.path.join(lokasi_dsm_shp, file))
            data_jalur_terbang = []
            for file in os.listdir(lokasi_dsm_shp):
                if file.endswith('.shp'):
                    data_jalur_terbang.append(os.path.join(lokasi_dsm_shp, file))


            arcpy.FeatureVerticesToPoints_management(data_jalur_terbang[0], os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), "ALL")

            arcpy.gp.ExtractValuesToPoints_sa(os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), data_dsm[0], os.path.join(lokasi_output_folder, 'pt_val_xy.shp'), "NONE", "VALUE_ONLY")

            arcpy.AddXY_management(os.path.join(lokasi_output_folder, 'pt_val_xy.shp'))

            arcpy.CalculateField_management(os.path.join(lokasi_output_folder, 'pt_val_xy.shp'), "Id", "autoIncrement()", "PYTHON", "rec=0 \\ndef autoIncrement(): \\n global rec \\n pStart = 1  \\n pInterval = 1 \\n if (rec == 0):  \\n  rec = pStart  \\n else:  \\n  rec += pInterval  \\n return rec")

            data_dbf_xyval = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_val_xy.dbf' in file:
                    data_dbf_xyval.append(os.path.join(lokasi_output_folder, file))

            path_dbf = Dbf5(data_dbf_xyval[0])
            df = path_dbf.to_dataframe()

            df['start_x'] = df['POINT_X']
            df['end_x'] = df.iloc[1:, :].loc[:, 'start_x']
            df['end_x2'] = df['end_x'].shift(periods=-1)
            df = df.drop(['end_x'], axis=1)
            df['start_y'] = df['POINT_Y']
            df['end_y'] = df.iloc[1:, :].loc[:, 'start_y']
            df['end_y2'] = df['end_y'].shift(periods=-1)
            df = df.drop(['end_y'], axis=1)

            #  rastervalue_akhir = (df["RASTERVALU"].iloc[-1])      ###awalnya ini
            rastervalue_akhir = (df["RASTERVALU"].iloc[-1])+(entry_3)

            df2 = df.drop(df.index[len(df)-1])
            df2['Tinggi Terbang'] = df2['RASTERVALU']+(entry_3)    #awalnya yang ini 
            # df2['Tinggi Terbang'] = df2['RASTERVALU']


            colomn_tabel = df2

            colomn_tabel["end_dsm"] = colomn_tabel.iloc[1:, :].loc[:, 'RASTERVALU']
            colomn_tabel["end_dsm2"] = colomn_tabel['end_dsm'].shift(periods=-1)
            colomn_tabel = colomn_tabel.drop(['end_dsm'], axis=1)
            colomn_tabel['selisih'] = (colomn_tabel['RASTERVALU'] - colomn_tabel['end_dsm2']).abs()
            colomn_tabel = colomn_tabel[["Id", "RASTERVALU", "selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel.columns = ["no_titik", "DSM", "Selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]

            # colomn_tabel.to_csv(os.path.join(lokasi_folder,'final_dbf_siap_to_SCRIPTmasREY_satu.csv'))
            ''''''

            colomn_tabel.columns = [["Id", "RASTERVALU", "Selisih","Tinggi_Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel = colomn_tabel.drop(['Selisih'], axis=1)

            df = colomn_tabel

            ''' '''
            # df['start_elev'] = df['RASTERVALU']   ###AWALNYA INI####
            df['start_elev'] = df['Tinggi_Terbang']
            df['end_elev'] = df.iloc[1:, :].loc[:, 'start_elev']
            df['end_elev2'] = df['end_elev'].shift(periods=-1)
            df = df.drop(['end_elev'], axis=1)
            df.at[len(df)-1, 'end_elev2'] = rastervalue_akhir
            df2 = df

            df2.to_csv(os.path.join(lokasi_output_folder,'final_dbf_siap_to_SCRIPTmasREY.csv')) 


            # TAHAP 2
            # TAHAP 2
            # Tahap 2


            data_line_split = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_val_xy.shp' in file:
                    data_line_split.append(os.path.join(lokasi_output_folder, file))

            data_csv = []
            for file in os.listdir(lokasi_output_folder):
                if file.endswith('.csv'):
                    data_csv.append(os.path.join(lokasi_output_folder, file))

            output_keluaran = os.path.join(lokasi_output_folder, "output_keluaran")
            os.mkdir(output_keluaran)


            # Process: Make XY Event Layer
            arcpy.MakeXYEventLayer_management(data_csv[0], "POINT_X", "POINT_Y", 'z_layer_xy_point_shp', "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "")

            # Process: Feature Class To Shapefile (multiple)
            arcpy.FeatureClassToShapefile_conversion("'z_layer_xy_point_shp'", output_keluaran)

            data_ptcsv = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv.append(os.path.join(output_keluaran, file))

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_ptcsv[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            arcpy.XYToLine_management(data_csv[0], os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "start_x", "start_y", "end_x2", "end_y2", "0", "Id", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision")

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_line_split[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")
            # Process: Add Attribute Index
            arcpy.AddIndex_management(os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            data_ptcsv_scan2 = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv_scan2.append(os.path.join(output_keluaran, file))


            arcpy.JoinField_management(data_ptcsv_scan2[0], "Id", data_ptcsv_scan2[1], "Id", "RASTERVALU;Tinggi_Ter;start_elev;end_elev2")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d"))

            arcpy.AddField_management("ln_ready_to_3d", "start_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.AddField_management("ln_ready_to_3d", "end_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("ln_ready_to_3d", "start_elv", "float(!start_elev!)", "PYTHON", "")
            arcpy.CalculateField_management("ln_ready_to_3d", "end_elv", "float(!end_elev2!)", "PYTHON", "")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d_fixx.shp"))

            arcpy.FeatureTo3DByAttribute_3d("ln_ready_to_3d_fixx", os.path.join(lokasi_output_folder,"3d_jalur_terbang.shp"), "start_elv", "end_elv")

            arcpy.management.CopyFeatures("3d_jalur_terbang", os.path.join(lokasi_output,"3d_jalur_terbang_fixxx"))

        def local_altitude ():
            
            lokasi_output_folder = os.path.join(lokasi_output, "lokasi_output")
            os.mkdir(lokasi_output_folder)

            data_jalur_terbang = []
            for file in os.listdir(lokasi_dsm_shp):
                if file.endswith('.shp'):
                    data_jalur_terbang.append(os.path.join(lokasi_dsm_shp, file))


            arcpy.FeatureVerticesToPoints_management(data_jalur_terbang[0], os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), "ALL")

            arcpy.AddXY_management(os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'))

            arcpy.CalculateField_management(os.path.join(lokasi_output_folder, 'pt_vertice_pohon.shp'), "Id", "autoIncrement()", "PYTHON", "rec=0 \\ndef autoIncrement(): \\n global rec \\n pStart = 1  \\n pInterval = 1 \\n if (rec == 0):  \\n  rec = pStart  \\n else:  \\n  rec += pInterval  \\n return rec")

            arcpy.AddField_management("pt_vertice_pohon", "ketinggian", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("pt_vertice_pohon", "ketinggian", "{}".format(sum_local_alt_height), "VB", "")


            data_dbf_xyval = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_vertice_pohon.dbf' in file:
                    data_dbf_xyval.append(os.path.join(lokasi_output_folder, file))

            path_dbf = Dbf5(data_dbf_xyval[0])
            df = path_dbf.to_dataframe()

            df['start_x'] = df['POINT_X']
            df['end_x'] = df.iloc[1:, :].loc[:, 'start_x']
            df['end_x2'] = df['end_x'].shift(periods=-1)
            df = df.drop(['end_x'], axis=1)
            df['start_y'] = df['POINT_Y']
            df['end_y'] = df.iloc[1:, :].loc[:, 'start_y']
            df['end_y2'] = df['end_y'].shift(periods=-1)
            df = df.drop(['end_y'], axis=1)

            ketinggiane_akhir = df["ketinggian"].iloc[-1]

            df2 = df.drop(df.index[len(df)-1])
            # df2['Tinggi Terbang'] = df2['ketinggian']+(entry_3)     #awalnya yang ini
            df2['Tinggi Terbang'] = df2['ketinggian']

            colomn_tabel = df2

            colomn_tabel["end_dsm"] = colomn_tabel.iloc[1:, :].loc[:, 'ketinggian']
            colomn_tabel["end_dsm2"] = colomn_tabel['end_dsm'].shift(periods=-1)
            colomn_tabel = colomn_tabel.drop(['end_dsm'], axis=1)
            colomn_tabel['selisih'] = (colomn_tabel['ketinggian'] - colomn_tabel['end_dsm2']).abs()
            colomn_tabel = colomn_tabel[["Id", "ketinggian", "selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel.columns = ["no_titik", "DSM", "Selisih", "Tinggi Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]

            ''''''
        
            colomn_tabel.columns = [["Id", "ketinggian", "Selisih","Tinggi_Terbang", "POINT_X", "POINT_Y", "start_x", "end_x2", "start_y", "end_y2"]]
            colomn_tabel = colomn_tabel.drop(['Selisih'], axis=1)
            df = colomn_tabel

            ''' '''
            df['start_elev'] = df['ketinggian']
            df['end_elev'] = df.iloc[1:, :].loc[:, 'start_elev']
            df['end_elev2'] = df['end_elev'].shift(periods=-1)
            df = df.drop(['end_elev'], axis=1)
            df.at[len(df)-1, 'end_elev2'] = ketinggiane_akhir
            df2 = df
            # print(df2.tail(10))

            df2.to_csv(os.path.join(lokasi_output_folder,'final_dbf_siap_to_SCRIPTmasREY.csv')) 

            data_line_split = []
            for file in os.listdir(lokasi_output_folder):
                if 'pt_vertice_pohon.shp' in file:
                    data_line_split.append(os.path.join(lokasi_output_folder, file))

            data_csv = []
            for file in os.listdir(lokasi_output_folder):
                if file.endswith('.csv'):
                    data_csv.append(os.path.join(lokasi_output_folder, file))

            output_keluaran = os.path.join(lokasi_output_folder, "output_keluaran")
            os.mkdir(output_keluaran)


            # Process: Make XY Event Layer
            arcpy.MakeXYEventLayer_management(data_csv[0], "POINT_X", "POINT_Y", 'z_layer_xy_point_shp', "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "")

            # Process: Feature Class To Shapefile (multiple)
            arcpy.FeatureClassToShapefile_conversion("'z_layer_xy_point_shp'", output_keluaran)

            data_ptcsv = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv.append(os.path.join(output_keluaran, file))

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_ptcsv[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            arcpy.XYToLine_management(data_csv[0], os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "start_x", "start_y", "end_x2", "end_y2", "0", "Id", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision")

            # Process: Add Attribute Index
            arcpy.AddIndex_management(data_line_split[0], "Id", "", "NON_UNIQUE", "NON_ASCENDING")
            # Process: Add Attribute Index
            arcpy.AddIndex_management(os.path.join(output_keluaran, "ln_ready_to_3d.shp"), "Id", "", "NON_UNIQUE", "NON_ASCENDING")

            data_ptcsv_scan2 = []
            for file in os.listdir(output_keluaran):
                if file.endswith('.shp'):
                    data_ptcsv_scan2.append(os.path.join(output_keluaran, file))


            arcpy.JoinField_management(data_ptcsv_scan2[0], "Id", data_ptcsv_scan2[1], "Id", "ketinggian;Tinggi_Ter;start_elev;end_elev2")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d"))

            arcpy.AddField_management("ln_ready_to_3d", "start_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.AddField_management("ln_ready_to_3d", "end_elv", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("ln_ready_to_3d", "start_elv", "float(!start_elev!)", "PYTHON", "")
            arcpy.CalculateField_management("ln_ready_to_3d", "end_elv", "float(!end_elev2!)", "PYTHON", "")

            arcpy.management.CopyFeatures("ln_ready_to_3d", os.path.join(lokasi_output_folder,"ln_ready_to_3d_fixx.shp"))

            arcpy.FeatureTo3DByAttribute_3d("ln_ready_to_3d_fixx", os.path.join(lokasi_output_folder,"3d_jalur_terbang.shp"), "start_elv", "end_elv")
            
            arcpy.management.CopyFeatures("3d_jalur_terbang", os.path.join(lokasi_output,"3d_jalur_terbang_fixxx"))    
            
        if output1 == "Flat Altitude":
            flat_altitude()
        elif output1 == "Adding DSM Altitude":
            dsm_altitude()
        elif output1 == "Adding Local Altitude":
            local_altitude()
autocorrect.process_all()