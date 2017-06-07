#!/usr/bin/env python
#coding:utf-8

import sys
import math

'''
mc2ll and ll2mc
https://loftor.com/archives/bd09mc-bd09ll.html
compute the distance using lng and lat
http://bbs.lbsyun.baidu.com/forum.php?mod=viewthread&tid=76&highlight=%E7%BB%8F%E7%BA%AC%E5%BA%A6%2B%E8%B7%9D%E7%A6%BB
'''

EARTH_RADIUS = 6370996.81;

MCBAND = [12890594.86, 8362377.87, 5591021.00, 3481989.83, 1678043.12, 0.00]
LLBAND = [75.00, 60.00, 45.00, 30.00, 15.00, 0.00]
MC2LL = [
    [1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547, 91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2], 
    [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846,
    -1.85204757529826, -59.36935905485877, 47.40033549296737, -16.50741931063887,
    2.28786674699375, 10260144.86], 
    [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871, -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37], 
    [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277, -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06], 
    [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511, -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4], 
    [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994, -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5]
]
LL2MC = [
    [-0.0015702102444, 111320.7020616939, 1704480524535203.00, -10338987376042340.00,
    26112667856603880.00, -35149669176653700.00, 26595700718403920.00, -10725012454188240.00,
                      1800819912950474.00, 82.50], 
    [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316,
    10774905663.51142, -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5], 
    [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455, -115964993.2797253, 97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5], 
    [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013, -1221952.21711287, 1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5], 
    [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378, 54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5], 
    [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093, 2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]
]

def converter(x, y, cE):
    xTemp = cE[0] + cE[1] * math.fabs(x);
    cC = math.fabs(y) / cE[9];
    yTemp = cE[2] + \
        cE[3] * cC + \
        cE[4] * cC * cC + \
        cE[5] * cC * cC * cC + \
        cE[6] * cC * cC * cC * cC + \
        cE[7] * cC * cC * cC * cC * cC + \
        cE[8] * cC * cC * cC * cC * cC * cC;
    xTemp *= -1 if x < 0.0 else 1;
    yTemp *= -1 if y < 0.0 else 1;
    return xTemp, yTemp;

def get_loop(lng, minv, maxv):
    while lng > maxv:
        lng -= maxv - minv;
    while lng < minv:
        lng += maxv - minv;
    return lng;

def get_range(lat, minv, maxv):
    if minv != None:
        lat = max(lat, minv);
    if maxv != None:
        lat = min(lat, maxv);
    return lat;

def convert_mc2ll(x, y):
    cF = [];
    x = math.fabs(x);
    y = math.fabs(y);

    for cE in range(0, len(MCBAND)):
        if y >= MCBAND[cE]:
            cF = MC2LL[cE];
            break;
    return converter(x, y, cF);

def convert_ll2mc(lng, lat):
    cE = [];
    lng = get_loop(lng, -180, 180);
    lat = get_range(lat, -74, 74);
    for i in range(0, len(LLBAND)):
        if lat >= LLBAND[i]:
            cE = LL2MC[i];
            break;
    if len(cE) != 0:
        for i in reversed(range(len(LLBAND))):
            if lat <= -LLBAND[i]:
                cE = LL2MC[i];
                break;
    return converter(lng,lat, cE);

def ll2mc(lng, lat):
    '''经纬度转墨卡托'''
    if lng <= 0 or lat <= 0 or lng >= 180 or lat >= 90:
        return 0, 0
    else:
        return convert_ll2mc(lng, lat)

def mc2ll(mx, my):
    '''经纬度转墨卡托'''
    if mx <= 0 or my <= 0:
        return 0, 0
    else:
        return convert_mc2ll(mx, my)


def calc_ll_dist(lng1, lat1, lng2, lat2):
    ''' distance(m) of two location by longtitude and latitude'''
    radLat1 = math.radians(lat1);
    radLat2 = math.radians(lat2);
    radLng1 = math.radians(lng1);
    radLng2 = math.radians(lng2);
    deltaLat = radLat1 - radLat2;
    deltaLng = radLng1 - radLng2;
    distance = 2 * math.asin(math.sqrt(math.pow(
                    math.sin(deltaLat / 2), 2)
                    + math.cos(radLat1)
                    * math.cos(radLat2)
                    * math.pow(math.sin(deltaLng / 2), 2)));
    distance = distance * EARTH_RADIUS;
    return distance;

def calc_mc_dist(mc_x1, mc_y1, mc_x2, mc_y2):
    ''' distance(m) of two location by mecator coor'''
    lng1, lat1 = convert_mc2ll(mc_x1, mc_y1);
    lng2, lat2 = convert_mc2ll(mc_x2, mc_y2);
    return calc_ll_dist(lng1, lat1, lng2, lat2);

if __name__ == "__main__":
    
    lng, lat = 113.38998, 23.105773
    print lng, lat
    
    mc_x, mc_y = convert_ll2mc(lng, lat);
    print mc_x, mc_y
    
    lng, lat = convert_mc2ll(mc_x, mc_y);
    print lng, lat

    lng1, lat1 = 113.38998, 23.105773
    mc_x1, mc_y1 = convert_ll2mc(lng1, lat1)
    print "dong dan: ", lng1, lat1, mc_x1, mc_y1
    lng2, lat2 = 116.4423, 39.914555
    mc_x2, mc_y2 = convert_ll2mc(lng2, lat2)
    print "jianguomen: ",lng2, lat2, mc_x2, mc_y2
    dist1 = calc_ll_dist(lng1, lat1, lng2, lat2) # 1521m
    dist2 = calc_mc_dist(mc_x1, mc_y1, mc_x2, mc_y2) # 1521m
    print "distance: ", dist1, dist2

