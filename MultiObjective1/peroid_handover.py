from satellite_whether import Judge_Time_Size, Remaining_Time, Selected_Satellite_Parameter_Modify, Data_Normalization_Processing
from MyProblem_solution import Optimization_Model

NUMBER = 80
Max_Access_Time = 7000
Max_Storage_Size = 500
MAX_Qi_satellite = -9999999

fp3 = open("stk_data_processing.txt")
l3 = len(fp3.readlines())
fp3.close()

fp1 = open("final_selected_satellite.txt", "r")
for i in range(2):
    line1 = fp1.readline().rstrip()
    if i == 0:
        current_time = line1.split("          ")[1]
    if i == 1:
        satellite_parameter = line1.split("     ")[1]
fp1.close()
print("   切换时间          " + current_time)
print("卫星编号和相关参数     " + satellite_parameter)

f_handover_statistics = open("handover_satellite_statistics.txt", "w")
f_handover_statistics.writelines(current_time + "\n")
f_handover_statistics.writelines(satellite_parameter + "\n")

'''calculate total handover times during different call durations'''
#period_segment = [600, 1200, 1800, 2400, 3000, 3600, 4200, 4800, 5400, 6000]
period = 3600
total_period = period
handover = 0
list = []
while period >= 0:
        period = period - float(satellite_parameter.split("    ")[0].split(" ")[1])
        Selected_Satellite_Parameter_Modify(satellite_parameter)
        handover = handover + 1
        if period < 0:
            break
        fp3 = open("stk_data_processing.txt")
        fp4_1 = open("seleted_satellite_1.txt", "w")
        l4_1 = 0
        fp_1 = open("storage_time_initial1.txt")
        for j in range(0, l3):
            line3 = fp3.readline().rstrip()
            if line3 != '':
                if "Satellite" in line3:
                    Flag = line3.split('/')[0].split('e')[2]
                    flag = 0
                elif flag == 0:
                    start_time = line3.split("     ")[0]
                    end_time = line3.split("     ")[1]
                    if Judge_Time_Size(start_time, satellite_parameter.rstrip().split("    ")[2], end_time) == 1:
                        for k in range(NUMBER):
                            line = fp_1.readline().rstrip().split(" ")
                            if int(line[0]) == int(Flag):
                                line[1] = Remaining_Time(satellite_parameter.rstrip().split("    ")[2], end_time)
                                line[2] = Max_Access_Time - int(line[2])
                                line[3] = Max_Storage_Size - int(line[3])
                                fp4_1.writelines(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(
                                    line[3]) + "    " + start_time + "    " + end_time + "\n")
                                l4_1 = l4_1 + 1
                                break
                            else:
                                continue
                    else:
                        continue

        fp4_1.close()
        fp3.close()
        fp_1.close()

        MAX_Qi_satellite = -9999999

        fp1 = open("seleted_satellite_1.txt")
        for i in range(l4_1):            #comparison
            line2 = fp1.readline().rstrip()
            line1 = line2.split("    ")[0].split(" ")
            data1 = int(float(line1[1]))
            data2 = int(line1[2])
            data3 = int(line1[3])
            [data1, data2, data3] = Data_Normalization_Processing(data1, data2, data3)
            fpp = open("maxQi_parameter.txt", "w")
            fpp.writelines(str(data1) + ' ' + str(data2) + ' ' + str(data3))
            fpp.close()
            Qi_satellite = Optimization_Model()
            if Qi_satellite >= MAX_Qi_satellite:
                MAX_Qi_satellite = Qi_satellite
                satellite_four_parameters = line2
            else:
                continue
        fp1.close()
        print(satellite_four_parameters)
        list.append(satellite_four_parameters)
        satellite_parameter = satellite_four_parameters
print("相应周期：" + str(total_period))
print("切换次数：" + str(handover))

for i in range(len(list)):
    f_handover_statistics.writelines(list[i] + "\n")
f_handover_statistics.writelines("相应周期：" + str(total_period) + "\n")
f_handover_statistics.writelines("切换次数：" + str(handover))
f_handover_statistics.close()
