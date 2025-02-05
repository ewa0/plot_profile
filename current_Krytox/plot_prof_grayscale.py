import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

i = 0
dim05 = [916, 20, 59, 600]
dim1 = [880, 20, 71, 775]
dim2 = [868, 20, 95, 775]
dim3 = [856, 20, 119, 775]

# folder_name = "test"  # change here
folder_name = "pore_diam_05um"  # change here
dimensions = dim05  # change here

# folder_name = "pore_diam_05um"
# folder_name = "pore_diam_1um"
# folder_name = "pore_diam_2um"
# folder_name = "pore_diam_3um"


df_master = pd.DataFrame(columns=["time [s]", "krytox", "dodecane",
                                  "cumul_none", "normalized_krytox"])
directory = "/home/ewa/Documents/plot_profile/current_Krytox/" + folder_name + "/"
file_list = os.listdir(directory)
file_list.sort()

for filename in file_list:
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        i += 1
        filepath = directory + filename
        img = Image.open(filepath)
        # img.show()

        # crop
        x = dimensions[0]
        y = dimensions[1]
        width = dimensions[2]
        height = dimensions[3]
        cropped_image = img.crop((x, y, x + width, y + height))
        # cropped_image.show()

        # plot profile all
        all_values = np.asarray(cropped_image.getdata())
        values = all_values[:, 0]

        # attributing grayscale value to a phase
        cumul_dodecane = len(list((filter(lambda dod: dod <= 40, values))))  # black
        cumul_krytox = len(list((filter(lambda kryt: 41 <= kryt <= 247, values))))  # gray
        cumul_none = len(list((filter(lambda none: 248 <= none, values))))  # white
        # print(filename)

        # cropping pore only
        cropped_pore = cropped_image.crop((0, 358, width, 358 + 238))
        # cropped_pore.show()

        # plot profile pore
        pore_values = np.asarray(cropped_pore.getdata())
        values_pore = pore_values[:, 0]

        # attributing grayscale value to a phase
        pore_dodecane = len(list((filter(lambda dod: dod <= 40, values_pore))))  # black
        pore_krytox = len(list((filter(lambda kryt: 41 <= kryt <= 247, values_pore))))  # gray
        pore_none = len(list((filter(lambda none: 248 <= none, values_pore))))  # white

        # cropping top reservoir
        cropped_exit_reservoir = cropped_image.crop((0, 0, width, 357))
        # cropped_exit_reservoir.show()

        # plot profile exit reservoir
        res_values = np.asarray(cropped_exit_reservoir.getdata())
        values_res = res_values[:, 0]

        # attributing grayscale value to a phase
        exit_res_dodecane = len(list((filter(lambda dod: dod <= 40, values_res))))  # black
        exit_res_krytox = len(list((filter(lambda kryt: 41 <= kryt <= 247, values_res))))  # gray

        # appending data to dataframe
        if not cumul_krytox == 0:
            new_row = pd.DataFrame(
                {"time [s]": [i * 1e-4], "cumul Krytox": [cumul_krytox], "cumul dodecane": [cumul_dodecane],
                 "cumul_none": [cumul_none], "normalized_krytox": [cumul_krytox / (cumul_krytox + cumul_dodecane)],
                 "pore dodecane": [pore_dodecane], "pore Krytox": [pore_krytox],
                 "exit reservoir Krytox": [exit_res_krytox], "exit reservoir dodecane": [exit_res_dodecane],
                 "inlet reservoir Krytox": [cumul_krytox - pore_krytox - exit_res_krytox],
                 "inlet reservoir dodecane": [cumul_dodecane - pore_dodecane - pore_krytox]},
                index=[i])
            df_master = pd.concat([df_master, new_row])

        else:
            new_row = pd.DataFrame(
                {"time [s]": [i * 1e-4], "cumul Krytox": [cumul_krytox], "cumul dodecane": [cumul_dodecane],
                 "cumul_none": [cumul_none], "normalized_krytox": [0], "pore dodecane": [pore_dodecane],
                 "pore Krytox": [pore_krytox], "exit reservoir Krytox": [exit_res_krytox],
                 "exit reservoir dodecane": [exit_res_dodecane],
                 "inlet reservoir Krytox": [cumul_krytox - pore_krytox - exit_res_krytox],
                 "inlet reservoir dodecane": [cumul_dodecane - pore_dodecane - pore_krytox]}, index=[i])
            df_master = pd.concat([df_master, new_row])

        # plot this funky stuff
        plt.plot(df_master["time [s]"], df_master["normalized_krytox"])
        plt.xlabel("time [s]")
        plt.ylabel("normalized_krytox [-]")

# save to a file
dir_name = os.path.join(os.getcwd())
df_master.to_csv(path_or_buf=directory + folder_name + "_pore_res.csv", sep=';')
plt.show()
plt.savefig(folder_name + "_plot.png")
