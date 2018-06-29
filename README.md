# 凭曲写谱 <font size = 2>Signal & System Assignment</font>
<p align = "right">自62 &nbsp;程笑天&nbsp;2016011408</p>
<p align = "center">
    <img src = "assets/score.jpeg">
</p> 

## 概述
本次大作业主要是利用FFT（快速傅里叶变换）对*.wav格式音频文件进行分段裁剪，分析其时频特性，并根据钢琴88音对应的特征频率，得到音频的简谱；
</br>

## 主要功能
* <b>导入音频文件，并得出其音乐谱（简谱），可导出至文件</b>
* 对于wav文件，可作出其时域强度图
* 可将长度一定的wav文件进行切割，产生时间长度较小的子wav文件,<i>一般取0.5秒或1秒</i>。
* 对于wav文件进行快速傅里叶变换，并作出其FFT频域图像
</br>

## 目录下文件
+ assets/ 目录下为背景图，可无视
+ Piano88/ 目录下为钢琴88音的音频文件，感兴趣的朋友也可以拿来做一做频谱分析
+ Fcsv_final.csv CSV文件，内部记录了音阶－特征频率对应表，频率序号为音阶在钢琴上从左数的位置
+ night.wav　WAV文件，《晚风》
+ Tigers.wav WAV文件，《两只老虎》
+ <b>CutWavFile.py 用于切割原始音频文件</b>
+ <b>FA_CMD.py 可输出简谱、波形图、频谱图，为主要代码文件</b>
+ <b>FA.ipynb 可用jupyter notebook 打开，可完成所有功能</b>
+ README.md 向导文件
+ requirements.txt 记录了运行程序前所需下载的包
</br>

## 安装
    $ git clone git@github.com:greatwallet/ScoreTextMaker.git
    $ cd ScoreTextMaker/
    $ sudo pip3 install -r requirements.txt
</br>

## 实现方式
*  [jupyter notebook](### jupyter notebook)
*  [py文件命令行参数形式](### py文件命令行参数形式)
</br>

### jupyter notebook
    $ jupyter notebook
</br>
点击FA.ipynb之后可进行运行代码，内含全部功能
</br>

### py文件命令行参数形式
以night.wav文件为demo试运行

    $ python3 FA_CMD.py night.wav -cs  #主功能:切割wav文件并获得简谱,并输出到文件
    $ python3 FA_CMD.py night.wav -c  #切割wav文件为若干子文件
    $ python3 FA_CMD.py night.wav -gt #获取原始wav文件波形图
    $ python3 FA_CMD.py night.wav -gf #切割原始wav文件,并获取随机一个子文件的频谱图
    
