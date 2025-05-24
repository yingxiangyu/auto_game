向僵尸开炮自动程序

[mapiing.py](mapiing.py) 是基于屏幕匹配方案，但是分辨率变动时不好适配

[play_ocr.py](play_ocr.py) [play_shilian.py](play_shilian.py) 是基于ocr的版本，可以兼容不同分辨率

使用的umi-ocr，需要自己搭建，替换utils.py ocr函数的服务器地址

适配的windows下微信小程序版本，支持多开

推荐使用[play_shilian.py](play_shilian.py)版本，适配场景更多