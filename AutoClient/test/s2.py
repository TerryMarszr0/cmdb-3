#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com


t = """
010lm-ahzy.kq.bdyzh.com-----ahzy.010lm.com
01ny-hezhong.kq.bdyzh.com-----hezhong.01ny.cn
123cha-ahzy.kq712.bdyzh.com-----ahzy.123cha.com
123cha-kqjk.kq712.bdyzh.com-----kqjk.123cha.com
51etong-ahzy.kq.bdyzh.com-----ahzy.51etong.com
chibi-ahzy.kq712.bdyzh.com-----ahzy.chibi.com.cn
cqnet110-ahzy.kq712.bdyzh.com-----ahzy.cqnet110.gov.cn
cqwb-ahzy.kq712.bdyzh.com-----ahzy.cqwb.com.cn
hynews-knwy.kq.bdyzh.com-----knwy.hynews.net
jxgztv-ahzy.kq76.bdyzh.com-----ahzy.jxgztv.com
lenw-yst.kq712.bdyzh.com-----yst.lenw.cn
ntxx-baidianfeng.kq712.bdyzh.com-----baidianfeng.ntxx.net
nxing-yst.kq712.bdyzh.com-----health.nxing.cn
okinfo-kadt.kq.bdyzh.com-----kadt.okinfo.org
pcbaby-ahzy.kq712.bdyzh.com-----ahzy.pcbaby.cn
qndb-ahzy.kq712.bdyzh.com-----ahzy.qndb.net
qydjw-yst.kq.bdyzh.com-----yst.qydjw.gov.cn
tianqi4-yst.kq.bdyzh.com-----yst.tianqi4.com
zjrxz-myft.kq.bdyzh.com-----myft.zjrxz.com
zkxww-ahzy.kq.bdyzh.com-----ahzy.zkxww.com
zznews-yst.kq712.bdyzh.com-----yst.zznews.cn
"""

for i in t.split('\n'):
    if i:
        print("%s    %s" % ("60.169.77.238", i.split("--")[0]))