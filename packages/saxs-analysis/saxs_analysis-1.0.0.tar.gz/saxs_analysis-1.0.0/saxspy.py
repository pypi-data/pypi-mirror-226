'''Python module for saxs data analysis
Created by : Elizabeth Mathew'''
#import packages
import numpy as np
import shutil
import os
import glob
import copy
import pandas as pd
import scipy
import matplotlib.pyplot as plt 
import ipympl
import pyFAI
import fabio
import cv2
from pyFAI.gui import jupyter

#------------------------------------------
#
# Function to read the dat file from SAXS
#
#------------------------------------------

def read_saxs_dat(filename):
    '''
    read the vd file or the normal dat file obtained from SAXS measurement
    parameters: 
    filename=name of file with location
    results : pandas dataframe of q in ängstrom, I in arbitary unit and sig_q
    '''
    data = open(filename,'r')
    read = data.read()
    splitted_data = read.split('\n')
    title = 'q(A-1)                    I(q)                      Sig(q)                    '
    def line_start(title,splitted_data):
        number = []
        for index, line in enumerate(splitted_data):
            if title in line:
                number.append(index)           
        return number
    start = line_start(title,splitted_data) 
    #print(start)
    data1D =  pd.read_csv(filename,skiprows=int(start[0])+1, header=None,sep="\s+")
    data1D.columns =['q', 'I', 'sig_q']
    return data1D
    
#------------------------------------------
#
# Function to plot the dat file from SAXS
#
#------------------------------------------

def plot_saxs_dat(filename,label):
    '''Plot the dat file
    parameters: 
    filename=name of file with location
    label= label that u want for the plot
    results : single I vs Q plots with legends named label'''
    df=read_saxs_dat(filename)
    plt.figure(figsize=(7, 5))
    plt.semilogy(df['q'],df['I'],label=label)
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($A^{-1}$)", fontsize=14)
    plt.xscale("log")
    plt.legend()
    return plt.show()
    

#----------------------------------------------
#
#Function to do 1D transformation
#
#----------------------------------------------

def one_D_transform(filename,mask_file=None,masking=False):

    '''read the edf file and do the 1D transformation with and without masking
     the function creates a dictoinary with I and q values after normalising the results'''
    # step 1: loading the file
    obj=fabio.open(filename)
    data=obj.data
    data2D = data.transpose()
    shape = data2D.shape
    #step5: creating bins, counting them and saving them to defined hist dictionary
    def hist_normalize(data,obj):
        centerX = float(obj.header['Center_1'])
        centerY = float(obj.header['Center_2'])
        pixelsize = float(obj.header['PSize_1'])
        detectordistance = float(obj.header['SampleDistance'])
        lambda1 = float(obj.header['WaveLength'])
        # step3: creating the data_points, stepsize
        posx = []
        posy = []
        for i in np.arange(1,shape[0]+1,1):
            posx.append((i-centerX)*pixelsize)
        for i in np.arange(1,shape[1]+1,1):
            posy.append((i-centerY)*pixelsize)
        qmin=0
        # divided the formulation in two parts f1 and then qmax
        f1 = ((np.sqrt(2)*shape[1]*pixelsize)/detectordistance)
        qmax = (4*np.pi/lambda1)*(np.sin(0.5*np.arctan(f1)))
        stepsize = (qmax-qmin)/1000
        numofsteps = np.round((qmax-qmin)/stepsize) 
        # step4: creating histogram to save the results
        hist={}
        t1 = []
        for i in np.arange(0,numofsteps+1,1):
            t1.append(i*stepsize)
        hist['q'] = np.array(t1)
        hist ['I'] = np.zeros(int(numofsteps)+1)
        hist ['I_corr'] = np.zeros(int(numofsteps)+1)
        low = 0
        high = 0
        bin2 = []
        for i in np.arange(0,shape[0],1):
            for j in np.arange(0,shape[1],1):
                f2 = np.sqrt((posx[i])**2+(posy[j])**2)/detectordistance
                q = (4*np.pi/lambda1)*(np.sin(0.5*np.arctan(f2)))
                bin1 = np.round((q-qmin+stepsize)/stepsize)
                if bin1<1:
                    low = low+1
                if bin1>numofsteps:
                    high = high+1
                if bin1>=1:
                    if bin1<=numofsteps:
                        if data[i][j] >=0:
                            bin2.append(bin1)
                            hist['I'][int(bin1)] = hist['I'][int(bin1)]+1
                            hist['I_corr'][int(bin1)] = hist['I_corr'][int(bin1)]+data[i][j]
        return hist,numofsteps
    if masking==True:
        hist,numofsteps=hist_normalize(mask_file,obj)
    else:
        hist,numofsteps= hist_normalize(data2D,obj)
    #step6 : create another histogram to save the normalised results
    qscan = {}
    t2=[]
    for i in np.arange(0,int(numofsteps)+1,1):                        
        qscan['q'] = hist['q']
        if hist['I'][i]>0:
            t2.append(hist['I_corr'][i]/hist['I'][i])
    qscan['I'] = np.array(t2)
    return qscan
    
#------------------------------------------------
#    
# Function to plot 1D transformation
#    
#------------------------------------------------

def one_D_plot(filename,label,mask_file=None,masking=False):
    '''plot the 1D transformation of SAXS data
    parameters: 
    filename=name of file with location
    label= label that u want for the plot
    results : single I vs Q plots with legends named label'''
    qscan = one_D_transform(filename)
    if masking==True:
        qscan = one_D_transform(filename,mask_file,masking) 
    plt.figure(figsize=(7, 5))
    plt.semilogy(qscan['q'][0:len(qscan['I'])],qscan['I'],label=label)
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    #plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    return plt.show()
    
#------------------------------------------------
#    
# Function to plot scotch and metal
#    
#------------------------------------------------  

def scotch_metal_plot_check_dat(filedetails,file_saxs,dist=None,n=None):
    '''
      Here, I use this to compare it with the dat file 
      and see if its comparing with the edf 1D trandformation
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(file_details)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    dist=0
    for mat,file,distance,c in zip(df.material,df.filename,df.detector_distance,colors):
        if distance != dist:
            i=0
            dist = distance
        else:   
            i=i+1
        

        if mat == 'scotch_tape':
            filename_s_dat = file_saxs+file+'.dat'
        
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['SumForIntensity1'])*(float(s.header['PSize_1'])/float(s.header['SampleDistance']))**2
            dt_s_dat = read_saxs_dat(filename_s_dat)
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_dat['q']*10000000000,dt_s_dat['I'],color=c,label='{}_dat'.format(mat))
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color='r',label='{}_edf'.format(mat))
        if mat == 'metal':
            filename_m_dat = file_saxs+file+'.dat'
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['SumForIntensity1'])*(float(s.header['PSize_1'])/float(s.header['SampleDistance']))**2
            dt_m_dat = read_saxs_dat(filename_m_dat)
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_dat['q']*10000000000,dt_m_dat['I'],color=c,label='{}_dat({})'.format(mat,i))
            plt.plot(dt_m_edf['q'][0:len(dt_s_edf['I'])],dt_m_edf['I']/i_ratio_m,color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show() 
 
def scotch_metal_plot(filedetails,file_saxs,dist=None,n=None):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector only for one distance
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(filedetails)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    dist=0
    for mat,file,distance,c in zip(df.material,df.filename,df.detector_distance,colors):
        if distance != dist:
            i=0
            dist = distance
        else:   
            i=i+1
        
        if mat == 'scotch_tape':
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color=c,label='{}_edf'.format(mat))
        if mat == 'metal':
            #i=i+1
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_edf['q'][0:len(dt_m_edf['I'])],dt_m_edf['I']/i_ratio_m,color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
    
 
def scotch_metal_plot_adv(filedetails,file_saxs):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
      Note : the labels are for 300, 600 , 1200 distance, change in the csv order or 
      adding the new distance care should be taken to consider all that 
      changes.
      
    '''
    df = pd.read_csv(filedetails)
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(7.5, 7))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    distance=0
    dist=[]
    for j,mat in enumerate(df.material):
        if distance != df.detector_distance[j]:
            i=0
            distance = df.detector_distance[j]
            dist.append(distance)
        else:   
            i=i+1

        if mat == 'scotch_tape':
            filename_s_edf = file_saxs+df.filename[j]+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color=colors[j],label='{}_edf'.format(mat))
        if mat == 'metal':
            filename_m_edf = file_saxs+df.filename[j]+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_edf['q'][0:len(dt_m_edf['I'])],dt_m_edf['I']/i_ratio_m,color=colors[j],label='{}_edf({})'.format(mat,i))
            plt.xscale("log")
            plt.yscale("log")
    h, l = ax.get_legend_handles_labels()
    ph = [plt.plot([],marker="", ls="")[0]]*3
    handles = ph[:1] + h[0:6] + ph[1:2] + h[6:12]+ ph[-1:] + h[12:18]
    labels = ["600"] + l[0:6] + ["1200"] + l[6:12]+['300']+ l[12:18]
    leg = plt.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    for vpack in leg._legend_handle_box.get_children():
        for hpack in vpack.get_children()[:1]:
            hpack.get_children()[0].set_width(0)

    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    
def scotch_minus_metal_plot(filedetails,file_saxs,dist=None,n=None):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(filedetails)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    for mat,file,c in zip(df.material,df.filename,colors):
        if mat == 'scotch_tape':        
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
        if mat == 'metal':
            i=i+1
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            dt_m_edf['lim_q']=dt_m_edf['q'][0:len(dt_s_edf['I'])]
            dt_m_edf['I_sm']=dt_m_edf['I']/i_ratio_m-dt_s_edf['I']/i_ratio_s
            dt= pd.DataFrame(dt_m_edf['lim_q'],columns=['lim_q'])
            dt['I_sm']= dt_m_edf['I_sm']
            dt=dt[dt['I_sm'] > 0]
            #print(dt)
            plt.plot(dt['lim_q'],dt['I_sm'],color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
     
#------------------------------------------------
#    
# Function to create mask
#    
#------------------------------------------------  
        
 def my_dpi():
    figure = plt.figure()
    dpi = figure.dpi
    plt.close()
    return dpi

#------------------------------------------------
#    
# ## Function to export the edf image
#    
#------------------------------------------------  

def export_figure_matplotlib(filename, resize_fact=1, plt_show=False,loc=None):
    """
    Export edf file to png in original resolution. The file is saved as my_image.png
    It will be saved in the working directory or the directory according to your 
    specification that iu specify in loc.
    f_name: name of file where to save figure
    resize_fact: resize facter wrt shape of arr, in (0, np.infty)
    plt_show: show plot or not
    loc: location where the png file would be saved eg: './tmp/'
    
    """
    fig = plt.figure(frameon=False)
    obj=fabio.open(filename)
    data=obj.data
    dpi=my_dpi()
    plt.ioff()
    fig.set_size_inches(data.shape[1]/dpi, data.shape[0]/dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    #ax.imshow(arr)
    save_cwd=os.getcwd()
    colornorm = SymLogNorm(1, base=10,
                           vmin=np.nanmin(1),
                           vmax=np.nanmax(data))
    ax.imshow(data,
            cmap="jet",
            norm=colornorm)
    plt.axis('off')
    plt.margins(x=0)
    
    if loc != None:
        plt.savefig(loc+'my_image.png', dpi=(dpi * resize_fact))
        savefig=save_cwd+loc
    else:
        plt.savefig('my_image.png', dpi=(dpi * resize_fact))
        savefig=save_cwd
    return savefig
    
#------------------------------------------------
#
# ## Function to create an ellipse
#    
#------------------------------------------------  


def create_ellipse(filename):
    '''loc=Location of the mask image
       data=filename
       Note:I am using the colour to identify the ellipse range so check for material a bit 
       before using this function, like if the ring is in the Turquoise colour. For my material 
       this was the colour for this intensity. So I have a function named check ellipse that will plot
       major axis for checking if required 
       '''
    
    obj=fabio.open(filename)
    data=obj.data
    dpi=my_dpi()
    image_loc=export_figure_matplotlib(filename)
    img = cv2.imread(image_loc+'/my_image.png')
    plt.ioff()
    #resized = cv2.resize(img, (data.shape[1],data.shape[0]))
    image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_hsv, np.array([0,100,20],np.uint8), np.array([90,255,255],np.uint8))
    Contour_image = mask.copy()
    Contour, Hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(Contour_image, Contour, len(Hierarchy[0])-1, (255, 0, 170), 1)
    List = []
    for c in range(len(Hierarchy[0])):
        for p in Contour[c]:
            point_array = np.array(p[0], dtype = 'int')
            List.append(tuple(point_array))
    
    import math
    Major_List = []
    for p1 in range(0, len(List)):
        for p2 in range(p1+1, len(List)):
            Distance = math.sqrt(math.pow(List[p1][0] - List[p2][0], 2) + math.pow(List[p1][1] - List[p2][1], 2))
            Major_List.append([List[p1], List[p2], Distance])
    Major_Axis_1 = max(Major_List, key = lambda sublist: sublist[2])
    Major_List.remove(Major_Axis_1)
    Major_Axis_2 = max(Major_List, key = lambda sublist: sublist[2])
    #print('Major_1',Major_Axis_1)
    #print('Major_2',Major_Axis_2)
    slope2=[]
    slope, intercept = np.polyfit([int(Major_Axis_1[0][0]),int(Major_Axis_1[1][0])],[int(Major_Axis_1[0][1]),int(Major_Axis_1[1][1])], 1)
    slope2.append(slope)
    #print(slope)
    #plt.imshow(mask)
    #plt.plot([248,269],[284,310])
    #plt.scatter(float(obj.header['Center_1']),float(obj.header['Center_2']),c='r')
    #plt.plot([int(Major_Axis_1[0][0]),int(Major_Axis_1[1][0])],[int(Major_Axis_1[0][1]),int(Major_Axis_1[1][1])])
    #plt.show()
    return slope 

#------------------------------------------------
#
# ## Creating mask_minor image
#    
#------------------------------------------------  



def make_mask_minor(filename,loc=None):
    '''make a mask minor and 
    '''
    obj=fabio.open(filename)
    data=obj.data
    plt.ioff()
    #plt.imshow(data)
    save_cwd=os.getcwd()
    image_file=export_figure_matplotlib(filename)
    sl= create_ellipse(filename)
    print(sl)
    angle= math.degrees(math.atan(sl))
    #print(angle)
    #if angle<0:
    #    ang= -angle
    #else:
    ang=angle
    upper_limit=ang-15 # here I check what area I would like to choose across around the major and minor axis
    lower_limit=ang+15
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    slope1_minor = np.tan(np.pi/180*(lower_limit+90))
    #print(slope1_minor)
    slope2_minor = np.tan(np.pi/180*(upper_limit+90))
    #print(slope2_minor)
    
    dpi=my_dpi()
    b1_minor = pt[1] - slope1_minor * pt[0]
    b2_minor = pt[1] - slope2_minor * pt[0]
    #print(b1_minor, b2_minor)
    x1_minor = [0,pt[0],0]
    y1_minor = [slope1_minor*x1_minor[0]+b1_minor,pt[1],slope2_minor*x1_minor[2]+b2_minor]
    x2_minor = [data.shape[1],pt[0],data.shape[1]]
    y2_minor = [slope1_minor*x2_minor[0]+b1_minor,pt[1],slope2_minor*x2_minor[2]+b2_minor]
    img = cv2.imread(image_file+'/my_image.png')
    plt.imshow(img)
    plt.fill(x1_minor, y1_minor,'w')
    plt.fill(x2_minor, y2_minor,'w')
    if sl<=-0.3 or sl >=0.3:
        #print('yes')
        plt.plot([0,data.shape[1]],[b1_minor,(slope1_minor*data.shape[1]+b1_minor)],'w',linewidth=2)
        plt.plot([0,data.shape[1]],[b2_minor,(slope2_minor*data.shape[1]+b2_minor)],'w',linewidth=2)
    plt.xlim(0,data.shape[1])
    plt.ylim(data.shape[0],0)
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    #print(pt)
    #plt.scatter(pt[0],pt[1],200,c='g',marker = "o")
    #plt.close()
    if loc != None:
        plt.savefig(loc+'/masked_trial_minor.png',bbox_inches='tight',pad_inches = 0,dpi=dpi)
        savefig=save_cwd+loc
    else:
        plt.savefig('./masked_trial_minor.png',bbox_inches='tight',pad_inches = 0,dpi=dpi)
        savefig=save_cwd
        #print(savefig)
    #plt.show()
    return savefig,sl
    
#------------------------------------------------
#
# ## Creating mask_major image
#    
#------------------------------------------------  




def make_mask_major(filename,loc=None):
    '''make a mask minor and 
    '''
    obj=fabio.open(filename)
    data=obj.data
    plt.ioff()
    image_file=export_figure_matplotlib(filename)
    sl= create_ellipse(filename)
    #print(sl)
    angle= math.degrees(math.atan(sl))
    #if angle<0:
    #    ang= -angle
    #else:
    ang=angle
    upper_limit=ang-15 # here I check what area I would like to choose across around the major and minor axis
    lower_limit=ang+15
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    slope1_major = np.tan(np.pi/180*(lower_limit))
    #print(slope1_major)
    slope2_major = np.tan(np.pi/180*(upper_limit))
    #print(slope2_major)
    slope=[slope1_major,slope2_major]
    
    dpi=my_dpi()
    b1_major = pt[1] - slope1_major * pt[0]
    b2_major = pt[1] - slope2_major * pt[0]
    x1_major = [0,pt[0],0]
    y1_major = [slope1_major*x1_major[0]+b1_major,pt[1],slope2_major*x1_major[2]+b2_major]
    x2_major = [data.shape[1],pt[0],data.shape[1]]
    y2_major = [slope1_major*x2_major[0]+b1_major,pt[1],slope2_major*x2_major[2]+b2_major]      
    save_cwd=os.getcwd()
    img = cv2.imread(image_file+'/my_image.png')
    plt.imshow(img)
    #fig = plt.figure(frameon=False)
    plt.fill(x1_major, y1_major,'w')
    plt.fill(x2_major, y2_major,'w')
    if sl>=-3.7:
        if sl <=3.7:
            plt.plot([0,data.shape[1]],[b1_major,(slope1_major*data.shape[1]+b1_major)],'w',linewidth=2)
            plt.plot([0,data.shape[1]],[b2_major,(slope2_major*data.shape[1]+b2_major)],'w',linewidth=2)
    plt.xlim(0,data.shape[1])
    plt.ylim(data.shape[0],0)
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    #print(pt)
    #plt.scatter(pt[0],pt[1],200,c='g',marker = "o")
    #
    if loc != None:
        plt.savefig(loc+'/masked_trial_major.png',bbox_inches='tight',pad_inches = 0,dpi=dpi)
        savefig=save_cwd+loc
    else:
        plt.savefig('./masked_trial_major.png',bbox_inches='tight',pad_inches = 0,dpi=dpi)
        savefig=save_cwd
    #plt.show(block=False)
    #plt.show()
    return savefig,sl
    




def major_mask(filename, loc=None):
    obj=fabio.open(filename)
    data=obj.data
    data2D=data.transpose()
    plt.ioff()
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    #sl= create_ellipse(filename2)
    image_loc,sl=make_mask_major(filename,loc=None)
    #print(sl)
    img_major =  cv2.imread(image_loc+"/masked_trial_major.png")
    resized_major = cv2.resize(img_major, (data.shape[1],data.shape[0]))
    #plt.imshow(resized_major)
    #plt.scatter(pt[0],pt[1],c='g',marker = "X")
    whiteMin = np.array([0, 0, 231],np.uint8)
    whiteMax = np.array([180, 18, 255],np.uint8)
    HSV_major  = cv2.cvtColor(resized_major,cv2.COLOR_BGR2HSV)
    mask_major = cv2.inRange(HSV_major, whiteMin, whiteMax)
    #plt.imshow(mask_major)
    mask_major_t = mask_major.transpose()
    data_mask_major=data2D.copy()
    shape = data2D.shape
    for i in np.arange(0,shape[0],1):
        for j in np.arange(0,shape[1],1):
            if sl>=-3.7:
                if sl <=3.7:
                #print('yes')
                    if mask_major_t[i][j]==0:
                        data_mask_major[i][j]=-144
            if sl<-3.7 or sl>3.7:
                if mask_major_t[i][j]!=0:
                    data_mask_major[i][j]=-144 
    #plt.close()
    
    return data_mask_major 





def minor_mask(filename, loc=None):
    obj=fabio.open(filename)
    data=obj.data
    data2D=data.transpose()
    plt.ioff()
    pt = (float(obj.header['Center_1']), float(obj.header['Center_2']))
    #sl= create_ellipse(filename2)
    image_loc,sl=make_mask_minor(filename,loc=None)
    #print(sl)
    img_minor =  cv2.imread(image_loc+"/masked_trial_minor.png")
    resized_minor = cv2.resize(img_minor, (data.shape[1],data.shape[0]))
    #plt.imshow(resized_major)
    #plt.scatter(pt[0],pt[1],c='g',marker = "X")
    whiteMin = np.array([0, 0, 231],np.uint8)
    whiteMax = np.array([180, 18, 255],np.uint8)
    HSV_minor  = cv2.cvtColor(resized_minor,cv2.COLOR_BGR2HSV)
    mask_minor = cv2.inRange(HSV_minor, whiteMin, whiteMax)
    #plt.imshow(mask_major)
    mask_minor_t = mask_minor.transpose()
    data_mask_minor=data2D.copy()
    shape = data2D.shape
    for i in np.arange(0,shape[0],1):
        for j in np.arange(0,shape[1],1):
            if sl>=-0.3:
                if sl <=0.3:
                #print('yes')
                    if mask_minor_t[i][j]!=0:
                        data_mask_minor[i][j]=-144
            if sl<=-0.3 or sl>=0.3:
                if mask_minor_t[i][j]==0:
                    data_mask_minor[i][j]=-144 
    #plt.close()
    
    return data_mask_minor 



    
#------------------------------------------------
#    
# Function to save the intensity and q vector in dataframe
#    
#------------------------------------------------      
    
    
 
def scotch_minus_metal_dataframe(scotch_file,metal_file):
    '''
      function to plot the major, minor intensity vs q plot
      parameters: scotch file and matel file, do a foe loop to include 
      all of the files
      
      two outpot major and minor I vs q 
      major_20,minor_20=scotch_minus_metal_dataframe(scotch_file,metal_file)
      
    '''

        
    filename_s_edf = scotch_file
    s = fabio.open(filename_s_edf)
    i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])

    dt_s_major = one_D_transform(filename_s_edf)
    dt_s_minor = one_D_transform(filename_s_edf)

    filename_m_edf = metal_file
    m = fabio.open(filename_m_edf)
            
    i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])
            
    
    mask_file_m_major=major_mask(filename_m_edf)
    mask_file_m_minor=minor_mask(filename_m_edf)
    plt.ioff()

    dt_m_major = one_D_transform(filename_m_edf,mask_file_m_major,masking=True)
    dt_m_minor = one_D_transform(filename_m_edf,mask_file_m_minor,masking=True)
    dt_m_major['lim_q']=dt_m_major['q'][0:len(dt_m_major['I'])]
    dt_m_minor['lim_q']=dt_m_minor['q'][0:len(dt_m_minor['I'])]
    dt_m_major['I_sm']=dt_m_major['I']/i_ratio_m-dt_s_major['I'][0:len(dt_m_major['I'])]/i_ratio_s
    dt_m_minor['I_sm']=dt_m_minor['I']/i_ratio_m-dt_s_minor['I'][0:len(dt_m_minor['I'])]/i_ratio_s
    dt= pd.DataFrame(dt_m_major['lim_q']/10000000000,columns=['lim_q_major'])
    dt['I_sm_major']= dt_m_major['I_sm']
    df= pd.DataFrame(dt_m_minor['lim_q']/10000000000,columns=['lim_q_minor'])
    df['I_sm_minor']= dt_m_minor['I_sm']
                #print(dt)
    dt=dt[dt['I_sm_major'] > 0]
    df=df[df['I_sm_minor']>0]      
    return dt.to_dict('list'),df.to_dict('list')

#------------------------------------------------
#    
# Function to find the area under the curve
#    
#------------------------------------------------     


def area_under_curve(major,minor):
    result={}
    #print(major)
    a=[]
    for i in np.arange(1,len(major)+1,1):
        p_major=pd.DataFrame(major['{}'.format(i)])
        #print(p_major)
        p_minor=pd.DataFrame(minor['{}'.format(i)])
        p_major=p_major[p_major['lim_q_major']>0.007]
        p_major=p_major[p_major['lim_q_major']<0.039]
        a_major=np.trapz(p_major['I_sm_major'],p_major['lim_q_major'])
        p_minor=p_minor[p_minor['lim_q_minor']>0.007]
        p_minor=p_minor[p_minor['lim_q_minor']<0.039]
        a_minor=np.trapz(p_minor['I_sm_minor'],p_minor['lim_q_minor'])
        a.append(a_major-a_minor)
                
    result['delta_area']=a
    result['pos_center']=np.arange(0,len(major),1)
    
    return result           
