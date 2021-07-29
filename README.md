# Faster-estimation-of-3D-points-cloud-descriptors
The paper named Faster Estimation Of 3D Points Cloud Descriptors it is developed to get an improved on the compiling time of  the 3D geometric descriptors calculating algorithm. Through the design of two codes based on parallel computing (CPU & GPU) and a reference code to compair the results. 

## Software

- Python 3.8

- CloudCompare

### Libraries

- Numpy 1.2
- Pandas 1.2.4
- Skit-learn 0.22
- Concurrent.futures 3.2
- Cupy 11.2
- Cuda Toolkit 11.2

## Hardware
- Lenovo IdeaPad Gaming
- Intel core i5 9700H, 4 cores
- Graphic card NVidia GTX 1050, 2 GB VRAM.
- 8 GB RAM.


<img width="555" alt="paso1" src="https://user-images.githubusercontent.com/38701770/127534500-bbca3386-e166-4e96-b6ec-6d64fabadc34.png">

## Step by Step

These codes have the same base structure, therefore all three follow the same process for their execution. This section was developed based on the above, in order to show the key points to run the algorithms with any 3D point cloud.

To run the code with a new point cloud, three key steps are required to successfully obtain the results. The first step is to save in the same folder both the Python code and the 3D point cloud in ".CSV" format, thus giving the code access to the required point cloud.

<img width="555" alt="paso1" src="https://user-images.githubusercontent.com/38701770/127534500-bbca3386-e166-4e96-b6ec-6d64fabadc34.png">

The second step involves the modification of the algorithm, allowing to adjust the communication of the algorithm with the new point cloud. The mentioned change should be made in line number 9, where the name of the new file you want to work with should be entered. Finally, in the third step, the name of the files that the code will deliver in the same source folder must be changed in the same way. These files contain the 3D point clouds of the geometric descriptors, therefore it is recommended to leave the name of the descriptor intact and only add the name of the new point cloud to avoid confusion in the future. 


<img width="503" alt="paso2" src="https://user-images.githubusercontent.com/38701770/127535144-7ab1fde3-23f7-4b10-b9a8-2ffcc9a95296.png">

<img width="668" alt="paso22" src="https://user-images.githubusercontent.com/38701770/127535159-2df75088-4685-47c1-b4ff-189c2d2dbf98.png">

As a final result, nine files in ".CSV" format with the names assigned in the previous step should be obtained inside the folder. These files contain the information of each geometric descriptor separately in point cloud format and an additional file containing the information of all descriptors, this in order to facilitate their practical use within other algorithms.


<img width="695" alt="paso3" src="https://user-images.githubusercontent.com/38701770/127535330-c55d6991-502f-4451-ab30-08c4caf6f078.png">

