# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:40:32 2021

@author: André Dias
"""

from tkinter import *
from tkinter import filedialog
from tkinter.constants import DISABLED, NORMAL
from tkinter.ttk import *
import pandas as pd
import posixpath
import os
import tkinter as tk
import pandas as pd
import math
import ntpath
import pathlib
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.title('Non-Cross-Linking calculator | Made by André Dias')
root.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')

def SSCreadfiles():
    z = pd.read_csv(filename, skiprows = 1, sep = ',', decimal ='.', engine = 'python')
    r = np.array(z)
    return r

def SSCheaders():
    hd = []
    n = 1
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 0)
        y = x.columns.values
        for element in y:
            n = n + 1
            if n%2 == 0:
                hd.append(element)
        hd.pop()
        return hd

def SSCnumbercolumns():
    numcol = 0
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 1)
        for element in x:
            numcol = numcol + 1
    return(numcol)

def SSCcalmax(numcol, r, hd):
    t = {}
    t1 = {}
    for i in range(int((numcol-1)/2)):
        n = i + 1
        t[hd[i]] = r[:,i+n].max()
        x = r[:,i+n].min()
        y = r[:,i+n]
        y1 = np.subtract(y,x)
        t1[hd[i]] = y1.max()
    return t, t1

def SSCwavemax(r, t, t1, numcol, hd):
    m = {}
    m1 = {}
    o = 0
    for i in range(int((numcol-1)/2)):
        b = i + 1
        p = i * 2
        y = r[:,p]
        u = r[:,i+b]
        u1 = r[:,i+b]
        x = r[:,i+b].min()
        for line in u1:
            line = line - x
        for line in u:
            if line != t[hd[i]]:
                o = o + 1
            else:
                m[hd[i]] = y[o]
        o = 0
        for line in u1:
            if line != t1[hd[i]]:
                o = o + 1
            else:
                m1[hd[i]] = [0]
        o = 0
    return m, m1

def SSCcalmin(r, m, m1, numcol, hd):
    n = {}
    n1 = {}
    count = 0
    for i in range(int((numcol-1)/2)):
        b = i + 1
        p = i * 2
        y = r[:,p]
        u = r[:,i+b]
        x = r[:,i+b].min()
        u1 = np.subtract(u,x)
        for line in y:
            t = str(round(line))
            if '450' not in t:
                count = count + 1
            else:
                n[hd[i]] = u[count]
        count = 0
        for line in y:
            t1 = str(round(line))
            if '450' not in t1:
                count = count + 1
            else:
                n1[hd[i]] = u1[count]
        count = 0
    return n, n1

def SSCratio(r,t,t1,n,n1,numcol,hd):
    rat = {}
    rat1 = {}
    for i in range(int((numcol-1)/2)):
        rat[hd[i]] = round(t[hd[i]]/n[hd[i]],3)
        rat1[hd[i]] = round(t1[hd[i]]/n1[hd[i]],3)
    return rat, rat1

def SSCsize(r,rat,rat1,numcol,hd):
    siz = {}
    siz1 = {}
    for i in range(int((numcol-1)/2)):
        siz[hd[i]] = round(0.112*math.exp(2.998*rat[hd[i]]),1)
        siz1[hd[i]] = round(0.112*math.exp(2.998*rat1[hd[i]]),1)
    return siz, siz1

def SSCaveragesize(r,siz,siz1,numcol,hd):
    x = 0
    y = 0
    for i in range(int((numcol-1)/2)):
        x = x + siz[hd[i]]
        y = y + siz1[hd[i]]
    avgsz = round(x/int((numcol-1)/2),1)
    avgsz1 = round(y/int((numcol-1)/2),1)
    return avgsz, avgsz1

def SSCconcentration(r,siz,siz1,n,n1,numcol,hd):
    dilution = float(e1.get())
    conc = {}
    conc1 = {}
    for i in range(int((numcol-1)/2)):
        x = np.log(siz[hd[i]])*3.0869 + 10.869
        x1 = np.log(siz1[hd[i]])*3.0869 + 10.869
        y = math.exp(x)
        y1 = math.exp(x1)
        conc[hd[i]] = round((n[hd[i]] * dilution / y * 10**9),2)
        conc1[hd[i]] = round((n1[hd[i]] * dilution / y1 * 10**9),2)
    return conc, conc1

def SSCaverageconcentration(r,conc,conc1,numcol,hd):
    x = 0
    y = 0
    for i in range(int((numcol-1)/2)):
        x = x + conc[hd[i]]
        y = y + conc1[hd[i]]
    avgconc = round(x/int((numcol-1)/2),2)
    avgconc1 = round(y/int((numcol-1)/2),2)
    return avgconc, avgconc1

def SSCclicked():
    global filename, e1
    filename = tk.filedialog.askopenfilename(initialdir = 'shell:Desktop', title = 'Select a csv file', filetypes = (('csv files','*.csv'),))
    e1 = tk.Entry(root, width = 10)
    e1.grid(row = 4, column = 1)
    l2 = tk.Label(root, text = 'Enter dilution factor:')
    l2.grid(row = 4, column = 0)
    b11 = tk.Button(root, text = 'GO!', command = calglobal)
    b11.grid(row = 11, column = 0)

def MSCreadfiles():
    r = {}
    i = -1
    for element in try2:
        i = i + 1
        if i <= len(try2):
            if 'xls' in element:
                x = pd.read_excel(element,skiprows = 0)
                r['r'+str(i)] = np.array(x)
            elif 'txt' in element:
                x = pd.read_csv(element, sep = '\t', decimal = ',', skiprows = 0, engine = 'python')
                r['r'+str(i)] = np.array(x)
    return r

def MSCcalmax(r):
    t = {}
    for i in range(len(r)):
        x = r['r'+str(i)]
        y = x[:,1]
        t['max'+str(i)] = y.max()
        i = i + 1
    return t

def MSCwavemax(r,t):
    m = {}
    o = 0
    for i in range(len(r)):
        x = r['r'+str(i)]
        y = x[:,0]
        u = x[:,1]
        for line in u:
            if line != t['max'+str(i)]:
                o = o + 1
            else:
                m['wmax'+str(i)] = y[o]
        o = 0
        i = i + 1
    return m

def MSCcalmin(r):
    n = {}
    for i in range(len(r)):
        x = r['r'+str(i)]
        for line in x:
            y = line
            if 450 in y:
                n['wmin'+str(i)] = y[1]
        i = i + 1
    return n

def MSCratio(r,t,n):
    rat = {}
    for i in range(len(r)):
        rat['ratio'+str(i)] = round(t['max'+str(i)]/n['wmin'+str(i)],3)
    return rat

def MSCsize(r,rat):
    siz = {}
    for i in range(len(r)):
        siz['size'+str(i)] = round(0.112*math.exp(2.998*rat['ratio'+str(i)]),1)
    return siz

def MSCaveragesize(r,siz):
    x = 0
    for i in range(len(r)):
        x = x + siz['size'+str(i)]
    avgsz = round(x/len(r),1)
    return avgsz

def MSCconcentration(r,siz,n):
    dilution = float(e1.get())
    conc = {}
    for i in range(len(r)):
        x = np.log(siz['size'+str(i)])*3.0869 + 10.869
        y = math.exp(x)
        conc['conc'+str(i)] = round((n['wmin'+str(i)] * dilution / y * 10**9),2)
    return conc

def MSCaverageconcentration(r,conc):
    x = 0
    for i in range(len(r)):
        x = x + conc['conc'+str(i)]
    avgconc = round(x/len(r),2)
    return avgconc

def MSCclicked():
    global try2, e1
    root.filename = tk.filedialog.askopenfilenames(initialdir = 'shell:Desktop', title = 'Select xls files', filetypes = (('xls files','*.xls'),('xlsx files','*.xlsx')))
    try1 = []
    try2 = []
    n = 0
    for element in root.filename:
        chacho = ntpath.basename(root.filename[n])
        n = n + 1
        try2.append(element)
    e1 = tk.Entry(root, width = 10)
    e1.grid(row = 4, column = 1)
    l2 = tk.Label(root, text = 'Enter dilution factor:')
    l2.grid(row = 4, column = 0)
    b11 = tk.Button(root, text = 'GO!', command = calglobal)
    b11.grid(row = 11, column = 0)

def SSreadfiles():
    z = pd.read_csv(filename, skiprows = 1, sep = ',', decimal ='.', engine = 'python')
    r = np.array(z)
    return r

def SSheaders():
    hd = []
    n = 1
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 0)
        y = x.columns.values
        for element in y:
            n = n + 1
            if n%2 == 0:
                hd.append(element)
        hd.pop()
        return hd

def SSnumbercolumns():
    numcol = 0
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 1)
        for element in x:
            numcol = numcol + 1
    return(numcol)

def SSsubtraction(r):
    x = (numcontrol + 1) + numcontrol
    y = (numsaltcontrol + 1) + numsaltcontrol
    z = r[:,x] - r[:,y]
    v = r[:,0]
    cnt = np.column_stack((v,r[:,x]))
    slcnt = np.column_stack((v,r[:,y]))
    sub = np.column_stack((v,z))
    return sub, cnt, slcnt

def SScalmax(sub, cnt):
    t = {}
    t['maxR'] = cnt[:,1].max()
    t['maxS'] = sub[:,1].max()
    return t

def SSwavemax(sub, cnt, t):
    m = {}
    count = 0
    for line in cnt[:,1]:
        if line != t['maxR']:
            count = count + 1
        else:
            m['WmaxR'] = cnt[count,0]
    count = 0
    for line in sub[:,1]:
        if line != t['maxS']:
            count = count + 1
        else:
            m['WmaxS'] = sub[count,0]
    return m

def SScalmin(sub, slcnt):
    n = {}
    n['minR'] = slcnt[:,1].max()
    n['minS'] = sub[:,1].min()
    return n

def SSwavemin(sub, slcnt, n):
    b = {}
    count = 0
    try:
        b['WminR'] = float(e1.get())
    except:
        for line in slcnt[:,1]:
            if line != n['minR']:
                count = count + 1
            else:
                b['WminR'] = slcnt[count,0]
    count = 0
    for line in sub[:,1]:
        if line != n['minS']:
            count = count + 1
        else:
            b['WminS'] = sub[count,0]
    return b

def SSfindmax(r, hd, m):
    maxR = {}
    maxS = {}
    for i in range(len(hd)):
        z = i + 1 + i
        v = i * 2
        count = -1
        x = r[:,v]
        for line in x:
            y = line
            count = count + 1
            if round(m['WmaxR']) == round(y):
                maxR[hd[i]] = r[count,z]
        count = -1
        for line in x:
            y = line
            count = count + 1
            if round(m['WmaxS']) == round(y):
                maxS[hd[i]] = r[count,z]
    return maxR, maxS

def SSfindmin(r, hd, b):
    minR = {}
    minS = {}
    for i in range(len(hd)):
        z = i + 1 + i
        v = i * 2
        count = -1
        x = r[:,v]
        for line in x:
            y = line
            count = count + 1
            if round(b['WminR']) == round(y):
                minR[hd[i]] = r[count,z]
        count = -1
        for line in x:
            y = line
            count = count + 1
            if round(b['WminS']) == round(y):
                minS[hd[i]] = r[count,z]
    return minR, minS

def SScalratio(maxR, minR, maxS, minS, hd):
    ratR = {}
    ratS = {}
    for i in range(len(maxR)):
        x1 = maxR[hd[i]]
        x2 = maxS[hd[i]]
        y1 = minR[hd[i]]
        y2 = minS[hd[i]]
        ratR[hd[i]] = round(x1/y1,2)
        ratS[hd[i]] = round(x2/y2,2)
    return ratR, ratS

def SSclicked():
    global filename, e1
    filename = tk.filedialog.askopenfilename(initialdir = 'shell:Desktop', title = 'Select a csv file', filetypes = (('csv files','*.csv'),))
    hd = SSheaders()
    o1 = tk.OptionMenu(root, v, *hd, command = SScallback)
    o1.grid(row = 2, column = 1)
    o2 = tk.OptionMenu(root, v1, *hd, command = SScallback1)
    o2.grid(row = 3, column = 1)
    l1 = tk.Label(root, text = 'Enter manual wavelength of aggregates (leave empty if automatic works)')
    l1.grid(row = 4, column = 0)
    l2 = tk.Label(root, text = 'Select Control:')
    l2.grid(row = 2, column = 0)
    l3 = tk.Label(root, text = 'Select sample with highest salt concentration:')
    l3.grid(row = 3, column = 0)
    e1 = tk.Entry(root, width = 20, text = v2)
    e1.grid(row = 4, column = 1)
    b2 = tk.Button(root, text = 'GO!', command = calglobal)
    b2.grid(row = 10, column = 0)

def SScallback(selection):
    global numcontrol
    hd = SSheaders()
    control = selection
    count = 0
    for element in hd:
        if control != element:
            count = count + 1
        else:
            numcontrol = count

def SScallback1(selection):
    global numsaltcontrol
    hd = SSheaders()
    saltcontrol = selection
    count = 0
    for element in hd:
        if saltcontrol != element:
            count = count + 1
        else:
            numsaltcontrol = count
    z = pd.read_csv(filename, skiprows = 1, sep = ',', decimal ='.', engine = 'python')
    r = np.array(z)
    for i in range(len(hd)):
        if i == count:
            q = 2 * i + 1
            w = 2 * i
            x = r[:,q]
            y = r[:,w]
            plt.plot(y,x)
            plt.show(block = False)

def MSreadfiles():
    global name
    r = {}
    name = []
    for element in try2:
        chacho = ntpath.basename(element)
        chacho = chacho.split('.xls')
        segment = chacho[0]
        name.append(segment)
        if 'xls' in element:
            x = pd.read_excel(element,skiprows = 0)
            r[segment] = np.array(x)
        elif 'txt' in element:
            x = pd.read_csv(element, sep = '\t', decimal = ',', skiprows = 0, engine = 'python')
            r[segment] = np.array(x)
    return r

def MScalmax():
    t1 = control[:,1].max()
    t2 = sub[:,1].max()
    return t1, t2

def MSwavemax(t1, t2):
    count = 0
    count2 = 0
    for line in control[:,1]:
        if line != t1:
            count = count + 1
        elif line == t1:
            m1 = control[count,0]
    for line in sub[:,1]:
        if line != t2:
            count2 = count2 + 1
        elif line == t2:
            m2 = sub[count2,0]
    return m1, m2

def MScalmin():
    n1 = saltcontrol[:,1].max()
    n2 = sub[:,1].min()
    return n1, n2

def MSwavemin(n1, n2):
    count = 0
    count2 = 0
    try:
        b1 = float(e1.get())
    except:
        for line in saltcontrol[:,1]:
            if line != n1:
                count = count + 1
            elif line == n1:
                b1 = saltcontrol[count,0]
    for line in sub[:,1]:
        if line != n2:
            count2 = count2 + 1
        elif line == n2:
            b2 = sub[count2,0]
    return b1, b2

def MSfindmax(m1, m2, r):
    maxR = {}
    maxS = {}
    for element in name:
        x = r[element]
        for line in x:
            y = line
            if m1 in y:
                maxR[element] = y[1]
        for line in x:
            y = line
            if m2 in y:
                maxS[element] = y[1]
    return maxR, maxS

def MSfindmin(b1, b2, r):
    minR = {}
    minS = {}
    for element in name:
        x = r[element]
        for line in x:
            y = line
            if b1 in y:
                minR[element] = y[1]
        for line in x:
            y = line
            if b2 in y:
                minS[element] = y[1]
    return minR, minS

def MScalratio(maxR, minR, maxS, minS, r):
    ratR = {}
    ratS = {}
    for element in name:
        x1 = maxR[element]
        x2 = maxS[element]
        y1 = minR[element]
        y2 = minS[element]
        ratR[element] = round(x1/y1,2)
        ratS[element] = round(x2/y2,2)
    return ratR, ratS

def MScallback(selection):
    global control
    opt1 = selection
    for element in try2:
        j = element.split('/')
        h = j[-1]
        if h == opt1:
            x = pd.read_excel(element, skiprows = 0)
            control = np.array(x)

def MScallback1(selection):
    global sub, saltcontrol
    opt2 = selection
    for element in try2:
        j = element.split('/')
        h = j[-1]
        if h == opt2:
            x = pd.read_excel(element, skiprows = 0)
            saltcontrol = np.array(x)
    sub = control.copy()
    sub[:,1] = sub[:,1] - saltcontrol[:,1]
    q = saltcontrol[:,0]
    w = saltcontrol[:,1]
    plt.plot(q,w)
    plt.show(block = False)

def MSclicked():
    global try1, try2, o1, o2, e1
    root.filename = tk.filedialog.askopenfilenames(initialdir = 'shell:Desktop', title = 'Select xls files', filetypes = (('xls files','*.xls'),('xlsx files','*.xlsx')))
    try1 = []
    try2 = []
    for n in range(len(root.filename)):
        chacho = ntpath.basename(root.filename[n])
        try1.append(chacho)
        try2.append(root.filename[n])
    o1 = tk.OptionMenu(root, v, *try1, command = MScallback)
    o1.grid(row = 2, column = 1)
    o2 = tk.OptionMenu(root, v1, *try1, command = MScallback1)
    o2.grid(row = 3, column = 1)
    l1 = tk.Label(root, text = 'Enter manual wavelength of aggregates (leave empty if automatic works)')
    l1.grid(row = 4, column = 0)
    l2 = tk.Label(root, text = 'Select Control:')
    l2.grid(row = 2, column = 0)
    l3 = tk.Label(root, text = 'Select sample with highest salt concentration:')
    l3.grid(row = 3, column = 0)
    e1 = tk.Entry(root, width = 20, text = v2)
    e1.grid(row = 4, column = 1)
    b2 = tk.Button(root, text = 'GO!', command = calglobal)
    b2.grid(row = 10, column = 0)

def SCreadfiles():
    z = pd.read_csv(filename, skiprows = 1, sep = ',', decimal ='.', engine = 'python')
    r = np.array(z)
    return r

def SCheaders():
    hd = []
    n = 1
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 0)
        y = x.columns.values
        for element in y:
            n = n + 1
            if n%2 == 0:
                hd.append(element)
        hd.pop()
        return hd

def SCnumbercolumns():
    numcol = 0
    if 'csv' in filename:
        x = pd.read_csv(filename, skiprows = 1)
        for element in x:
            numcol = numcol + 1
    return(numcol)

def SCsubtraction(r):
    x = (numcontrol + 1) + numcontrol
    y = (numsaltcontrol + 1) + numsaltcontrol
    z = r[:,x] - r[:,y]
    v = r[:,0]
    cnt = np.column_stack((v,r[:,x]))
    slcnt = np.column_stack((v,r[:,y]))
    sub = np.column_stack((v,z))
    return sub, cnt, slcnt

def SCcalmax(sub, cnt):
    t = {}
    t['maxR'] = cnt[:,1].max()
    t['maxS'] = sub[:,1].max()
    return t

def SCwavemax(sub, cnt, t):
    m = {}
    count = 0
    for line in cnt[:,1]:
        if line != t['maxR']:
            count = count + 1
        else:
            m['WmaxR'] = round(cnt[count,0])
    count = 0
    for line in sub[:,1]:
        if line != t['maxS']:
            count = count + 1
        else:
            m['WmaxS'] = round(sub[count,0])
    return m

def SCcalmin(sub, slcnt):
    n = {}
    n['minR'] = slcnt[:,1].max()
    n['minS'] = sub[:,1].min()
    return n

def SCwavemin(sub, slcnt, n):
    b = {}
    count = 0
    try:
        b['WminR'] = float(e1.get())
    except:
        for line in slcnt[:,1]:
            if line != n['minR']:
                count = count + 1
            else:
                b['WminR'] = round(slcnt[count,0])
    count = 0
    for line in sub[:,1]:
        if line != n['minS']:
            count = count + 1
        else:
            b['WminS'] = round(sub[count,0])
    return b

def SCfindmax(r, hd, m):
    maxR = {}
    maxS = {}
    for i in range(len(hd)):
        z = i + 1 + i
        v = i * 2
        count = -1
        x = r[:,v]
        for line in x:
            y = line
            count = count + 1
            if round(m['WmaxR']) == round(y):
                maxR[hd[i]] = r[count,z]
        count = -1
        for line in x:
            y = line
            count = count + 1
            if round(m['WmaxS']) == round(y):
                maxS[hd[i]] = r[count,z]
    return maxR, maxS

def SCfindmin(r, hd, b):
    minR = {}
    minS = {}
    for i in range(len(hd)):
        z = i + 1 + i
        v = i * 2
        count = -1
        x = r[:,v]
        for line in x:
            y = line
            count = count + 1
            if round(b['WminR']) == round(y):
                minR[hd[i]] = r[count,z]
        count = -1
        for line in x:
            y = line
            count = count + 1
            if round(b['WminS']) == round(y):
                minS[hd[i]] = r[count,z]
    return minR, minS

def SCcalratio(maxR, minR, maxS, minS, hd):
    ratR = {}
    ratS = {}
    for i in range(len(maxR)):
        x1 = maxR[hd[i]]
        x2 = maxS[hd[i]]
        y1 = minR[hd[i]]
        y2 = minS[hd[i]]
        ratR[hd[i]] = round(x1/y1,2)
        ratS[hd[i]] = round(x2/y2,2)
    return ratR, ratS

def SCcallback(selection):
    global numcontrol
    hd = SCheaders()
    control = selection
    count = 0
    for element in hd:
        if control != element:
            count = count + 1
        else:
            numcontrol = count

def SCcallback1(selection):
    global numsaltcontrol
    hd = SCheaders()
    saltcontrol = selection
    count = 0
    for element in hd:
        if saltcontrol != element:
            count = count + 1
        else:
            numsaltcontrol = count
    z = pd.read_csv(filename, skiprows = 1, sep = ',', decimal ='.', engine = 'python')
    r = np.array(z)
    for i in range(len(hd)):
        if i == numsaltcontrol:
            q = 2 * i + 1
            w = 2 * i
            x = r[:,q]
            y = r[:,w]
            plt.plot(y,x)
            plt.show(block = False)

def SCclicked():
    global filename, e1
    filename = tk.filedialog.askopenfilename(initialdir = 'shell:Desktop', title = 'Select a csv file', filetypes = (('csv files','*.csv'),))
    hd = SCheaders()
    o1 = tk.OptionMenu(root, v, *hd, command = SCcallback)
    o1.grid(row = 2, column = 1)
    o2 = tk.OptionMenu(root, v1, *hd, command = SCcallback1)
    o2.grid(row = 3, column = 1)
    l1 = tk.Label(root, text = 'Enter manual wavelength of aggregates (leave empty if automatic works)')
    l1.grid(row = 4, column = 0)
    l2 = tk.Label(root, text = 'Select Control:')
    l2.grid(row = 2, column = 0)
    l3 = tk.Label(root, text = 'Select Negative control:')
    l3.grid(row = 3, column = 0)
    e1 = tk.Entry(root, width = 20, text = v2)
    e1.grid(row = 4, column = 1)
    b2 = tk.Button(root, text = 'GO!', command = calglobal)
    b2.grid(row = 10, column = 0)

def MCreadfiles():
    global name
    r = {}
    name = []
    for element in try2:
        chacho = ntpath.basename(element)
        chacho = chacho.split('.xls')
        segment = chacho[0]
        name.append(segment)
        print(name)
        if 'xls' in element:
            x = pd.read_excel(element,skiprows = 0)
            r[segment] = np.array(x)
        elif 'txt' in element:
            x = pd.read_csv(element, sep = '\t', decimal = ',', skiprows = 0, engine = 'python')
            r[segment] = np.array(x)
    return r

def MCcalmax():
    t1 = control[:,1].max()
    t2 = sub[:,1].max()
    return t1, t2

def MCwavemax(t1, t2):
    count = 0
    count2 = 0
    for line in control[:,1]:
        if line != t1:
            count = count + 1
        elif line == t1:
            m1 = control[count,0]
    for line in sub[:,1]:
        if line != t2:
            count2 = count2 + 1
        elif line == t2:
            m2 = sub[count2,0]
    return m1, m2

def MCcalmin():
    n1 = saltcontrol[:,1].max()
    n2 = sub[:,1].min()
    return n1, n2

def MCwavemin(n1, n2):
    count = 0
    count2 = 0
    try:
        b1 = float(e1.get())
    except:
        for line in saltcontrol[:,1]:
            if line != n1:
                count = count + 1
            elif line == n1:
                b1 = saltcontrol[count,0]
    for line in sub[:,1]:
        if line != n2:
            count2 = count2 + 1
        elif line == n2:
            b2 = sub[count2,0]
    return b1, b2

def MCfindmax(m1, m2, r):
    maxR = {}
    maxS = {}
    for element in name:
        x = r[element]
        for line in x:
            y = line
            if m1 in y:
                maxR[element] = y[1]
        for line in x:
            y = line
            if m2 in y:
                maxS[element] = y[1]
    return maxR, maxS

def MCfindmin(b1, b2, r):
    minR = {}
    minS = {}
    for element in name:
        x = r[element]
        for line in x:
            y = line
            if b1 in y:
                minR[element] = y[1]
        for line in x:
            y = line
            if b2 in y:
                minS[element] = y[1]
    return minR, minS

def MCcalratio(maxR, minR, maxS, minS, r):
    ratR = {}
    ratS = {}
    for element in name:
        x1 = maxR[element]
        x2 = maxS[element]
        y1 = minR[element]
        y2 = minS[element]
        ratR[element] = round(x1/y1,2)
        ratS[element] = round(x2/y2,2)
    return ratR, ratS

def MCcallback(selection):
    global control
    opt1 = selection
    for element in try2:
        j = element.split('/')
        h = j[-1]
        if h == opt1:
            x = pd.read_excel(element, skiprows = 0)
            control = np.array(x)

def MCcallback1(selection):
    global sub, saltcontrol
    opt2 = selection
    for element in try2:
        j = element.split('/')
        h = j[-1]
        if h == opt2:
            x = pd.read_excel(element, skiprows = 0)
            saltcontrol = np.array(x)
    sub = control.copy()
    sub[:,1] = sub[:,1] - saltcontrol[:,1]
    q = saltcontrol[:,0]
    w = saltcontrol[:,1]
    plt.plot(q,w)
    plt.show(block = False)

def MCclicked():
    global try1, try2, o1, o2, e1
    root.filename = tk.filedialog.askopenfilenames(initialdir = 'shell:Desktop', title = 'Select xls files', filetypes = (('xls files','*.xls'),('xlsx files','*.xlsx')))
    try1 = []
    try2 = []
    for n in range(len(root.filename)):
        chacho = ntpath.basename(root.filename[n])
        try1.append(chacho)
        try2.append(root.filename[n])
    o1 = tk.OptionMenu(root, v, *try1, command = MCcallback)
    o1.grid(row = 2, column = 1)
    o2 = tk.OptionMenu(root, v1, *try1, command = MCcallback1)
    o2.grid(row = 3, column = 1)
    l1 = tk.Label(root, text = 'Enter manual wavelength of aggregates (leave empty if automatic works)')
    l1.grid(row = 4, column = 0)
    l2 = tk.Label(root, text = 'Select Control:')
    l2.grid(row = 2, column = 0)
    l3 = tk.Label(root, text = 'Select Negative control:')
    l3.grid(row = 3, column = 0)
    e1 = tk.Entry(root, width = 20, text = v2)
    e1.grid(row = 4, column = 1)
    b2 = tk.Button(root, text = 'GO!', command = calglobal)
    b2.grid(row = 10, column = 0)

def calglobal():
    global top
    if s == 1 and k == 1:
        r = SSCreadfiles()
        numcol = SSCnumbercolumns()
        hd = SSCheaders()
        t, t1 = SSCcalmax(numcol, r, hd)
        m, m1 = SSCwavemax(r, t, t1, numcol, hd)
        n, n1 = SSCcalmin(r, m, m1, numcol, hd)
        rat, rat1 = SSCratio(r,t,t1,n,n1,numcol,hd)
        siz, siz1 = SSCsize(r,rat,rat1,numcol,hd)
        avgsz, avgsz1 = SSCaveragesize(r,siz,siz1,numcol,hd)
        conc, conc1 = SSCconcentration(r,siz,siz1,n,n1,numcol,hd)
        avgconc, avgconc1 = SSCaverageconcentration(r,conc,conc1,numcol,hd)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Maximum:')
        lab1.grid(row = 1, column = 0)
        lab8 = tk.Label(top, text = 'Maximum: (baseline)')
        lab8.grid(row = 2, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at max:')
        lab2.grid(row = 3, column = 0)
        lab3 = tk.Label(top, text = 'Absorbance at 450 nm:')
        lab3.grid(row = 5, column = 0)
        lab10 = tk.Label(top, text = 'Absorbance at 450 nm: (baseline)')
        lab10.grid(row = 6, column = 0)
        lab4 = tk.Label(top, text = 'Size (nm):')
        lab4.grid(row = 7, column = 0)
        lab11 = tk.Label(top, text = 'Size (nm): (baseline)')
        lab11.grid(row = 9, column = 0)
        lab5 = tk.Label(top, text = 'Average Size (nm):')
        lab5.grid(row = 8, column = 0)
        lab12 = tk.Label(top, text = 'Average Size (nm): (baseline)')
        lab12.grid(row = 10, column = 0)
        lab6 = tk.Label(top, text = 'Concentration (nM):')
        lab6.grid(row = 11, column = 0)
        lab13 = tk.Label(top, text = 'Concentration (nM): (baseline)')
        lab13.grid(row = 13, column = 0)
        lab7 = tk.Label(top, text = 'Average concentration (nM):')
        lab7.grid(row = 12, column = 0)
        lab14 = tk.Label(top, text = 'Average concentration (nM): (baseline)')
        lab14.grid(row = 14, column = 0)
        i = 0
        for element in t:
            lab = tk.Label(top, text = round(t[element],3))
            lab.grid(row = 1, column = i + 1)
            i = i + 1
        i = 0
        for element in t1:
            lab = tk.Label(top, text = round(t1[element],3))
            lab.grid(row = 2, column = i + 1)
            i = i + 1
        i = 0
        for element in m:
            lab = tk.Label(top, text = round(m[element]))
            lab.grid(row = 3, column = i + 1)
            i = i + 1
        i = 0
        for element in n:
            lab = tk.Label(top, text = round(n[element],3))
            lab.grid(row = 5, column = i + 1)
            i = i + 1
        i = 0
        for element in n1:
            lab = tk.Label(top, text = round(n1[element],3))
            lab.grid(row = 6, column = i + 1)
            i = i + 1
        i = 0
        for element in siz:
            lab = tk.Label(top, text = siz[element])
            lab.grid(row = 7, column = i + 1)
            i = i + 1
        i = 0
        for element in siz1:
            lab = tk.Label(top, text = siz1[element])
            lab.grid(row = 9, column = i + 1)
            i = i + 1
        i = 0
        for element in conc:
            lab = tk.Label(top, text = conc[element])
            lab.grid(row = 11, column = i + 1)
            i = i + 1
        i = 0
        for element in conc1:
            lab = tk.Label(top, text = conc1[element])
            lab.grid(row = 13, column = i + 1)
            i = i + 1
        i = 0
        for element in hd:
            lab = tk.Label(top, text = element)
            lab.grid(row = 0, column = i + 1)
            i = i + 1
        lab = tk.Label(top, text = avgsz)
        lab.grid(row = 8, column = 1, columnspan = len(t))
        lab = tk.Label(top, text = avgsz1)
        lab.grid(row = 10, column = 1, columnspan = len(t))
        lab = tk.Label(top, text = avgconc)
        lab.grid(row = 12, column = 1, columnspan = len(t))
        lab = tk.Label(top, text = avgconc1)
        lab.grid(row = 14, column = 1, columnspan = len(t))
    elif s == 1 and k == 2:
        r = MSCreadfiles()
        t = MSCcalmax(r)
        m = MSCwavemax(r,t)
        n = MSCcalmin(r)
        rat = MSCratio(r,t,n)
        siz = MSCsize(r,rat)
        avgsz = MSCaveragesize(r,siz)
        conc = MSCconcentration(r,siz,n)
        avgconc = MSCaverageconcentration(r,conc)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Maximum:')
        lab1.grid(row = 1, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at max:')
        lab2.grid(row = 2, column = 0)
        lab3 = tk.Label(top, text = 'Absorbance at 450 nm:')
        lab3.grid(row = 3, column = 0)
        lab4 = tk.Label(top, text = 'Size (nm):')
        lab4.grid(row = 4, column = 0)
        lab5 = tk.Label(top, text = 'Average Size (nm):')
        lab5.grid(row = 5, column = 0)
        lab6 = tk.Label(top, text = 'Concentration (nM):')
        lab6.grid(row = 6, column = 0)
        lab7 = tk.Label(top, text = 'Average concentration (nM):')
        lab7.grid(row = 7, column = 0)
        i = 0
        for element in t:
            lab = tk.Label(top, text = t[element])
            lab.grid(row = 1, column = i + 1)
            i = i + 1
        i = 0
        for element in m:
            lab = tk.Label(top, text = m[element])
            lab.grid(row = 2, column = i + 1)
            i = i + 1
        i = 0
        for element in n:
            lab = tk.Label(top, text = n[element])
            lab.grid(row = 3, column = i + 1)
            i = i + 1
        i = 0
        for element in siz:
            lab = tk.Label(top, text = siz[element])
            lab.grid(row = 4, column = i + 1)
            i = i + 1
        i = 0
        for element in conc:
            lab = tk.Label(top, text = conc[element])
            lab.grid(row = 6, column = i + 1)
            i = i + 1
        i = 0
        for element in hd:
            lab = tk.Label(top, text = element)
            lab.grid(row = 0, column = i + 1)
            i = i + 1
        lab = tk.Label(top, text = avgsz)
        lab.grid(row = 5, column = 1, columnspan = len(t))
        lab = tk.Label(top, text = avgconc)
        lab.grid(row = 7, column = 1, columnspan = len(t))
    elif s == 2 and k == 1:
        r = SSreadfiles()
        numcol = SSnumbercolumns()
        hd = SSheaders()
        sub, cnt, slcnt = SSsubtraction(r)
        t = SScalmax(sub, cnt)
        m = SSwavemax(sub, cnt, t)
        n = SScalmin(sub, slcnt)
        b = SSwavemin(sub, slcnt, n)
        maxR, maxS = SSfindmax(r, hd, m)
        minR, minS = SSfindmin(r, hd, b)
        ratR, ratS = SScalratio(maxR, minR, maxS, minS, hd)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Wavelength at max:')
        lab1.grid(row = 1, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at min:')
        lab2.grid(row = 2, column = 0)
        lab3 = tk.Label(top, text = 'Ratio through ratio method:')
        lab3.grid(row = 4, column = 0)
        lab4 = tk.Label(top, text = 'Ratio through subtraction method:')
        lab4.grid(row = 5, column = 0)
        lab5 = tk.Label(top, text = 'Ratio method')
        lab5.grid(row = 0, column = 1, columnspan = math.ceil((len(hd)/2)))
        lab6 = tk.Label(top, text = 'Subtraction method')
        lab6.grid(row = 0, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in m:
            i = i + 1
            if i == 1:
                lab = tk.Label(top, text = round(m[element]))
                lab.grid(row = 1, column = i, columnspan = math.ceil((len(hd)/2)))
            if i == 2:
                lab = tk.Label(top, text = round(m[element]))
                lab.grid(row = 1, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in b:
            i = i + 1
            if i == 1:
                lab = tk.Label(top, text = round(b[element]))
                lab.grid(row = 2, column = i, columnspan = math.ceil((len(hd)/2)))
            if i == 2:
                lab = tk.Label(top, text = round(b[element]))
                lab.grid(row = 2, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in ratR:
            lab = tk.Label(top, text = ratR[element])
            lab.grid(row = 4, column = i + 1)
            i = i + 1
        i = 0
        for element in ratS:
            lab = tk.Label(top, text = ratS[element])
            lab.grid(row = 5, column = i + 1)
            i = i + 1
        i = 0
        for element in hd:
            lab = tk.Label(top, text = element)
            lab.grid(row = 3, column = i + 1)
            i = i + 1
    elif s == 2 and k == 2:
        r = MSreadfiles()
        t1, t2 = MScalmax()
        m1, m2 = MSwavemax(t1, t2)
        n1, n2 = MScalmin()
        b1, b2 = MSwavemin(n1, n2)
        maxR, maxS = MSfindmax(m1, m2, r)
        minR, minS = MSfindmin(b1, b2, r)
        ratR, ratS = MScalratio(maxR, minR, maxS, minS, r)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Wavelength at max:')
        lab1.grid(row = 1, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at min:')
        lab2.grid(row = 2, column = 0)
        lab3 = tk.Label(top, text = 'Ratio through ratio method:')
        lab3.grid(row = 4, column = 0)
        lab4 = tk.Label(top, text = 'Ratio through subtraction method:')
        lab4.grid(row = 5, column = 0)
        lab5 = tk.Label(top, text = 'Ratio method')
        lab5.grid(row = 0, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab6 = tk.Label(top, text = 'Subtraction method')
        lab6.grid(row = 0, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        lab7 = tk.Label(top, text = round(m1))
        lab7.grid(row = 1, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab8 = tk.Label(top, text = round(m2))
        lab8.grid(row = 1, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        lab9 = tk.Label(top, text = round(b1))
        lab9.grid(row = 2, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab10 = tk.Label(top, text = round(b2))
        lab10.grid(row = 2, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        i = 0
        for element in ratR:
            lab = tk.Label(top, text = ratR[element])
            lab.grid(row = 4, column = i + 1)
            i = i + 1
        i = 0
        for element in ratS:
            lab = tk.Label(top, text = ratS[element])
            lab.grid(row = 5, column = i + 1)
            i = i + 1
        i = 0
        for element in try1:
            lab = tk.Label(top, text = element)
            lab.grid(row = 3, column = i + 1)
            i = i + 1
    elif s == 3 and k == 1:
        r = SSreadfiles()
        numcol = SSnumbercolumns()
        hd = SSheaders()
        sub, cnt, slcnt = SSsubtraction(r)
        t = SScalmax(sub, cnt)
        m = SSwavemax(sub, cnt, t)
        n = SScalmin(sub, slcnt)
        b = SSwavemin(sub, slcnt, n)
        maxR, maxS = SSfindmax(r, hd, m)
        minR, minS = SSfindmin(r, hd, b)
        ratR, ratS = SScalratio(maxR, minR, maxS, minS, hd)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Wavelength at max:')
        lab1.grid(row = 1, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at min:')
        lab2.grid(row = 2, column = 0)
        lab3 = tk.Label(top, text = 'Ratio through ratio method:')
        lab3.grid(row = 4, column = 0)
        lab4 = tk.Label(top, text = 'Ratio through subtraction method:')
        lab4.grid(row = 5, column = 0)
        lab5 = tk.Label(top, text = 'Ratio method')
        lab5.grid(row = 0, column = 1, columnspan = math.ceil((len(hd)/2)))
        lab6 = tk.Label(top, text = 'Subtraction method')
        lab6.grid(row = 0, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in m:
            i = i + 1
            if i == 1:
                lab = tk.Label(top, text = round(m[element]))
                lab.grid(row = 1, column = i, columnspan = math.ceil((len(hd)/2)))
            if i == 2:
                lab = tk.Label(top, text = round(m[element]))
                lab.grid(row = 1, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in b:
            i = i + 1
            if i == 1:
                lab = tk.Label(top, text = round(b[element]))
                lab.grid(row = 2, column = i, columnspan = math.ceil((len(hd)/2)))
            if i == 2:
                lab = tk.Label(top, text = round(b[element]))
                lab.grid(row = 2, column = math.ceil((len(hd)/2)) + 1, columnspan = math.floor((len(hd)/2)))
        i = 0
        for element in ratR:
            lab = tk.Label(top, text = ratR[element])
            lab.grid(row = 4, column = i + 1)
            i = i + 1
        i = 0
        for element in ratS:
            lab = tk.Label(top, text = ratS[element])
            lab.grid(row = 5, column = i + 1)
            i = i + 1
        i = 0
        for element in hd:
            lab = tk.Label(top, text = element)
            lab.grid(row = 3, column = i + 1)
            i = i + 1
    elif s == 3 and k == 2:
        r = MSreadfiles()
        t1, t2 = MScalmax()
        m1, m2 = MSwavemax(t1, t2)
        n1, n2 = MScalmin()
        b1, b2 = MSwavemin(n1, n2)
        maxR, maxS = MSfindmax(m1, m2, r)
        minR, minS = MSfindmin(b1, b2, r)
        ratR, ratS = MScalratio(maxR, minR, maxS, minS, r)
        top = Toplevel()
        top.title('Results')
        top.iconbitmap('c:/users/Dj-AT/desktop/gui/capturar.ico')
        lab1 = tk.Label(top, text = 'Wavelength at max:')
        lab1.grid(row = 1, column = 0)
        lab2 = tk.Label(top, text = 'Wavelength at min:')
        lab2.grid(row = 2, column = 0)
        lab3 = tk.Label(top, text = 'Ratio through ratio method:')
        lab3.grid(row = 4, column = 0)
        lab4 = tk.Label(top, text = 'Ratio through subtraction method:')
        lab4.grid(row = 5, column = 0)
        lab5 = tk.Label(top, text = 'Ratio method')
        lab5.grid(row = 0, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab6 = tk.Label(top, text = 'Subtraction method')
        lab6.grid(row = 0, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        lab7 = tk.Label(top, text = round(m1))
        lab7.grid(row = 1, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab8 = tk.Label(top, text = round(m2))
        lab8.grid(row = 1, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        lab9 = tk.Label(top, text = round(b1))
        lab9.grid(row = 2, column = 1, columnspan = math.ceil((len(try1)/2)))
        lab10 = tk.Label(top, text = round(b2))
        lab10.grid(row = 2, column = math.ceil((len(try1)/2)) + 1, columnspan = math.floor((len(try1)/2)))
        i = 0
        for element in ratR:
            lab = tk.Label(top, text = ratR[element])
            lab.grid(row = 4, column = i + 1)
            i = i + 1
        i = 0
        for element in ratS:
            lab = tk.Label(top, text = ratS[element])
            lab.grid(row = 5, column = i + 1)
            i = i + 1
        i = 0
        for element in try1:
            lab = tk.Label(top, text = element)
            lab.grid(row = 3, column = i + 1)
            i = i + 1

def clicked(number):
    global filename, try2, e1, o1, o2, k
    k = number
    rb1.configure(state = DISABLED)
    rb2.configure(state = DISABLED)
    if s == 1 and number == 1:
        SSCclicked()
    elif s == 1 and number == 2:
        MSCclicked()
    elif s == 2 and number == 1:
        SSclicked()
    elif s == 2 and number == 2:
        MSclicked()
    elif s == 3 and number == 1:
        SCclicked()
    elif s == 3 and number == 2:
        MCclicked()

def clicked1():
    rb3.configure(state = DISABLED)
    rb4.configure(state = DISABLED)
    rb5.configure(state = DISABLED)
    global rb1, rb2, s
    label1 = tk.Label(root, text = 'File type: ')
    label1.grid(row = 1, column = 0)
    rb1 = tk.Radiobutton(root, text = 'csv (1 file)', variable = var1, value = 1, command = lambda: clicked(var1.get()))
    rb1.grid(row = 1, column = 1)
    rb2 = tk.Radiobutton(root, text = 'xlsx (1 or more files)', variable = var1, value = 2, command = lambda: clicked(var1.get()))
    rb2.grid(row = 1, column = 2)
    s = var.get()

def clear():
    global rb3, rb4, rb5, b1
    for widget in root.winfo_children():
        widget.destroy()
    try:
        top.destroy()
        plt.close('all')
        var2.set(0)
        var1.set(0)
        var.set(0)
        v.set('')
        v1.set('')
        v2.set('')
        label2 = tk.Label(root, text = 'Objective: ')
        label2.grid(row = 0, column = 0)
        rb3 = tk.Radiobutton(root, text = 'Size and concentration', variable = var, value = 1, state = NORMAL, command = clicked1)
        rb4 = tk.Radiobutton(root, text = 'Stability Assay', variable = var, value = 2, state = NORMAL, command = clicked1)
        rb5 = tk.Radiobutton(root, text = 'Colorimetric Assay', variable = var, value = 3, state = NORMAL, command = clicked1)
        rb3.grid(row = 0, column = 1)
        rb4.grid(row = 0, column = 2)
        rb5.grid(row = 0, column = 3)
        b1 = tk.Button(root, text = 'Reset', command = clear)
        b1.grid(row = 10, column = 3)
    except:
        plt.close('all')
        var2.set(0)
        var1.set(0)
        var.set(0)
        v.set('')
        v1.set('')
        v2.set('')
        label2 = tk.Label(root, text = 'Objective: ')
        label2.grid(row = 0, column = 0)
        rb3 = tk.Radiobutton(root, text = 'Size and concentration', variable = var, value = 1, state = NORMAL, command = clicked1)
        rb4 = tk.Radiobutton(root, text = 'Stability Assay', variable = var, value = 2, state = NORMAL, command = clicked1)
        rb5 = tk.Radiobutton(root, text = 'Colorimetric Assay', variable = var, value = 3, state = NORMAL, command = clicked1)
        rb3.grid(row = 0, column = 1)
        rb4.grid(row = 0, column = 2)
        rb5.grid(row = 0, column = 3)
        b1 = tk.Button(root, text = 'Reset', command = clear)
        b1.grid(row = 10, column = 3)

var1 = tk.IntVar()
var = tk.IntVar()
var2 = tk.IntVar()
v = tk.StringVar()
v1 = tk.StringVar()
v2 = tk.StringVar()

label2 = tk.Label(root, text = 'Objective: ')
label2.grid(row = 0, column = 0)
rb3 = tk.Radiobutton(root, text = 'Size and concentration', variable = var, value = 1, state = NORMAL, command = clicked1)
rb4 = tk.Radiobutton(root, text = 'Stability Assay', variable = var, value = 2, state = NORMAL, command = clicked1)
rb5 = tk.Radiobutton(root, text = 'Colorimetric Assay', variable = var, value = 3, state = NORMAL, command = clicked1)
rb3.grid(row = 0, column = 1)
rb4.grid(row = 0, column = 2)
rb5.grid(row = 0, column = 3)
b1 = tk.Button(root, text = 'Reset', command = clear)
b1.grid(row = 10, column = 3)

tk.mainloop()
