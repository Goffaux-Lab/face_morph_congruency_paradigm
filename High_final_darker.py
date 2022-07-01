# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:04:04 2020

@author: user
"""


#===============
# Import modules
#===============
import os                    
import numpy as np
import numpy.matlib as npm          # for file/folder operations
import numpy.random as rnd          # for random number generators
import operator
from psychopy import visual, event, core, gui, data, monitors
from numpy import asarray
from PIL import Image, ImageEnhance


#===========================ssss===================
# Settings that we might want to tweak later on
#==============================================
    
datapath = 'data'                   # directory to save data in     
pracpath = 'pracims'
instpath= 'InstScr'
exppath= 'expims'  # directory where images can be found
scramblepath = 'scrambles'
pracscramblepath = 'pracscrambles'
TextVSize = 1


brightness=.5
brightdiv=1/brightness


explength = 768
explength2= explength 
praclength = 96
tottri= praclength/2
tilt = [0,1]
imside=[0,1]


mencxts1 = ['123','125','145','24','2','49','146','7']
mencxts2 = ['44','17','52','160','46','151','147','25']
meneyes=['100_125','38_9','148_66','76_2','93_8','87_146','25_7','147_55']


womcxts1 = ['139','135','192','129','41','20','13','128']
womcxts2 = ['103','197','111','131','65','208','96','225']
womeyes = ['197_135','103_192','216_220','37_94','208_20','65_13','225_128','96_30']
    
praccxt1= ['223','209','78','203','224','226']
praccxt2= ['21','154','214','37','31','106']
praceyes=['154_209','21_78','37_203','214_224','106_226','31_163']
pracmorphs=['10','18','24','32','38','50','62','68','77','82','90']
morphs=['10','18','24','32','38','50','62','68','77','82','90']


# 0% dissimilarity pairs: 
# 24% dissimilarity pairs: 38-62
# 36% dissimilarity pairs: 32-68
# 53% dissimilarity pairs: 24-77
# 80% dissimilarity pairs: 10-90

praclist=[]
       
imlistwom = [] 
imlistmen = []                       # image names without the suffixes
asfx = '.png'                      # suffix for the image
timelimit = 3           # image freezing time in seconds

IBW=3 #the wait between the blocks
#IBW=0.1
ISI = [.7, .8, .9, 1, 1.1, 1.2]
#ISI=[.01, .02]
FixT = 500
IntT = 500
TargetT = 500
MaskT = 200


#========================================
# Store info about the experiment session
#========================================
    
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Discriminability and Congruency'
exp_info = {
        'participant': '',
        'gender': ('male', 'female'),
        'age':'',
        'screenwidth(cm)': '59',
        'screenresolutionhori(pixels)': '1920',
        'screenresolutionvert(pixels)': '1080',
        'refreshrate(hz)': '60'
        }

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)
    
    #========================
    # Prepare condition lists
    #========================
    
#Check if all images exist
for cxt1, cxt2, eyes in zip(mencxts1, mencxts2,meneyes):
    for morph in morphs:
        if (not os.path.exists(os.path.join(exppath, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(exppath, cxt2+'-'+eyes+'-'+morph+asfx))):
            raise Exception('Image files not found in image folder: ' + str(cxt1+'-'+eyes+'-'+morph+asfx) + ' or ' + str(cxt2+'-'+eyes+'-'+morph+asfx))
        if not os.path.exists(os.path.join(exppath, eyes+'-'+morph+asfx)):
            raise Exception('Image files not found in image folder: ' + str(eyes+'-'+morph+asfx))           
    
for cxt1, cxt2, eyes in zip(womcxts1, womcxts2,womeyes):
    for morph in morphs:
        if (not os.path.exists(os.path.join(exppath, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(exppath, cxt2+'-'+eyes+'-'+morph+asfx))):
            raise Exception('Image files not found in image folder: ' + str(cxt1+'-'+eyes+'-'+morph+asfx) + ' or ' + str(cxt2+'-'+eyes+'-'+morph+asfx))
        if not os.path.exists(os.path.join(exppath, eyes+'-'+morph+asfx)):
            raise Exception('Image files not found in image folder: ' + str(eyes+'-'+morph+asfx))
#            
for cxt1, cxt2, eyes in zip(praccxt1,praccxt2,praceyes):
    for morph in pracmorphs:
        if (not os.path.exists(os.path.join(pracpath, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(pracpath, cxt2+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(pracpath, eyes+'-'+morph+asfx))):
            raise Exception('Image file not found in image folder:' + str(cxt1+'-'+eyes+'-'+morph+asfx))
#                
    
    
    # Randomize the image order
rnd.shuffle(imlistmen)



    
mon = monitors.Monitor('Dell')
mon.setDistance(57)

mon.setWidth(float(exp_info['screenwidth(cm)']))
horipix = exp_info['screenresolutionhori(pixels)']
vertpix = exp_info['screenresolutionvert(pixels)']
framerate = exp_info['refreshrate(hz)']
scrsize = (float(horipix),float(vertpix))


framelength = 1000/(float(framerate))

FixFrame = int(FixT/framelength)
IntFrame = int(IntT/framelength)
ImFrame = int(TargetT/framelength)
MaskFrame = int(MaskT/framelength)



mon.setSizePix(scrsize)

    # Open a window
    
win = visual.Window(monitor = mon, 
                    size = scrsize,
                    color=(-(1-brightness),-(1-brightness),-(1-brightness)),
                    units='deg',
                    fullscr=True)
win.mouseVisible=False

#frameRate = win.getActualFrameRate()
#print('framerate is', frameRate)


bitmapinst = visual.ImageStim(win,interpolate=True,units='norm', size=[1.5,1.5])
    # Define trial start text



empty_scr = visual.TextStim(win,
                            text="Por.",
                                    color='black', height=20)
    # Define bitmap stimulus (contents can still change)
    
    #they are 8.38 vertically, but actually when you calculate depending 
    # on head size vertically, the faces subtend a visual angle of 7 degrees.
    #image size is different than average head size.
    
bitmap1 = visual.ImageStim(win, size=[7.05,8.38], interpolate=True) 
bitmap2 = visual.ImageStim(win, size=[7.05,8.38], interpolate=True)
bitmap3 = visual.ImageStim(win, size=[7.05,8.38])
bitmap4 = visual.ImageStim(win, size=[7.05,8.38])
bitmap5 = visual.ImageStim(win, size=[7.05,8.38])
bitmap6 = visual.ImageStim(win, size=[7.05,8.38])
bitmap7 = visual.ImageStim(win, size=[7.05,8.38])
bitmap8 = visual.ImageStim(win, size=[7.05,8.38])
bitmap9 = visual.ImageStim(win, size=[7.05,8.38])
bitmap10 = visual.ImageStim(win, size=[7.05,8.38])
bitmap11 = visual.ImageStim(win, size=[7.05,8.38])
bitmap12 = visual.ImageStim(win, size=[7.05,8.38])
bitmap13 = visual.ImageStim(win, size=[7.05,8.38])
bitmap14 = visual.ImageStim(win, size=[7.05,8.38])
bitmap15 = visual.ImageStim(win, size=[7.05,8.38])
bitmap16 = visual.ImageStim(win, size=[7.05,8.38])
maskmap = visual.ImageStim(win, size=[7.05,8.38], interpolate=True)

    
    #==========================
    # Define the trial sequence
    #==========================
    
    # Define a list of trials with their properties:
    #   - Which image (without the suffix)
    #   - Which orientation
stim_order = []
    
    
morph1=npm.repmat((38, 32, 24, 10),1,int(len(praceyes)))

morph2=npm.repmat([62, 68, 77, 90],1,int(len(praceyes)))

morph31=npm.repmat([10, 24, 32, 38],1,int(len(praceyes)/2))
morph32=npm.repmat([62, 68, 77, 90],1,int(len(praceyes)/2))
morph3=np.append(morph31,morph32)
    
morph41=npm.repmat([62, 68, 77, 90],1,int(len(praceyes)/2))
morph42=npm.repmat([10, 24, 32, 38],1,int(len(praceyes)/2))
morph4=np.append(morph41,morph42)
    
morph51=npm.repmat([10, 32, 62, 77],1,int(len(praceyes)/2))
morph52=npm.repmat([24, 38, 68, 90],1,int(len(praceyes)/2))
morph5=np.append(morph51,morph52)
    
i=0
pracdiffdiff = []
pracdiffsame=[]
pracsamediff=[]
pracsamesame=[]
pracisodiff=[]
pracisosame=[]
ori= [0,180]
for cxt1, cxt2, eyes in zip(praccxt1, praccxt2, praceyes):
    for itr in np.arange(4):
        pracdiffdiff.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[0][i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[0][i])+asfx), 'dissim': abs(morph1[0][i]-morph2[0][i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[0][i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[0][i])+'mask'+asfx)})
        pracdiffsame.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx)})
        pracsamediff.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[0][i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[0][i])+asfx), 'dissim': abs(morph1[0][i]-morph2[0][i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[0][i])+'mask'+asfx), 'mask2': str(cxt1+'-'+eyes+'-'+str(morph2[0][i])+'mask'+asfx)})
        pracsamesame.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx), 'mask2': str(cxt1+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx)})
        pracisodiff.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[0][i])+asfx), 'im2': str(eyes+'-'+str(morph2[0][i])+asfx), 'dissim': abs(morph1[0][i]-morph2[0][i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[0][i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[0][i])+'mask'+asfx)})
        pracisosame.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph5[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph5[i])+'mask'+asfx)})
        i=i+1
    
pddmat24=[]
pddmat36=[]
pddmat53=[]
pddmat80=[]
psdmat24=[]
psdmat36=[]
psdmat53=[]
psdmat80=[]
pisodmat24=[]
pisodmat36=[]
pisodmat53=[]
pisodmat80=[]
    
for j in np.arange(len(pracdiffdiff)):
    if pracdiffdiff[j]['dissim'] == 24:
        pddmat24.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 36:
        pddmat36.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 53:
        pddmat53.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 80:
        pddmat80.append(pracdiffdiff[j])
            
for j in np.arange(len(pracsamediff)):
    if pracsamediff[j]['dissim'] == 24:
        psdmat24.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 36:
        psdmat36.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 53:
        psdmat53.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 80:
        psdmat80.append(pracsamediff[j])
            
for j in np.arange(len(pracisodiff)):
    if pracisodiff[j]['dissim'] == 24:
        pisodmat24.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 36:
        pisodmat36.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 53:
        pisodmat53.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 80:
        pisodmat80.append(pracisodiff[j])
            
rnd.shuffle(pddmat24)
rnd.shuffle(pddmat36)
rnd.shuffle(pddmat53)
rnd.shuffle(pddmat80)
rnd.shuffle(psdmat24)
rnd.shuffle(psdmat36)
rnd.shuffle(psdmat53)
rnd.shuffle(psdmat80)
rnd.shuffle(pisodmat24)
rnd.shuffle(pisodmat36)
rnd.shuffle(pisodmat53)
rnd.shuffle(pisodmat80)
rnd.shuffle(pracdiffsame)
rnd.shuffle(pracsamesame)
rnd.shuffle(pracisosame)

    
adr=0
practrials=[]
for adder in np.arange(tottri/24):
    slcr=slice(adr*4,(adr*4)+4,1)
        
    practrials.append(pddmat24[adr])
    practrials.append(pddmat36[adr])
    practrials.append(pddmat53[adr])
    practrials.append(pddmat80[adr])
    practrials.extend(pracdiffsame[slcr])
        
    practrials.append(psdmat24[adr])
    practrials.append(psdmat36[adr])
    practrials.append(psdmat53[adr])
    practrials.append(psdmat80[adr])
    practrials.extend(pracsamesame[slcr])
        
    practrials.append(pisodmat24[adr])
    practrials.append(pisodmat36[adr])
    practrials.append(pisodmat53[adr])
    practrials.append(pisodmat80[adr])
    practrials.extend(pracisosame[slcr])
    adr=adr+1


import copy
p1 = copy.deepcopy(practrials)
    
for ind in range(0,int(len(practrials))):
        practrials[ind].update(ori=0)
for ind in range(0, int(len(p1))):
        p1[ind].update(ori=180)
        
p2 = practrials + p1
    

p2.sort(key=operator.itemgetter('dissim'))

pracordtrials1=[]
slcr=slice(0,int(len(p2)/2),1)
pracordtrials1.extend(p2[slcr])

pracordtrials2=[]
slcr2=slice(int(len(p2)/2),len(p2),1)
pracordtrials2.extend(p2[slcr2])

rnd.shuffle(pracordtrials1)
rnd.shuffle(pracordtrials2)

pracnewtrials=[]
# This is where we take equal number of same and diff trials and put them in a 
# new list.
for indx in np.arange(0,int(len(p2)/2),3):
    slcr=slice(indx,indx+3,1)
    pracnewtrials.extend(pracordtrials1[slcr])
    pracnewtrials.extend(pracordtrials2[slcr])

pracnewtrials2=[]
for indx in np.arange(0,len(p2),6):
    slcr=slice(indx,indx+6,1)
    pp=pracnewtrials[slcr]
    rnd.shuffle(pp)
    pracnewtrials2.extend(pp)
    

pp2= pracnewtrials2
prtrials = data.TrialHandler(pp2, nReps=1, method='sequential', originPath=datapath)


morph1=[]
morph2=[]
morph3=[]
morph4=[]
morph5=[]



morph11=npm.repmat([38, 32, 24, 10],1,int(len(meneyes)/4))
morph12=npm.repmat([32, 24, 10, 38],1,int(len(meneyes)/4))
morph13=npm.repmat([24, 10, 38, 32],1,int(len(meneyes)/4))
morph14=npm.repmat([10, 38, 32, 24],1,int(len(meneyes)/4))

morph1=np.append(morph11,morph12)
morph1=np.append(morph1, morph13)
morph1=np.append(morph1, morph14)

morph21=npm.repmat([62, 68, 77, 90],1,int(len(meneyes)/4))
morph22=npm.repmat([68, 77, 90, 62],1,int(len(meneyes)/4))
morph23=npm.repmat([77, 90, 62, 68],1,int(len(meneyes)/4))
morph24=npm.repmat([90, 62, 68, 77],1,int(len(meneyes)/4))
morph2=np.append(morph21,morph22)
morph2=np.append(morph2, morph23)
morph2=np.append(morph2, morph24)
    

morph31=npm.repmat([10, 32, 62, 77],1,int(len(meneyes)/4))
morph32=npm.repmat([77, 10, 32, 62],1,int(len(meneyes)/4))
morph33=npm.repmat([62, 77, 10, 32],1,int(len(meneyes)/4))
morph34=npm.repmat([32, 62, 77, 10],1,int(len(meneyes)/4))

morph3=np.append(morph31, morph32)
morph31=np.append(morph33, morph34)
morph3=np.append(morph3, morph31)


morph41=npm.repmat([77, 10, 32, 62],1,int(len(meneyes)/4))
morph42=npm.repmat([62, 77, 10, 32],1,int(len(meneyes)/4))
morph43=npm.repmat([32, 62, 77, 10],1,int(len(meneyes)/4))
morph44=npm.repmat([10, 32, 62, 77],1,int(len(meneyes)/4))


morph4=np.append(morph41, morph42)
morph41=np.append(morph43, morph44)
morph4=np.append(morph4, morph41)

morph51=npm.repmat([62, 77, 10, 32],1,int(len(meneyes)/4))
morph52=npm.repmat([77, 10, 32, 62],1,int(len(meneyes)/4))
morph53=npm.repmat([10, 32, 62, 77],1,int(len(meneyes)/4))
morph54=npm.repmat([32, 62, 77, 10],1,int(len(meneyes)/4))

morph5=np.append(morph51, morph52)
morph51=np.append(morph53, morph54)
morph5=np.append(morph5, morph51)

expdiffdiffmen=[]
expdiffsamemen=[]
expsamediffmen=[]
expsamesamemen=[]
expisodiffmen=[]
expisosamemen=[]


i=0
for cxt1, cxt2, eyes in zip(mencxts1, mencxts2, meneyes):
    for itr in np.arange(4):
        expdiffdiffmen.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+'mask'+asfx), 'tno': i})
        expdiffsamemen.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i]), 'pair': str(morph3[i])+'-'+str(morph3[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'tno': i})
        expsamediffmen.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+'mask'+asfx), 'mask2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+'mask'+asfx), 'tno': i})
        expsamesamemen.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i]), 'pair': str(morph4[i])+'-'+str(morph4[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx), 'tno': i})
        expisodiffmen.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+'mask'+asfx), 'tno': i})
        expisosamemen.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i]), 'pair': str(morph5[i])+'-'+str(morph5[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'tno': i})
        i+=1

expdiffdiffwom = []
expdiffsamewom=[]
expsamediffwom=[]
expsamesamewom=[]
expisodiffwom=[]
expisosamewom=[]

i=0

for cxt1, cxt2, eyes in zip(womcxts1, womcxts2, womeyes):
    for itr in np.arange(4):
        expdiffdiffwom.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+'mask'+asfx), 'tno': i})
        expdiffsamewom.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i]), 'pair': str(morph3[i])+'-'+str(morph3[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'tno': i})
        expsamediffwom.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'tno': i})
        expsamesamewom.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i]), 'pair': str(morph4[i])+'-'+str(morph4[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph4[i])+'mask'+asfx), 'tno': i})
        expisodiffwom.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i]), 'pair': str(morph1[i])+'-'+str(morph2[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+'mask'+asfx), 'tno': i})
        expisosamewom.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i]), 'pair': str(morph5[i])+'-'+str(morph5[i]), 'mask1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'mask2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+'mask'+asfx), 'tno': i})
        i+=1
    
eddmen24=[]
eddwom24=[]
eddmen36=[]
eddwom36=[]
eddmen53=[]
eddwom53=[]
eddmen80=[]
eddwom80=[]
esdmen24=[]
esdwom24=[]
esdmen36=[]
esdwom36=[]
esdmen53=[]
esdwom53=[]
esdmen80=[]
esdwom80=[]
eisodmen24=[]
eisodwom24=[]
eisodmen36=[]
eisodwom36=[]
eisodmen53=[]
eisodwom53=[]
eisodmen80=[]
eisodwom80=[]
    
for j in np.arange(len(expdiffdiffmen)):
    if expdiffdiffmen[j]['dissim'] == 24:
        eddmen24.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 36:
        eddmen36.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 53:
        eddmen53.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 80:
        eddmen80.append(expdiffdiffmen[j])
        
for j in np.arange(len(expdiffdiffwom)):
    if expdiffdiffwom[j]['dissim'] == 24:
        eddwom24.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 36:
        eddwom36.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 53:
        eddwom53.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 80:
        eddwom80.append(expdiffdiffwom[j])
            
for j in np.arange(len(expsamediffmen)):
    if expsamediffmen[j]['dissim'] == 24:
        esdmen24.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 36:
        esdmen36.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 53:
        esdmen53.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 80:
        esdmen80.append(expsamediffmen[j])
for j in np.arange(len(expsamediffwom)):
    if expsamediffwom[j]['dissim'] == 24:
        esdwom24.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 36:
        esdwom36.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 53:
        esdwom53.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 80:
        esdwom80.append(expsamediffwom[j])
for j in np.arange(len(expisodiffmen)):
    if expisodiffmen[j]['dissim'] == 24:
        eisodmen24.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 36:
        eisodmen36.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 53:
        eisodmen53.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 80:
        eisodmen80.append(expisodiffmen[j])
for j in np.arange(len(expisodiffwom)):
    if expisodiffwom[j]['dissim'] == 24:
        eisodwom24.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 36:
        eisodwom36.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 53:
        eisodwom53.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 80:
        eisodwom80.append(expisodiffwom[j])
            
rnd.shuffle(eddmen24)
rnd.shuffle(eddwom24)
rnd.shuffle(eddmen36)
rnd.shuffle(eddwom36)
rnd.shuffle(eddmen53)
rnd.shuffle(eddwom53)
rnd.shuffle(eddmen80)
rnd.shuffle(eddwom80)
rnd.shuffle(esdmen24)
rnd.shuffle(esdwom24)
rnd.shuffle(esdmen36)
rnd.shuffle(esdwom36)
rnd.shuffle(esdmen53)
rnd.shuffle(esdwom53)
rnd.shuffle(esdmen80)
rnd.shuffle(esdwom80)
rnd.shuffle(eisodmen24)
rnd.shuffle(eisodwom24)
rnd.shuffle(eisodmen36)
rnd.shuffle(eisodwom36)
rnd.shuffle(eisodmen53)
rnd.shuffle(eisodwom53)
rnd.shuffle(eisodmen80)
rnd.shuffle(eisodwom80)
rnd.shuffle(expdiffsamemen)
rnd.shuffle(expdiffsamewom)
rnd.shuffle(expsamesamemen)
rnd.shuffle(expsamesamewom)
rnd.shuffle(expisosamemen)
rnd.shuffle(expisosamewom)

    
adr=0
exptrials=[]
for adder in np.arange(explength2/96):
    slcr=slice(adr*4,(adr*4)+4,1)
    
    
    
    exptrials.append(eddmen24[adr])
    exptrials.append(eddmen36[adr])
    exptrials.append(eddmen53[adr])
    exptrials.append(eddmen80[adr])
    exptrials.extend(expdiffsamemen[slcr])
    exptrials.append(eddwom24[adr])
    exptrials.append(eddwom36[adr])
    exptrials.append(eddwom53[adr])
    exptrials.append(eddwom80[adr])
    exptrials.extend(expdiffsamewom[slcr])
        
    exptrials.append(esdmen24[adr])
    exptrials.append(esdmen36[adr])
    exptrials.append(esdmen53[adr])
    exptrials.append(esdmen80[adr])
    exptrials.extend(expsamesamemen[slcr])
    exptrials.append(esdwom24[adr])
    exptrials.append(esdwom36[adr])
    exptrials.append(esdwom53[adr])
    exptrials.append(esdwom80[adr])
    exptrials.extend(expsamesamewom[slcr])
        
    exptrials.append(eisodmen24[adr])
    exptrials.append(eisodmen36[adr])
    exptrials.append(eisodmen53[adr])
    exptrials.append(eisodmen80[adr])
    exptrials.extend(expisosamemen[slcr])
    exptrials.append(eisodwom24[adr])
    exptrials.append(eisodwom36[adr])
    exptrials.append(eisodwom53[adr])
    exptrials.append(eisodwom80[adr])
    exptrials.extend(expisosamewom[slcr])
    adr=adr+1


e1 = copy.deepcopy(exptrials)
    
for ind in range(0,int(len(exptrials))):
        exptrials[ind].update(ori=0)
for ind in range(0, int(len(e1))):
        e1[ind].update(ori=180)
        
e2 = exptrials + e1


e2.sort(key=operator.itemgetter('dissim'))

ordtrials1=[]
slcr=slice(0,int(len(e2)/2),1)
ordtrials1.extend(e2[slcr])

ordtrials2=[]
slcr2=slice(int(len(e2)/2),len(e2),1)
ordtrials2.extend(e2[slcr2])

rnd.shuffle(ordtrials1)
rnd.shuffle(ordtrials2)

ord1iso0=[]
ord1iso1=[]
ord1cong0=[]
ord1cong1=[]
ord1inc0=[]
ord1inc1=[]

for i in np.arange(0,len(ordtrials1)):
    if ordtrials1[i]['cond'] == 'ISOS' and ordtrials1[i]['ori'] == 0:
        ord1iso0.append(ordtrials1[i])
    elif ordtrials1[i]['cond'] == 'ISOS' and ordtrials1[i]['ori'] == 180:
        ord1iso1.append(ordtrials1[i])
    elif ordtrials1[i]['cond'] == 'SS' and ordtrials1[i]['ori'] == 0:
        ord1cong0.append(ordtrials1[i])
    elif ordtrials1[i]['cond'] == 'SS' and ordtrials1[i]['ori'] == 180:
        ord1cong1.append(ordtrials1[i])
    elif ordtrials1[i]['cond'] == 'DS' and ordtrials1[i]['ori'] == 0:
        ord1inc0.append(ordtrials1[i])
    elif ordtrials1[i]['cond'] == 'DS' and ordtrials1[i]['ori'] == 180:
        ord1inc1.append(ordtrials1[i])
        
for i in np.arange(0,len(ordtrials1)):
    if ordtrials1[i]['cond'] == 'DS'and ordtrials1[i]['ori'] == 0:
        ord1inc0.append(ordtrials1[i])
        
        
ord24iso0=[]
ord24iso1=[]
ord24cong0=[]
ord24cong1=[]
ord24inc0=[]
ord24inc1=[]

ord36iso0=[]
ord36iso1=[]
ord36cong0=[]
ord36cong1=[]
ord36inc0=[]
ord36inc1=[]

ord53iso0=[]
ord53iso1=[]
ord53cong0=[]
ord53cong1=[]
ord53inc0=[]
ord53inc1=[]

ord80iso0=[]
ord80iso1=[]
ord80cong0=[]
ord80cong1=[]
ord80inc0=[]
ord80inc1=[]

for i in np.arange(0,len(ordtrials2)):
    if ordtrials2[i]['dissim'] == 24:
        if ordtrials2[i]['ori'] == 0:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord24iso0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord24cong0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord24inc0.append(ordtrials2[i])
        else:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord24iso1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord24cong1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord24inc1.append(ordtrials2[i])
    if ordtrials2[i]['dissim'] == 36:
        if ordtrials2[i]['ori'] == 0:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord36iso0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord36cong0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord36inc0.append(ordtrials2[i])
        else:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord36iso1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord36cong1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord36inc1.append(ordtrials2[i])
    if ordtrials2[i]['dissim'] == 53:
        if ordtrials2[i]['ori'] == 0:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord53iso0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord53cong0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord53inc0.append(ordtrials2[i])
        else:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord53iso1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord53cong1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord53inc1.append(ordtrials2[i])
    if ordtrials2[i]['dissim'] == 80:
        if ordtrials2[i]['ori'] == 0:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord80iso0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord80cong0.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord80inc0.append(ordtrials2[i])
        else:
            if ordtrials2[i]['cond'] == 'ISOD':
                ord80iso1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'DD':
                ord80cong1.append(ordtrials2[i])
            elif ordtrials2[i]['cond'] == 'SD':
                ord80inc1.append(ordtrials2[i])
    
                
            
                

newtrials=[]
# This is where we take equal number of same and diff trials and put them in a 
# new list.


adr=0
for indx in np.arange(0,16):
    
    slcr=slice(adr*4,(adr*4)+4,1)
   
    newtrials.extend(ord1iso0[slcr])
    newtrials.extend(ord1iso1[slcr])
    newtrials.extend(ord1inc0[slcr])
    newtrials.extend(ord1inc1[slcr])
    newtrials.extend(ord1cong0[slcr])
    newtrials.extend(ord1cong1[slcr])

    newtrials.append(ord24iso0[indx])
    newtrials.append(ord24iso1[indx])
    newtrials.append(ord24inc0[indx])
    newtrials.append(ord24inc1[indx])
    newtrials.append(ord24cong0[indx])
    newtrials.append(ord24cong1[indx])

    newtrials.append(ord36iso0[indx])
    newtrials.append(ord36iso1[indx])
    newtrials.append(ord36inc0[indx])
    newtrials.append(ord36inc1[indx])
    newtrials.append(ord36cong0[indx])
    newtrials.append(ord36cong1[indx])

    newtrials.append(ord53iso0[indx])
    newtrials.append(ord53iso1[indx])
    newtrials.append(ord53inc0[indx])
    newtrials.append(ord53inc1[indx])
    newtrials.append(ord53cong0[indx])
    newtrials.append(ord53cong1[indx])

    newtrials.append(ord80iso0[indx])
    newtrials.append(ord80iso1[indx])
    newtrials.append(ord80inc0[indx])
    newtrials.append(ord80inc1[indx])
    newtrials.append(ord80cong0[indx])
    newtrials.append(ord80cong1[indx])
    adr+=1



# This part shuffles every 36 within itself.
newtrials2=[]
for indx in np.arange(0,len(e2),48):
    slcr=slice(indx,indx+48,1)
    a=newtrials[slcr]
    rnd.shuffle(a)
    newtrials2.extend(a)

fintrials = copy.deepcopy(newtrials2)
    
ttno=0
for ind in range(int(len(fintrials))):
        fintrials[ttno].update(ttno=ttno)
        ttno+=1
        
        
# creating two sessions.
ses1=[]
slcr3=slice(0,int(len(fintrials)/2),1)
ses1.extend(fintrials[slcr3])


ses2=[]
slcr4=slice(int(len(fintrials)/2),len(fintrials),1)
ses2.extend(fintrials[slcr4])

import pickle

trials_fname = exp_info['participant'] + '_' + 'trials'
trials_fname = os.path.join(datapath, trials_fname)
pickle_fname = exp_info['participant'] + '-' + 'pickle'
pickle_fname = os.path.join(datapath, pickle_fname)
subinfo_fname = exp_info['participant'] + '-' + 'subinfo'
subinfo_fname = os.path.join(datapath, subinfo_fname)
pickled=False

if os.path.exists(pickle_fname):
    pickled=True
    print('pickled')


if not pickled: 
    print('unpickled, pickling now')
    with open(trials_fname, 'wb') as pickle_file:
        pickle.dump([fintrials], pickle_file)
    with open(pickle_fname, 'wb') as pickle_file2:
        pickle.dump([pickled], pickle_file2)
    with open(subinfo_fname, 'wb') as pickle_file3:
        pickle.dump([exp_info], pickle_file3)
    exTrials = data.TrialHandler(ses1, nReps=1, method='sequential', originPath=datapath)
    print('ses1')
        
else:    
    with open(trials_fname, 'rb') as pickle_file:
        fintrials=pickle.load(pickle_file)
        fintrials=fintrials[0][:]
    with open(pickle_fname, 'rb') as pickle_file2:
        pickled=pickle.load(pickle_file2)
        
    ses2=[]
    slcr4=slice(int(len(fintrials)/2),len(fintrials),1)
    ses2.extend(fintrials[slcr4])
    exTrials= data.TrialHandler(ses2, nReps=1, method='sequential', originPath=datapath)
    


    
#=====================
# Start the experiment
#=====================

# Initialize two clocks:
#   - for image change time
#   - for response time
change_clock = core.Clock()
rt_clock = core.Clock()

trialCount=0
training=0
trainingAccTot=0
trainingAccBlock=0


pracCount=0
pracDone=0
pracblockno=1
# Run through the trials PRACTICE


for trial in prtrials:
    pracCount=pracCount+1
    # Display trial start text
    if pracCount == 1:
        
        ##Instruction Screen 1: Before starting, make sure to find ...
        inst1_imname=os.path.join(instpath, 'instscr1.png')
        inst1=Image.open(inst1_imname)
        enh1=ImageEnhance.Brightness(inst1)
        inst1_end=enh1.enhance(brightness)
        bitmapinst.setImage(inst1_end)
        bitmapinst.draw()

        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 2: In this experiment, pictures of faces ...
        inst2_imname=os.path.join(instpath, 'instscr2.png')
                
        inst2=Image.open(inst2_imname)
        enh1=ImageEnhance.Brightness(inst2)
        inst2_end=enh1.enhance(brightness)
        bitmapinst.setImage(inst2_end)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        
        
        ##Instruction Screen 6: The task is difficult since...
        inst5_imname=os.path.join(instpath, 'instscr5.png')
        bitmapinst.setImage(inst5_imname)
        
        inst5=Image.open(inst5_imname)
        enh1=ImageEnhance.Brightness(inst5)
        inst5_end=enh1.enhance(brightness)
        bitmapinst.setImage(inst5_end)
        
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 7: IDENTICAL eyes = "S", DIFFERENT...
        inst6_imname=os.path.join(instpath, 'instscr6.png')
        inst6=Image.open(inst6_imname)
        enh1=ImageEnhance.Brightness(inst6)
        inst6_end=enh1.enhance(brightness)
        bitmapinst.setImage(inst6_end)

        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        
     
        
            # Set the images
    im1_fname = os.path.join(pracpath, trial['im1'])
    im2_fname = os.path.join(pracpath, trial['im2'])
    mask1_fname = os.path.join(pracscramblepath, trial['mask1'])
    mask2_fname = os.path.join(pracscramblepath, trial['mask2'])
    
    im1=Image.open(im1_fname)
    im2=Image.open(im2_fname)
    enh1=ImageEnhance.Brightness(im1)
    enh2=ImageEnhance.Brightness(im2)
    
    im1_end=enh1.enhance(brightness)
    im2_end=enh2.enhance(brightness)
                
    rnd.shuffle(imside)
    if imside[1] == 0:
        bitmap1.setImage(im1_end)
        bitmap2.setImage(im2_end)
        maskim=Image.open(mask1_fname)
        
    else:
        bitmap1.setImage(im2_end)
        bitmap2.setImage(im1_end)
        maskim=Image.open(mask2_fname)
    
    maskend=asarray(maskim)
    maskend=maskend/256
    maskend=maskend/brightdiv
    masking=Image.fromarray(maskend)
    
    
    maskmap.setImage(masking)
    
    
    
    bitmap1.setOri(trial['ori'])
    bitmap2.setOri(trial['ori'])
    maskmap.setOri(trial['ori'])

    maskmap.setOri(trial['ori'])
    if trial['ori'] == 0:
        eyeleveling=-1.18
    else:
        eyeleveling=1.18

    
    fixation = visual.ShapeStim(win, 
    vertices=((0, -0.3), (0, 0.3), (0,0), (-0.3,0), (0.3, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor="black"
    )


    bitmap1.pos=(0,eyeleveling) #142+284/2 (5.1 is equal to 142 pixels, then we add half of the horizontal size (7/2) because pos. takes the center to the defined location.)
    
    bitmap2.pos=(0,eyeleveling)
    
    maskmap.pos = (0,eyeleveling)

                                
    bitmap1.size=(7.05,8.38)
    bitmap2.size=(7.05,8.38)  
    maskmap.size=(7.05,8.38)
    
   
    for nFrames in range(FixFrame): # 600 ms.
        fixation.draw()
        win.flip()
#    
        
    for nFrames in range(IntFrame):  # 500 ms
        win.flip()
    
    
    for nFrames in range(ImFrame): # 300 ms
        bitmap1.draw()
        win.flip()
        
    
    for nFrames in range(MaskFrame): # 200 ms
        maskmap.draw()
        win.flip()
    
    bitmap2.draw()
    win.flip()
    change_clock.reset()
    rt_clock.reset()
                                
    # Wait until a response, or until time limit.
    #keys = event.waitKeys(maxWait=timelimit, keyList=['s','l', 'escape'])
         
    keys = event.waitKeys(keyList=['s','l','escape','p'])     
    # If a key is pressed, take the reaction time. If not, just remove the images from the screen    
    if keys:
        rt = rt_clock.getTime()
        
    #fixation.clearTextures()
    bitmap1.clearTextures()
    bitmap2.clearTextures()
    win.flip()
                                    
        #At this point, there are still no keys pressed. So "if not keys" is definitely 
        #going to be processed.
        #After removing the images from the screen, still listening for a keypress. 
        #Record the reaction time if a key is pressed.
                                    
    if not keys:
        keys = event.waitKeys(keyList=['s','l','escape','p'])
        rt = rt_clock.getTime()
                                        
        #If the key is pressed analyze the keypress.
    if keys:
        if 'escape' in keys:
            break
        elif 'p' in keys:
            pracDone=1
            break
        elif 's' in keys and trial['dissim'] == 0: #left is same
            acc = 1
        elif 'l' in keys and not trial['dissim'] == 0: #right is different
            acc = 1
        #elif 't' in keys:
            #pracDone=1
            #break
        else:
            acc = 0
                                                        
    trainingAccTot=trainingAccTot+acc
    trainingAccBlock=trainingAccBlock+acc
                                                        
               
    win.setColor(color=(-(1-brightness),-(1-brightness),-(1-brightness)))
    win.flip()
    event.clearEvents()
    prtrials.addData('rt', rt)
    prtrials.addData('acc', acc)
    rnd.shuffle(ISI)
    core.wait(ISI[1])
                                         
    if pracCount%24 == 0 and not pracCount == len(pp2):
        blockPerc=trainingAccBlock/24*100
        if blockPerc < 65:
            inst1_fbname=os.path.join(instpath, 'expscr3.png')
        elif blockPerc >=65:
            inst1_fbname=os.path.join(instpath, 'expscr1.png')
        
        instfb=Image.open(inst1_fbname)
        enh1=ImageEnhance.Brightness(instfb)
        instfb_end=enh1.enhance(brightness)
        bitmapinst.setImage(instfb_end)
        bitmapinst.draw()
        win.flip()
        
    
        trainingAccBlock=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()
        if 'escape' in keys:
            win.flip()
            break
        elif 'space' in keys:
            keys = []
            event.clearEvents()
            win.flip()
        core.wait(IBW)

        
        
        
    elif pracCount == len(pp2):
        totPerc=trainingAccTot/len(pp2)*100;
        if totPerc > 65:
            inst1_fbname=os.path.join(instpath, 'pracacc1.png')

            instfb=Image.open(inst1_fbname)
            enh1=ImageEnhance.Brightness(instfb)
            instfb_end=enh1.enhance(brightness)
            bitmapinst.setImage(instfb_end)
            bitmapinst.draw()

            win.flip()
            keys = event.waitKeys(keyList=['t','escape'])
            if 'escape' in keys:
                win.setColor(color=(-(1-brightness),-(1-brightness),-(1-brightness)))
                win.flip()
                win.flip()
                break
            elif 't' in keys:
                keys = []
                event.clearEvents()
            pracDone=1
            core.wait(.2)
            
        elif totPerc <= 65:
            inst1_fbname=os.path.join(instpath, 'pracacc2.png')

            instfb=Image.open(inst1_fbname)
            enh1=ImageEnhance.Brightness(instfb)
            instfb_end=enh1.enhance(brightness)
            bitmapinst.setImage(instfb_end)
            bitmapinst.draw()
            win.flip()
            keys = event.waitKeys(keyList=['escape'])                                                      
            if 'escape' in keys:
                win.setColor(color=(-(1-brightness),-(1-brightness),-(1-brightness)))
                win.flip()
                win.flip()
                break
            elif 't' in keys:
                keys = []
                event.clearEvents()
            pracDone=1
            core.wait(.2)

            core.wait(.2)
                # Add the current trial's data to the TrialHandler
    
                # Advance to the next trial
                                                                                        

#======================
# End of the experiment
#======================

# Save all data to a file
prtrials.saveAsWideText(data_fname + 'prac' + '.csv', delim=',')


trialCount=0
expAccTot=0
expAccBlock=0

blockno=1



for trial in exTrials:
    if pracDone == 0:
        break
    
    trialCount=trialCount+1
    if trialCount == 1:
                ##Instruction Screen 1: Before starting, make sure to find ...
        expscrbgn_imname=os.path.join(instpath, 'expscrbgn.png')
        instfb=Image.open(expscrbgn_imname)
        enh1=ImageEnhance.Brightness(instfb)
        instfb_end=enh1.enhance(brightness)
        bitmapinst.setImage(instfb_end)
        bitmapinst.draw()
        
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
                
            # Set the images
    im1_fname = os.path.join(exppath, trial['im1'])
    im2_fname = os.path.join(exppath, trial['im2'])
    mask1_fname = os.path.join(scramblepath, trial['mask1'])
    mask2_fname = os.path.join(scramblepath, trial['mask2'])
    
    
    im1=Image.open(im1_fname)
    im2=Image.open(im2_fname)
    enh1=ImageEnhance.Brightness(im1)
    enh2=ImageEnhance.Brightness(im2)
    
    im1_end=enh1.enhance(brightness)
    im2_end=enh2.enhance(brightness)
    
    rnd.shuffle(imside)
    if imside[1] == 0:
        bitmap1.setImage(im1_end)
        bitmap2.setImage(im2_end)
        maskim=Image.open(mask1_fname)
        
    else:
        bitmap1.setImage(im2_end)
        bitmap2.setImage(im1_end)
        maskim=Image.open(mask2_fname)
    
    maskend=asarray(maskim)
    maskend=maskend/256
    maskend=maskend/brightdiv
    masking=Image.fromarray(maskend)
    
    maskmap.setImage(masking)
    
    
    
    bitmap1.setOri(trial['ori'])
    bitmap2.setOri(trial['ori'])
    maskmap.setOri(trial['ori'])

    maskmap.setOri(trial['ori'])
    if trial['ori'] == 0:
        eyeleveling=-1.18
    else:
        eyeleveling=1.18

            
    
    fixation = visual.ShapeStim(win, 
    vertices=((0, -0.3), (0, 0.3), (0,0), (-0.3,0), (0.3, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor="black"
    )


    bitmap1.pos=(0,eyeleveling) #142+284/2 (5.1 is equal to 142 pixels, then we add half of the horizontal size (7/2) because pos. takes the center to the defined location.)
    
    bitmap2.pos=(0,eyeleveling)
    
    maskmap.pos = (0,eyeleveling)

                                
    bitmap1.size=(7.05,8.38)
    bitmap2.size=(7.05,8.38)  
    maskmap.size=(7.05,8.38)
    for nFrames in range(FixFrame): # 600 ms.
        fixation.draw()
        win.flip()
    for nFrames in range(IntFrame):  # 500 ms
        win.flip()        
                
    
    for nFrames in range(ImFrame): # 300 ms
        bitmap1.draw()
        win.flip()
        

    
    for nFrames in range(MaskFrame): # 200 ms
        maskmap.draw()
        win.flip()
    
    bitmap2.draw()
    win.flip()
    change_clock.reset()
    rt_clock.reset()
                                
    # Wait until a response, or until time limit.
         
    # Wait until a response, or until time limit.
    keys = event.waitKeys(keyList=['s','l', 'escape'])
              
    # If a key is pressed, take the reaction time. If not, just remove the images from the screen    
    if keys:
        rt = rt_clock.getTime()
    bitmap1.clearTextures()
    bitmap2.clearTextures()
    win.flip()
    win.flip(clearBuffer=True)
                                    
        #At this point, there are still no keys pressed. So "if not keys" is definitely 
        #going to be processed.
        #After removing the images from the screen, still listening for a keypress. 
        #Record the reaction time if a key is pressed.
                                    
    if not keys:
        keys = event.waitKeys(keyList=['s','l','escape'])
        rt = rt_clock.getTime()
                                        
        #If the key is pressed analyze the keypress.
    acc = 0
    if keys:
        if 'escape' in keys:
            break
        elif 's' in keys and trial['dissim'] == 0: # is same
            acc = 1
        elif 'l' in keys and not trial['dissim'] == 0: # is different
            acc = 1
    
                                                    
    expAccTot=expAccTot+acc
    expAccBlock=expAccBlock+acc
    #print(expAccBlock)
    #print(trialCount)
    blockPerc=expAccBlock/48*100                     
    #print(blockPerc)         
    exTrials.addData('rt', rt)
    exTrials.addData('acc', acc)
    rnd.shuffle(ISI)
    core.wait(ISI[1])
              
    if trialCount%48 == 0 and not trialCount == 768:
        
        if blockPerc < 65:
            inst1_fbname=os.path.join(instpath, 'expscr3.png')
        elif blockPerc >= 65:
            inst1_fbname=os.path.join(instpath, 'expscr1.png')
        
        instfb=Image.open(inst1_fbname)
        enh1=ImageEnhance.Brightness(instfb)
        instfb_end=enh1.enhance(brightness)
        bitmapinst.setImage(instfb_end)
        bitmapinst.draw()
        
        win.flip()
        
    
        expAccBlock=0
        blockPerc=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()
        if 'escape' in keys:
            win.flip()
            break
        elif 'space' in keys:
            keys = []
            event.clearEvents()
            win.flip()
        core.wait(IBW)
    elif trialCount == 768:
        
        inst1_fbname=os.path.join(instpath, 'ending.png')

        instfb=Image.open(inst1_fbname)
        enh1=ImageEnhance.Brightness(instfb)
        instfb_end=enh1.enhance(brightness)
        bitmapinst.setImage(instfb_end)
        bitmapinst.draw()
        win.flip()
           
        keys = event.waitKeys(keyList=['escape'])
        win.flip()
        if 'escape' in keys:
            win.flip()
            break
        core.wait(IBW)
            
                # Add the current trial's data to the TrialHandler

                # Advance to the next trial


exTrials.saveAsWideText(data_fname + 'Exp' + '.csv', delim=',')
# Quit the experiment
win.close()
win.mouseVisible=True


