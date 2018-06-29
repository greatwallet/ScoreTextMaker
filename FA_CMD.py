#encoding=utf-8
import sys
import wave
import pyaudio
import pylab
import numpy as np
import os
import csv
import random
import CutWavFile


threshold = 0.9 # 标定强度阈值（0~1之间）
key_file = "./Piano88/German Concert D "    # 钢琴88音所在目录
FDicCSV = "./Fcsv_final.csv"    # 钢琴88音对应csv文件
# 全部以简谱表示X(Y),X为音调，Y为有多少个降key
KeyList = [
    "6(-4)","6(-4)#","7(-4)",    # 大字一组
            "1(-3)","1(-3)#","2(-3)","2(-3)#","3(-3)","4(-3)","4(-3)#",
            "5(-3)","5(-3)#","6(-3)","6(-3)#","7(-3)" , # 大字二组  
            "1(-2)","1(-2)#","2(-2)","2(-2)#","3(-2)","4(-2)","4(-2)#",
            "5(-2)","5(-2)#","6(-2)","6(-2)#","7(-2)" , # 大字组 
            "1(-1)","1(-1)#","2(-1)","2(-1)#","3(-1)","4(-1)","4(-1)#",
            "5(-1)","5(-1)#","6(-1)","6(-1)#","7(-1)" , # 小字组 
            "1","1#","2","2#","3","4","4#",
            "5","5#","6","6#","7" , # 小字一组，中央调
            "1(+1)","1(+1)#","2(+1)","2(+1)#","3(+1)","4(+1)","4(+1)#",
            "5(+1)","5(+1)#","6(+1)","6(+1)#","7(+1)" , # 小字二组 
            "1(+2)","1(+2)#","2(+2)","2(+2)#","3(+2)","4(+2)","4(+2)#",
            "5(+2)","5(+2)#","6(+2)","6(+2)#","7(+2)" , # 小字三组 
            "1(+3)","1(+3)#","2(+3)","2(+3)#","3(+3)","4(+3)","4(+3)#",
            "5(+3)","5(+3)#","6(+3)","6(+3)#","7(+3)" , # 小字四组 
            "1(+4)" #小字五组
            ]
# 产生波形数据
def GenerateWavData(WavFile):
    # 打开WAV文档，文件路径根据需要做修改
    with wave.open(WavFile,'rb') as wf:
        # 读取WAV文档的参数
        nframes = wf.getnframes()
        framerate = wf.getframerate()
        width = wf.getsampwidth()
        channels = wf.getnchannels()
        # 读取完整的帧数据到str_data中，这是一个string类型的数据
        str_data = wf.readframes(nframes)
    # 将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    # 将wave_data数组改为2列，行数自动匹配。在修改shape的属性时，需使得数组的总长度不变。
    wave_data.shape = -1,2
    # 将数组转置
    wave_data = wave_data.T
    return wave_data,nframes,framerate,width,channels

# 产生波形图
def GenerateWavGraph(WavFile):
    wave_data,nframes,framerate,width,channels = GenerateWavData(WavFile)
    # time 也是一个数组，与wave_data[0]或wave_data[1]配对形成系列点坐标
    time = np.arange(0,nframes)*(1.0/framerate)
    # #绘制波形图
    pylab.plot(time, wave_data[0])
    pylab.subplot(212)
    pylab.plot(time, wave_data[1], c="g")
    pylab.xlabel("time (seconds)")
    pylab.show()

# 进行0~1之间正则化，线性变化
def MaxMinNormalization(x,Max,Min):
	x = (x - Min) / (Max - Min)
	return x
# 进行数组归一化
def MMNormalization(original_array):
    abs_array = abs(original_array)
    max = np.max(abs_array)
    min = np.min(abs_array)
    if max != min:
        c = MaxMinNormalization(abs_array,max,min)
    else:
        c = np.zeros(original_array.shape)
    return c

# 进行秩相近的元素，留下它们的最大值
def Simplify(f,a,distance_index):
    current = 0
    i = 0
    while i < f.size:
        if 0 < abs(f[i]-f[current]) <= distance_index:
            if(a[i]>a[current]):
                a = np.delete(a,current,axis = 0)
                f = np.delete(f,current,axis = 0)
                current = i - 1
            else:
                a = np.delete(a,i,axis = 0)
                f = np.delete(f,i,axis = 0)
            i = i - 1
        elif abs(f[i]-f[current]) > distance_index:
            current = i
        i = i+1
    return f,a
# 寻找谱线较大的值，返回较大值及相应的秩
def FindFrequency(x):
    f_lst = []
    a_lst = []
    for i in range(int(x.shape[0]/2)):
        if x[i] > threshold:
            f_lst.append(i)
            a_lst.append(x[i])
    f_arr = np.array(f_lst)
    a_arr = np.array(a_lst)
    f_arr,a_arr = Simplify(f_arr,a_arr,distance_index = 5)
    return f_arr,a_arr
# 列出所有音阶的特征频率
def ListFrequency():
    key_file = "./Piano88/German Concert D "
    with open("./key2frequency.txt",'w') as f:
            numlst1 = [str(n) for n in range(21,100)]
            numlst2 = [str(n) for n in range(100,109)]
            for i in range(len(numlst1)):
                key_wav1 = key_file + "0" + numlst1[i] + " 083.wav"
                print(key_wav1)
                wave_data,nframes,framerate,width,channels = GenerateWavData(key_wav1)
                # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
                N = framerate
                start = 0 #开始采样位置
                wave_data2=wave_data[0][start:start+N]
                original_array=np.fft.fft(wave_data2)*2/N
                # 进行正则化，将赋值转变到0~1之间
                c = MMNormalization(original_array)
                f_arr,a_arr = FindFrequency(c)
                print(numlst1[i]," ",f_arr,file = f)
            for i in range(len(numlst2)):
                key_wav2 = key_file + numlst2[i] + " 083.wav"
                wave_data,nframes,framerate,width,channels = GenerateWavData(key_wav2)
                # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
                N = framerate
                start = 0 #开始采样位置
                wave_data2=wave_data[0][start:start+N]
                original_array=np.fft.fft(wave_data2)*2/N
                # 进行正则化，将赋值转变到0~1之间
                c = MMNormalization(original_array)
                f_arr,a_arr = FindFrequency(c)
                print(numlst2[i]," ",f_arr,file = f)
# 输出为CSV文件
def outCSV():
    key_file = "./Piano88/German Concert D "
    numlst1 = [str(n) for n in range(21,100)]
    numlst2 = [str(n) for n in range(100,109)]
    csvfile = open("./Fcsv.csv",'w')
    writer = csv.writer(csvfile)
    for i in range(len(numlst1)):
        key_wav1 = key_file + "0" + numlst1[i] + " 083.wav"
        print(key_wav1)
        wave_data,nframes,framerate,width,channels = GenerateWavData(key_wav1)
        # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
        N = framerate
        start = 0 #开始采样位置
        wave_data2=wave_data[0][start:start+N]
        original_array=np.fft.fft(wave_data2)*2/N
        # 进行正则化，将赋值转变到0~1之间
        c = MMNormalization(original_array)
        f_arr1,a_arr = FindFrequency(c)
        writer.writerow(f_arr1)
    for i in range(len(numlst2)):
        key_wav2 = key_file + numlst2[i] + " 083.wav"
        print(key_wav2)
        wave_data,nframes,framerate,width,channels = GenerateWavData(key_wav2)
        # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
        N = framerate
        start = 0 #开始采样位置
        wave_data2=wave_data[0][start:start+N]
        original_array=np.fft.fft(wave_data2)*2/N
        # 进行正则化，将赋值转变到0~1之间
        c = MMNormalization(original_array)
        f_arr2,a_arr = FindFrequency(c)
        writer.writerow(f_arr2)
    csvfile.close()

# 绘制频谱图
def GenerateFGraph(WavFile,d = -1):
    wave_data,nframes,framerate,width,channels = GenerateWavData(WavFile)
    # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
    N = framerate
    start = 0 #开始采样位置
    df = framerate/(N-1) # 分辨率
    freq = [df*n for n in range(0,N)] #N个元素
    wave_data2=wave_data[0][start:start+N]
    original_array=np.fft.fft(wave_data2)*2/N
    # 进行正则化，将赋值转变到0~1之间
    c = MMNormalization(original_array)
    #常规显示采样频率一半的频谱
    if d <= 0:
        d = int(len(c)/2)
    pylab.plot(freq[:d-1],abs(c[:d-1]),'r')
    pylab.show()

# 导入音阶表
def ImportFDic(FDicCSV):
    FDic = np.loadtxt(FDicCSV,delimiter=",")
    return FDic

# 二分查找，返回失败的位置（秩最大者）
def bin_search(data_set,val):
    #low 和high代表下标 最小下标，最大下标
    low = 0
    high = len(data_set)-1
    while low < high:# 只有当low小于High的时候证明中间有数
        mid = int((low+high) / 2 )
        if(val < data_set[mid]):
            high = mid
        else:
            low = mid + 1
    low = low - 1
    return low 

# 对音阶进行分类
def Classify(f,FDic):
    f_indexs = []
    for i in range(len(f)):
        index = bin_search(FDic,f[i])
        # 若音阶最低
        if index == -1:
            index = 0
        # 若音阶最高
        elif index == len(f)-1:
            pass
        else:
            gap = FDic[index + 1] - FDic[index]
            # 检查离目标频率最近的音阶
            if (f[i]-FDic[index]) > (gap/2):
                index = index + 1
        f_indexs.append(index)
    f_indexs_arr = np.array(f_indexs)
    return f_indexs_arr


ext = ".wav"
# 主函数
if __name__ == '__main__':
    print("自62 程笑天  2016011408  信号与系统大作业(凭曲写谱)")
    print("")
    print("用法：python FA_CMD.py [wav文件] [参数]")
    print("参数：")
    print("-cs\t\t","切割文件并获取简谱，输出到文件")
    print("-c\t\t","切割文件")
    print("-gt\t\t","获取原始音乐波形图")
    print("-gf\t\t","获取随机一个子文件的频谱图")
    print("")
    print("----------------------分割线是这么用的吧---------------------------")
    print("")
    if len(sys.argv) < 3:
        print("参数错误，请重新输入")
        exit(0)

    # 导入文件
    WavFile = sys.argv[1]
    [filename, ext] = os.path.splitext(WavFile)
    filedir = os.path.join('./',filename) + "_segmentation/"

        
    if sys.argv[2] == "-c":
        print("切割原始音频%s"%WavFile)
        WavNum = CutWavFile.CutFile(WavFile)
        print("共有%d个子文件"%WavNum)
        print("子文件目录：./",filename + "_segmentation/")
    elif sys.argv[2] == "-cs":
        print("切割原始音频%s"%WavFile)
        WavNum = CutWavFile.CutFile(WavFile)
        print("共有%d个子文件"%WavNum)
        print("子文件目录：./",filename + "_segmentation/")
        # 导入音阶
        FDic = ImportFDic(FDicCSV)
        num = [str(n) for n in range(0,WavNum)]
        print(filename,"简谱如下:")
        with open(filename + "ScoreText.txt",'w') as f:
            for i in range(len(num)):
                WavFile = filedir + filename + "_" + num[i] + ext
                wave_data,nframes,framerate,width,channels = GenerateWavData(WavFile)
                # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
                N = framerate
                start = 0 #开始采样位置
                wave_data2=wave_data[0][start:start+N]
                original_array=np.fft.fft(wave_data2)*2/N
                # 进行正则化，将赋值转变到0~1之间
                c = MMNormalization(original_array)
                f_arr,a_arr = FindFrequency(c)
                f_index_arr = Classify(f_arr,FDic)
                # 翻译为简谱
                print("{",end = " ")
                print("{",end = " ",file = f)
                for j in range(len(f_index_arr)):
                    print(KeyList[f_index_arr[j]],end = " ",file = f)
                    print(KeyList[f_index_arr[j]],end = " ")
                print("}",end = " ",file = f)
                if (i+1) % 4 == 0:
                    print("",file = f)
                    print("")
        print("\n已输出将简谱输出至",filename + "ScoreText.txt")
    elif sys.argv[2] == "-gt":
        GenerateWavGraph(WavFile)
    elif sys.argv[2] == "-gf":
        print("切割原始音频%s"%WavFile)
        WavNum = CutWavFile.CutFile(WavFile)
        print("共有%d个子文件"%WavNum)
        print("子文件目录：./",filename + "_segmentation/")
        print("随机选取一个子文件，展示其波形图、频谱图")
        n = random.randint(0,WavNum)
        TestWavFile = filedir + filename + "_" + str(n) + ext
        print("%s 号频谱图如下　"%str(n))
        GenerateFGraph(TestWavFile,d = 3000)