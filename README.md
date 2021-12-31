# UNIOA
- [ Description. ](#desc)
- [ Ideas. ](#idea)
- [ Environment. ](#env)
- [ Example. ](#exm)
- [ Versions. ](#ver)

<a name="desc"></a>
## Description
UNIOA can help:
1. design your own swarm-based algorithms with only math knowledge, without any nature/bio knowledge.
2. benchmark your optimization algorithm **Your_Opt** with other seven existing algorithms with the help of IOHprofiler.

UNIOA is a small python package in which the user can design his/her own algorithm like nature-inspired algorithms. This package is inspired by standardizing nature-inspired algorithms project in which we build up a generic framework based on studying seven popular swarm-based algorithm.
<a name="idea"></a>
## Ideas
We built up this generic framework that can cover seven algorithms now. The generic framework is :
![framework](framework.png)
- **line1** iteration counter. At this moment, the optimization starts.
- **line2** initialize the initial pop with size M. Compulsory part. Fixed in UNIOA.
- **line3** evaluate fitness. Compulsory part. Fixed in UNIOA with the help of IOH.
- **line4** initialize influencing factors. Elective part. Open in UNIOA. **Customized part by users or select from UNIOA**.
- **line5** stop condition. Compulsory part. Fixed in UNIOA with the help of IOH.
- **line6** update assisting vector influencing factor. Elective part. Open in UNIOA. **Customized part by users**.
- **line7** update pop. Compulsory part. Open in UNIOA. **Customized part by users**.
- **line8** evaluate fitness. Compulsory part. Fixed in UNIOA with the help of IOH.
- **line9** selection. Compulsory part. Fixed/Open in UNIOA. **Customized part by users or select from UNIOA**.
- **line10** iteration counter. At this moment, the pop already is updated one time.
- **line11** update other vector influencing factors or dynamic numerical influencing factors. Elective part. Open in UNIOA. **Customized part by users**.

<a name="env"></a>
## Environment
```python
Python = 3.7
ioh = 0.3.2.3
numpy = 1.18.2
numba = 0.54.1
sklearn = 1.0
```
<a name="exm"></a>
## Example
1. install relative packages
```python
pip install ioh == 0.3.2.3
pip install UNIOA
```
2. open a `.py` file.
```python 
example.py
```
3. only import UNIOA
````python
from UNIOA import *
````
4. make sure what components will exist in your optimizer.\
You want to use follows to design the optimizer.\
   (1) assisting vector influencing factor <img src="https://latex.codecogs.com/svg.image?\mathbf{y}_i" title="\mathbf{y}_i" />.\
   (2) <img src="https://latex.codecogs.com/svg.image?\mathbf{x}" title="\mathbf{x}" /> related vector influencing factor <img src="https://latex.codecogs.com/svg.image?\mathbf{x}_{i_p}" title="\mathbf{x}_{i_p}" />.\
   (3) dynamic numberical influencing factor <img src="https://latex.codecogs.com/svg.image?z" title="z" />.\
   (4) static numberical influencing factors <img src="https://latex.codecogs.com/svg.image?w" title="w" />.
   
5. design a method to update <img src="https://latex.codecogs.com/svg.image?\mathbf{x}_{i}" title="\mathbf{x}_{i}" /> as <img src="https://latex.codecogs.com/svg.image?\mathbf{x}_i(t&plus;1)=(\mathbf{x}_i(t)\times&space;z(t)&space;-&space;\mathbf{y}_i(t))\times&space;w_1&space;&plus;&space;\mathbf{x}_{i_p}(t)" title="\mathbf{x}_i(t+1)=(\mathbf{x}_i(t)\times z(t) - \mathbf{y}_i(t))\times w_1 + \mathbf{x}_{i_p}(t)" />
```python
def your_Opt_X(old_x, y, x_ip, z, w):
    new_x = ( old_x * z - y )*w + x_ip
    return new_x
Opt_X.your = your_Opt_X
```
6. design each component in math and code.\
   (1)To <img src="https://latex.codecogs.com/svg.image?\mathbf{y}_i" title="\mathbf{y}_i" /> , the optimize methods designed as <img src="https://latex.codecogs.com/svg.image?\mathbf{y}_i(t&plus;1)=\mathbf{y}_i(t)\times&space;w_2" title="\mathbf{y}_i(t+1)=\mathbf{y}_i(t)\times w_2" />
```python
# initialize method selected in UNIOA
Init_Delta_Y.your = Init_Delta_Y.x_type
# optimize method customized by yourself as the following math formula
def your_Opt_Delta_Y(old_y, w):
    new_y = old_y * w
    return new_y
Opt_Delta_Y.your = your_Opt_Delta_Y
```





<a name="ver"></a>
## Versions
`2021.12.31: only works in .py file now`