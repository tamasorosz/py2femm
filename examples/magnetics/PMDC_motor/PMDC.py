import os
import math
from math import sin,cos,asin,acos,pi
import femm
from src.geometry import Node, Line
from src.executor import Executor


femm.openfemm(0)
femm.opendocument("blank.fem")

Ro=20
Ri=10
ag_s=0.2
ag_r=0.2
ns=24
np=8
r2=8
r3=9
n_req_slots=12
def draw_stator(Ro, Ri, w1, w2, w3, w4, h1, h2, h3, h4, s3, ns, n_req_slots, ag_s):
    #itt most nem egészen vagyok benne biztos, hogy az argumentumokból nem hiányzik 1-1 mínusz, de elvileg jó
    p0 = Node(0,0)
    p1 = Node(-w1 / 2, Ri * float(math.cos(math.asin(w1 / 2 / Ri))))
    p2 = Node(-w1 / 2, (Ri + h1) * float(math.cos(math.asin(w1 / 2 / (Ri + h1)))))
    p3 = Node(-w2 / 2, (Ri + h1 + h2) * float(math.cos(math.asin(w2 / 2 / (Ri + h1 + h2)))))
    p4 = Node(-w3 / 2, (Ri + h1 + h2 + h3) * float(math.cos(math.asin(w3 / 2 / (Ri + h1 + h2 + h3)))))
    p6 = Node(-w4 / 2, (Ri + h1 + h2 + h3 + h4) * float(math.cos(math.asin(w4 / 2 / (Ri + h1 + h2 + h3 + h4)))))
    p5 = Node((p3.x-p4.x)*(p6.y-p3.y)/(p3.y-p4.y)+p3.x,p6.y)
    p7 = Node(w4 / 2, (Ri + h1 + h2 + h3 + h4) * float(math.cos(math.asin(w4 / 2 / (Ri + h1 + h2 + h3 + h4)))))
    p9 = Node(w3 / 2, (Ri + h1 + h2 + h3) * float(math.cos(math.asin(w3 / 2 / (Ri + h1 + h2 + h3)))))

    p10 = Node(w2 / 2, (Ri + h1 + h2) * float(math.cos(math.asin(w2 / 2 / (Ri + h1 + h2)))))
    p11 = Node(w1 / 2, (Ri + h1) * float(math.cos(math.asin(w1 / 2 / (Ri + h1)))))
    p12 = Node(w1 / 2, Ri * float(math.cos(math.asin(w1 / 2 / Ri))))
    p8 = Node((p9.x-p10.x)*(p6.y-p9.y)/(p9.y-p10.y)+p9.x,p6.y)

    femm.mi_drawline(p1.x, p1.y, p2.x, p2.y) # l1
    femm.mi_drawline(p2.x, p2.y, p3.x, p3.y) # l2
    femm.mi_drawline(p3.x, p3.y, p4.x, p4.y) # l3
    femm.mi_drawline(p4.x, p4.y, p5.x, p5.y) # l4
    femm.mi_drawline(p5.x, p5.y, p6.x, p6.y) # l5
    femm.mi_drawline(p6.x, p6.y, p7.x, p7.y) # l6
    femm.mi_drawline(p7.x, p7.y, p8.x, p8.y) # l7
    femm.mi_drawline(p8.x, p8.y, p9.x, p9.y) # l8
    femm.mi_drawline(p9.x, p9.y, p10.x, p10.y) # l9
    femm.mi_drawline(p10.x, p10.y, p11.x, p11.y) # l10
    femm.mi_drawline(p11.x, p11.y, p12.x, p12.y) # l11
    #femm.mi_drawline(p12.x, p12.y, p1.x, p1.y) # l12
    femm.mi_addnode(p0.x, p0.y)

    femm.mi_selectsegment(p1.x, p1.y+(p2.y-p1.y)/2) # p1-p2 -?
    femm.mi_selectsegment(p2.x+(p3.x - p2.x)/2, p2.y+(p3.y - p2.y)/2) # p2-p3
    femm.mi_selectsegment(p3.x+(p4.x - p3.x)/2, p3.y+(p4.y - p3.y)/2)  # p3-p4
    femm.mi_selectsegment(0, Ri + h1 + h2 + h3 + h4)  # p6-p7
    femm.mi_selectsegment(p10.x+(p9.x - p10.x)/2, p10.y+(p9.y - p10.y)/2)  # p9-p10
    femm.mi_selectsegment(p11.x+(p10.x - p11.x)/2, p11.y+(p10.y - p11.y)/2)  # p10-p11
    femm.mi_selectsegment(p12.x, p12.y+(p12.y - p11.y)/2)  # p11-p12
    #femm.mi_selectsegment(0, p1.y)  # p12-p1
    femm.mi_selectsegment(p4.x+(p5.x-p4.x)/2, p4.y+(p5.y-p4.y)/2)  # p4-p5
    femm.mi_selectsegment(p6.x+(p5.x-p6.x)/2, p6.y)  # p5-p6
    femm.mi_selectsegment(p9.x + (p8.x - p9.x) / 2, p9.y + (p8.y - p9.y) / 2)  # p8-p9
    femm.mi_selectsegment(p7.x + (p8.x - p7.x) / 2, p7.y)  # p7-p8
    femm.mi_copyrotate2(0, 0, -360 / ns, (n_req_slots-1),1)

    r_aux=math.sqrt(p5.x*p5.x+p5.y*p5.y)
    i=0
    alpha1 = math.acos(p5.x/r_aux)
    alpha2 = math.acos(p8.x/r_aux)
    '''alpha4 = math.acos(p1.x/Ri+i*2*math.pi/ns)
    alpha5 = math.acos(p12.x/Ri+i*2*math.pi/ns)'''
    while i<n_req_slots:
        beta1 = alpha1 - i * 360/ns*math.pi/180
        beta2 = alpha2 - i * 360/ns*math.pi/180
        #femm.mi_selectnode(r_aux*math.cos(beta), r_aux*math.sin(beta))
        femm.mi_createradius(r_aux * math.cos(beta1), r_aux * math.sin(beta1), s3)
        femm.mi_createradius(r_aux * math.cos(beta2), r_aux * math.sin(beta2), s3)
        femm.mi_drawarc(0, Ri, 0, -Ri, 180, 1)
        femm.mi_drawarc(0, -Ri, 0, Ri, 180, 1)

        i=i+1
    alpha3 = 2*math.pi/2/ns
    beta3 = alpha3 - (2*math.pi/ns)*n_req_slots
    if n_req_slots == ns:
        femm.mi_drawarc(0, Ro, 0, -Ro, 180)
        femm.mi_drawarc(0, -Ro, 0, Ro, 180)
        'ide még be kéne rakni a Di pontokat is, de fuck it, már nagyon késő van'
    else:
        femm.mi_drawarc(Ro * math.sin(-beta3), Ro * math.cos(beta3),
                        -Ro * math.sin(alpha3), Ro * math.cos(alpha3),
                        360 / ns * n_req_slots, 2)
        femm.mi_drawline(Ro * math.sin(-beta3), Ro * math.cos(beta3),0,0)
        femm.mi_drawline(-Ro * math.sin(alpha3), Ro * math.cos(alpha3), 0, 0)


    femm.mi_selectarcsegment(Ri*math.sin(2*math.pi/ns*n_req_slots-2*math.pi/ns/2),
                             Ri*math.cos(2*math.pi/ns*n_req_slots-2*math.pi/ns/2))
    femm.mi_deleteselectedarcsegments()
    femm.mi_selectarcsegment(-Ri * math.sin(2 * math.pi / ns / 1.9),
                             Ri * math.cos(2 * math.pi / ns / 1.9))
    femm.mi_deleteselectedarcsegments()
    femm.mi_selectnode(0,-Ri)
    femm.mi_deleteselectednodes()
    '''femm.mi_addnode((Ri - ag) * sin(-2 * pi / ns / 2), (Ri - ag) * cos(-2 * pi / ns / 2))
    femm.mi_addnode((Ri - ag) * sin(-2 * pi / ns / 2 + 2*pi/ns*n_req_slots),
                    (Ri - ag) * cos(-2 * pi / ns / 2 + 2*pi/ns*n_req_slots))'''
    femm.mi_drawarc((Ri - ag_s) * sin(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    (Ri - ag_s) * cos(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    (Ri - ag_s) * sin(-2 * pi / ns / 2),
                    (Ri - ag_s) * cos(-2 * pi / ns / 2),
                    360 / ns * n_req_slots,
                    1)

def draw_rotor(r1, r2, r3, mw, np, ns, n_req_slots, ag_r):
    # it jutott eszembe, hogy a szögfüggvényeket beimportálhatom, és akkor a .math nem is kell
    alpha0 = 2*pi/ns
    alpha1 = 2*pi/np
    alpha2 = asin(mw/(2*r2))
    alpha3 = asin(mw/(2*r3))
    pr1 = Node(r2*sin(-alpha0/2), r2*cos(alpha0/2))
    pr4 = Node(r2*sin(-alpha0/2+alpha1),r2*cos(-alpha0/2+alpha1))
    femm.mi_drawline(0,0,pr1.x,pr1.y)
    femm.mi_drawline(0, 0, pr4.x, pr4.y)
    femm.mi_drawarc(pr4.x, pr4.y, pr1.x, pr1.y, alpha1*180/pi,2)
    pr2 = Node(r2*sin(-alpha0/2+alpha1/2-alpha2/2),r2*cos(-alpha0/2+alpha1/2-alpha2/2))
    pr3 = Node(r2*sin(-alpha0/2+alpha1/2+alpha2/2),r2*cos(-alpha0/2+alpha1/2+alpha2/2))
    femm.mi_addnode(pr2.x, pr2.y)
    femm.mi_addnode(pr3.x, pr3.y)
    femm.mi_selectarcsegment(r2*sin(-alpha0/2+alpha1/2), r2*cos(-alpha0/2+alpha1/2))
    femm.mi_deleteselectedarcsegments()
    femm.mi_drawline(pr2.x, pr2.y, pr3.x, pr3.y)
    pr5 = Node(r3 * sin(-alpha0 / 2 + alpha1 / 2 - alpha3 / 2), r3 * cos(-alpha0 / 2 + alpha1 / 2 - alpha3 / 2))
    pr6 = Node(r3 * sin(-alpha0 / 2 + alpha1 / 2 + alpha3 / 2), r3 * cos(-alpha0 / 2 + alpha1 / 2 + alpha3 / 2))
    femm.mi_drawline(pr3.x, pr3.y, pr6.x, pr6.y)
    femm.mi_drawline(pr2.x, pr2.y, pr5.x, pr5.y)
    femm.mi_drawarc(pr6.x,pr6.y,pr5.x,pr5.y,alpha3*180/pi,1)
    femm.mi_selectsegment(pr2.x + (pr3.x - pr2.x) / 2, pr3.y + (pr2.y - pr3.y) / 2)
    femm.mi_selectsegment(pr2.x + (pr5.x - pr2.x) / 2, pr2.y + (pr5.y - pr2.y) / 2)
    femm.mi_selectsegment(pr3.x + (pr6.x - pr3.x) / 2, pr6.y + (pr3.y - pr6.y) / 2)
    femm.mi_selectsegment(r2/2*sin(-alpha0/2+alpha1),r2/2*cos(-alpha0/2+alpha1))
    femm.mi_copyrotate2(0, 0, -360 / (np), n_req_slots / 3 - 1, 1)
    femm.mi_selectarcsegment(pr1.x * 1.01, pr1.y)
    femm.mi_selectarcsegment(pr4.x, pr4.y * 1.01)
    femm.mi_selectarcsegment(pr5.x * 1.01, pr5.y*1.01)
    femm.mi_copyrotate2(0, 0, -360 / (np), n_req_slots / 3 - 1, 3)

    femm.mi_drawarc((r3 + ag_r) * sin(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    (r3 + ag_r) * cos(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    (r3 + ag_r) * sin(-2 * pi / ns / 2),
                    (r3 + ag_r) * cos(-2 * pi / ns / 2),
                    360 / ns * n_req_slots,
                    1)

    femm.mi_selectsegment((r3 + ag_r*1.01) * sin(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                          (r3 + ag_r*1.01) * cos(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots))
    femm.mi_selectsegment((r3 + ag_r*1.01) * sin(-2 * pi / ns / 2),
                          (r3 + ag_r*1.01) * cos(-2 * pi / ns / 2))
    femm.mi_deleteselected()

    femm.mi_drawarc(r1 * sin(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    r1 * cos(-2 * pi / ns / 2 + 2 * pi / ns * n_req_slots),
                    r1 * sin(-2 * pi / ns / 2),
                    r1 * cos(-2 * pi / ns / 2),
                    360 / ns * n_req_slots,
                    1)
    j=1
    while j<n_req_slots / 3:
        femm.mi_selectsegment(r2/2*sin(-alpha0/2+j*alpha1), r2/2*cos(-alpha0/2+j*alpha1))
        j=j+1
    femm.mi_deleteselected()
    k=0
    while k <= n_req_slots/3:
        femm.mi_selectsegment(r1/2*sin(-2*pi/ns/2+k*2*pi/np), r1/2*cos(-2*pi/ns/2+k*2*pi/np))
        k = k + 1
    femm.mi_deleteselected()
    femm.mi_selectnode(0,0)
    femm.mi_deleteselected()


def add_blocklabels(Ro, Ri, r2, r3, ns, np, n_req_slots):
    k=0
    while k < n_req_slots: # slots
        femm.mi_addblocklabel((Ri+(Ro-Ri)/3)*sin(k*2*pi/ns),(Ri+(Ro-Ri)/3)*cos(k*2*pi/ns))
        femm.mi_selectlabel((Ri+(Ro-Ri)/3)*sin(k*2*pi/ns),(Ri+(Ro-Ri)/3)*cos(k*2*pi/ns))
        femm.mi_setblockprop('Air', 1, 1, )
        femm.mi_clearselected()
        k = k + 1

    i=0
    while i <= n_req_slots // 3-1: # magnets
        femm.mi_addblocklabel(r3 * 0.99 * sin(-2 * pi / ns / 2 + 2 * pi / np / 2 + i*2*pi/np),
                              r3 * 0.99 * cos(-2 * pi / ns / 2 + 2 * pi / np / 2 + i*2*pi/np))
        femm.mi_selectlabel(r3 * 0.99 * sin(-2 * pi / ns / 2 + 2 * pi / np / 2 + i*2*pi/np),
                              r3 * 0.99 * cos(-2 * pi / ns / 2 + 2 * pi / np / 2 + i*2*pi/np))
        femm.mi_setblockprop('Magnet', 1, 25,'<None',90+180/ns-180/np-i*360/np)
        femm.mi_clearselected()
        i = i + 1

    femm.mi_addblocklabel(Ro*0.99 * sin(2 * pi / ns), Ro*0.99 * cos(2 * pi / ns)) # stator yoke
    femm.mi_selectlabel(Ro*0.99 * sin(2 * pi / ns), Ro*0.99 * cos(2 * pi / ns))
    femm.mi_setblockprop('Stator', 1, 1, )
    femm.mi_clearselected()
    femm.mi_addblocklabel(r2 * 0.9 * sin(2 * pi / ns), r2 * 0.9 * cos(2 * pi / ns)) # rotor yoke
    femm.mi_selectlabel(r2 * 0.9 * sin(2 * pi / ns), r2 * 0.9 * cos(2 * pi / ns))
    femm.mi_setblockprop('Rotor', 1, 1, )
    femm.mi_clearselected()
    femm.mi_addblocklabel(Ri * 0.99 * sin(2 * pi / ns), Ri * 0.99 * cos(2 * pi / ns)) # stator airgap
    femm.mi_selectlabel(Ri * 0.99 * sin(2 * pi / ns), Ri * 0.99 * cos(2 * pi / ns))
    femm.mi_setblockprop('Air', 1, 1, )
    femm.mi_clearselected()
    femm.mi_addblocklabel(r3 * sin(-2 * pi / ns/2*0.9), r3 * 0.99 * cos(-2 * pi / ns/2*0.9)) # rotor airgap'''
    femm.mi_selectlabel(r3 * sin(-2 * pi / ns/2*0.9), r3 * 0.99 * cos(-2 * pi / ns/2*0.9))
    femm.mi_setblockprop('Air', 1, 1, )
    femm.mi_clearselected()

draw_stator(20, 10, 0.5,1,2.5,2,0.2,0.3,4,0.2,0.1, 24,6, 0.2)
draw_rotor(2,8,9,6,8,24, 6, 0.2)
add_blocklabels(20,10, 8, 9,24, 8,6)
#-------------------------------------------------problem definition--------------------------------------------------
femm.mi_addmaterial('Air',1,1,0,0,0,0,0,1,0,0,0)
femm.mi_addmaterial('Rotor',1,1,0,0,0,0,0,1,0,0,0)
femm.mi_addmaterial('Stator',1,1,0,0,0,0,0,1,0,0,0)
femm.mi_addmaterial('Magnet',1,1,23000,0,0,0,0,1,0,0,0)
femm.mi_getmaterial('Pure Iron')
femm.mi_addboundprop('A0',0,0,0,0,0,0,0,0,0,0,0)
femm.mi_addboundprop('apbc1',0,0,0,0,0,0,0,0,5,0,0)
femm.mi_addboundprop('apbc2',0,0,0,0,0,0,0,0,5,0,0)
femm.mi_addboundprop('apbc3',0,0,0,0,0,0,0,0,5,0,0)
femm.mi_addboundprop('apbc4',0,0,0,0,0,0,0,0,5,0,0)
femm.mi_addboundprop('apag',0,0,0,0,0,0,0,0,7,0,0)

#femm.mi_seteditmode('arcsegments')
femm.mi_selectarcsegment(0,Ro)
femm.mi_setarcsegmentprop(25,'A0',0,0)
femm.mi_clearselected()
femm.mi_selectarcsegment(0,Ri-ag_s)
femm.mi_selectarcsegment(0,r3+ag_r)
femm.mi_setarcsegmentprop(25,'apag',0,0)
femm.mi_clearselected()
#femm.mi_seteditmode('segments')
femm.mi_selectsegment(Ro*0.99*sin(-pi/ns),Ro*0.99*cos(pi/ns))
femm.mi_selectsegment(Ro*0.99*sin(-pi/ns+2*pi/ns*n_req_slots),Ro*0.99*cos(-pi/ns+2*pi/ns*n_req_slots))
femm.mi_setsegmentprop('apbc1',25,1,0,1) # stator
femm.mi_clearselected()
femm.mi_selectsegment(Ri*0.99*sin(-pi/ns),Ri*0.99*cos(-pi/ns))
femm.mi_selectsegment(Ri*0.99*sin(-pi/ns+2*pi/ns*n_req_slots),Ri*0.99*cos(-pi/ns+2*pi/ns*n_req_slots))
femm.mi_setsegmentprop('apbc2',25,1,0,1) # stator airgap
femm.mi_clearselected()
femm.mi_selectsegment(r3*sin(-pi/ns),r3*cos(-pi/ns))
femm.mi_selectsegment(r3*sin(-pi/ns+2*pi/ns*n_req_slots),r3*cos(-pi/ns+2*pi/ns*n_req_slots))
femm.mi_setsegmentprop('apbc3',25,1,0,1) # rotor airgap
femm.mi_clearselected()
femm.mi_selectsegment(r2*0.99*sin(-pi/ns),r2*0.99*cos(-pi/ns))
femm.mi_selectsegment(r2*0.99*sin(-pi/ns+2*pi/ns*n_req_slots),r2*0.99*cos(-pi/ns+2*pi/ns*n_req_slots))
femm.mi_setsegmentprop('apbc4',25,1,0,1) # rotor
femm.mi_clearselected()
#-----------------------------------------------------------------------------------------------------------------------
femm.mi_saveas("temp.fem")
breakpoint()
print('Abrakadabra')