import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

i = 0
dim05 = [916, 20, 39, 600]
dim1 = [880, 20, 71, 600]
dim2 = [868, 20, 95, 600]
dim3 = [856, 20, 119, 600]

# folder_name = "test"  # change here
folder_name = "pore_diam_3um"  # change here
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

        # plot profile
        all_values = np.asarray(cropped_image.getdata())
        values = all_values[:, 0]

        # attributing grayscale value to a phase
        cumul_dodecane = len(list((filter(lambda dod: dod <= 40, values))))  # black
        cumul_krytox = len(list((filter(lambda kryt: 41 <= kryt <= 247, values))))  # gray
        cumul_none = len(list((filter(lambda none: 248 <= none, values))))  # white
        # print(filename)

        # appending data to dataframe
        if not cumul_krytox == 0:
            new_row = pd.DataFrame(
                {"time [s]": [i * 1e-4], "krytox": [cumul_krytox], "dodecane": [cumul_dodecane],
                 "cumul_none": [cumul_none], "normalized_krytox": [cumul_krytox / (cumul_krytox + cumul_dodecane)]},
                index=[i])
            df_master = pd.concat([df_master, new_row])

        else:
            new_row = pd.DataFrame(
                {"time [s]": [i * 1e-4], "krytox": [cumul_krytox], "dodecane": [cumul_dodecane],
                 "cumul_none": [cumul_none], "normalized_krytox": [0]}, index=[i])
            df_master = pd.concat([df_master, new_row])

        # plot this funky stuff
        plt.plot(df_master["time [s]"], df_master["normalized_krytox"])
        plt.xlabel("time [s]")
        plt.ylabel("normalized_krytox [-]")

# save to a file
dir_name = os.path.join(os.getcwd())
df_master.to_csv(path_or_buf=directory + folder_name + ".csv", sep=';')
plt.show()
plt.savefig(folder_name + "_plot.png")
