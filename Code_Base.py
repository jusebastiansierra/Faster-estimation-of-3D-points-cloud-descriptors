import numpy as np
from sklearn.neighbors import NearestNeighbors
import time
import pandas as pd
inicio = time.time()

#Load your Point cloud as  .csv file

df = pd.read_csv("Point_Cloud.csv", sep=" ", header=None)
X=np.array(df[0])
Y=np.array(df[1])
Z=np.array(df[2])

# Define your neighborhood size

kmin = 10
kmax = 100
deltaK = 10
k_plus_1 = kmax+1;
stepsK = int((kmax - kmin)/deltaK)
K = np.linspace(kmin, kmax, stepsK)
K = K.astype(int)
num_k = len(K)

#do some initialization to manege the split size 

saltos=1000
alpha=np.linspace(0,len(X),saltos)
alpha=alpha.astype(int)
alpha1=alpha[:(len(alpha)-1)]
alpha2=alpha[1:]
All=np.zeros([len(X),11])

#Split the poind cloud in small sizes

def split(A,B):
    x=X[A:B]
    y=Y[A:B]
    z=Z[A:B]
    xyz=np.array([x,y,z]).T
    
    # get local neighborhoods consisting of k neighbors
    
    nbrs = NearestNeighbors(n_neighbors=k_plus_1, algorithm='kd_tree', metric='euclidean').fit(xyz)
    distances, idx = nbrs.kneighbors(xyz)
    point_ID_max = len(x)
    
    # do some initialization stuff 
    
    Shannon_entropy = np.zeros([point_ID_max,num_k])
    opt_nn_size = np.zeros([point_ID_max,1])
    final= np.zeros([point_ID_max,8])
    
    #calculate Shannon entropy
    
    for j1 in range(0,point_ID_max):
        Shannon_entropy_real = np.zeros([1,num_k])
        for j2 in range(0,num_k):
                        
            # select neighboring points
            
            P = idx[j1,1:int(K[j2])+1]      # the point and its k neighbors ...
            cov_mat = np.cov([x[P],y[P],z[P]])
            eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
            eig_val_cov = np.sort(eig_val_cov)
            epsilon_to_add = 1e-8;
            if eig_val_cov[2] <=0:
                eig_val_cov[2] = epsilon_to_add
            if eig_val_cov[1] <=0:
                eig_val_cov[1] = epsilon_to_add
            if eig_val_cov[0] <=0:
                eig_val_cov[0] = epsilon_to_add
            
            # normalize EVs
            
            EVs = 1.0*eig_val_cov/sum(eig_val_cov);
            
            # derive Shannon entropy based on eigenentropy
            
            Shannon_entropy_cal = -( EVs[0]*np.log(EVs[0]) + EVs[1]*np.log(EVs[1]) + EVs[2]*np.log(EVs[2]) )
            Shannon_entropy_real[0,j2] = np.real(Shannon_entropy_cal)
        Shannon_entropy[j1,:] = Shannon_entropy_real
        
        #select k with minimal Shannon entropy
        
        min_entry_of_Shannon_entropy = np.argmax(Shannon_entropy_real)
        opt_nn_size[j1,0] = K[min_entry_of_Shannon_entropy]

    #Calculate the Geometric descriptors     
    
    for i in range (0,point_ID_max):

        new_k = idx[i,1:int(opt_nn_size[i,0])+1]
        cov_mat2 = np.cov([X[new_k],Y[new_k],Z[new_k]])
        eig_val_cov2, eig_vec_cov2 = np.linalg.eig(cov_mat2)
        eig_val_cov2 = np.sort(eig_val_cov2)
        eps2 = 1e-8;
        e1 = eig_val_cov2[2]
        e2 = eig_val_cov2[1]
        e3 = eig_val_cov2[0]
        
        # Anistropy, planarity, sphericity, Lniearity, curvature....
        # https://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/II-3/9/2014/isprsannals-II-3-9-2014.pdf
           
        if(e1>0 and e2>0 and e3>0):
            p0 = (e1-e2)/(e1 + eps2)  # Linearity
            p1 = (e2-e3)/(e1 + eps2)  # Planarity
            p2 =  e3/(e1 + eps2)      # Sphericity
            p3 = pow(e1*e3*e3,1/3.0)  # Omnivariance
            p4 = (e1-e3)/(e1 + eps2)  # Anisotropy
            p5 = -( e3*np.log(e3) + e2*np.log(e2) + e1*np.log(e1) ) #Eigenentropy
            p6 = e1 +e3 + e3          # sumatory
            p7 = e3/(e1+e2+e3 + eps2) # change of curvature
        else:
            p0 = 0
            p1 = 0
            p2 = 0
            p3 = 0
            p4 = 0
            p5 = 0
            p6 = 0
            p7 = 0
        
        #Create an Array to keep the descriptors results        
        
        final[i,0] = np.real(p0)   #Linearity
        final[i,1] = np.real(p1)   #Planarity
        final[i,2] = np.real(p2)   #Sphericity
        final[i,3] = np.real(p3)   #Omnivariance
        final[i,4] = np.real(p4)   #Anisotropy
        final[i,5] = np.real(p5)   #Eigenentropy
        final[i,6] = np.real(p6)   #sumatory
        final[i,7] = np.real(p7)   #change of curvature
    End = np.append(xyz,final,axis=1)
    return End


#This variable has all the Descriptors and x,y,z values of the all point cloud

for i in range(len(alpha1)):
    c=split(alpha1[i],alpha2[i])
    All[alpha1[i]:alpha2[i],:]=c
    del c

#The final result generate 9 differents csv files 

np.savetxt("Name_All.csv",All, delimiter = " ")

Linearity = np.array([X,Y,Z,All[:,3]]).T
np.savetxt("Name_Linearity.csv",Linearity, delimiter = " ")
del Linearity


Planarity = np.array([X,Y,Z,All[:,4] ]).T
np.savetxt("Name_Planarity.csv",Planarity, delimiter = " ")
del Planarity

Sphericity = np.array([X,Y,Z,All[:,5]]).T
np.savetxt("Name_Sphericity.csv",Sphericity, delimiter = " ")
del Sphericity

Omnivariance = np.array([X,Y,Z,All[:,6]]).T
np.savetxt("Name_Omnivariance.csv",Omnivariance, delimiter = " ")
del Omnivariance

Anisotropy = np.array([X,Y,Z,All[:,7]]).T
np.savetxt("Name_Anisotropy.csv",Anisotropy, delimiter = " ")
del Anisotropy

Eigenentropy = np.array([X,Y,Z,All[:,8]]).T
np.savetxt("Name_Eigenentropy.csv",Eigenentropy, delimiter = " ")
del Eigenentropy

sumatory = np.array([X,Y,Z,All[:,9]]).T
np.savetxt("Name_sumatory.csv",sumatory, delimiter = " ")
del sumatory

change_curvature = np.array([X,Y,Z,All[:,10]]).T
np.savetxt("Name_change_curvature.csv",change_curvature, delimiter = " ")



fin = time.time()
print(" ")
print('The compilation time was:',((fin-inicio)/60),' Minutes')
