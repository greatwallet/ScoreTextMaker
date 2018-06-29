#encoding=utf-8
import os
import wave
import numpy as np
import pylab as plt

CutTimeDef = 500 # 以500ms截断文件
CutFrameNum =0

def CutFile(wavFileName):
    [filename, ext] = os.path.splitext(wavFileName) 
    print("CutFile File Name is ",filename)
    filedir = os.path.join('./',filename) + "_segmentation/"
    print("The Cuts are stored in %s" %filedir)
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
    f = wave.open(wavFileName, "rb")
    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
    # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    CutFrameNum = framerate * CutTimeDef / 1000
    print("CutFrameNum=%d" % (CutFrameNum))

    print("nchannels=%d" % (nchannels))
    print("sampwidth=%d" % (sampwidth))
    print("framerate=%d" % (framerate))
    print("nframes=%d" % (nframes))
    str_data = f.readframes(nframes)
    f.close()  # 将波形数据转换成数组
    # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    temp_data = wave_data.T
    StepNum = int(CutFrameNum)
    StepTotalNum = 0
    stemp = 0
    print("开始切割原始音频")
    while StepTotalNum < nframes:
        FileName = filedir + filename + "_" +str(stemp) + ext
        temp_dataTemp = temp_data[StepNum * (stemp):StepNum * (stemp + 1)]
        stemp = stemp + 1
        StepTotalNum = stemp * StepNum
        temp_dataTemp.shape = 1, -1
        temp_dataTemp = temp_dataTemp.astype(np.short)  # 打开WAV文档
        f = wave.open(FileName, "wb")  #
        # 配置声道数、量化位数和取样频率
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        # 将wav_data转换为二进制数据写入文件
        f.writeframes(temp_dataTemp.tostring())
        f.close()
    return stemp
