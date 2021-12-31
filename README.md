# UNIOA
- [ Description. ](#desc)
- [ Ideas. ](#idea)
- [ Environment. ](#env)
- [ Example. ](#exm)
  - [ customized optimizer. ](#exm1)
  - [ benchmark and comparison. ](#exm2)
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
<a name="exm1"></a>
### customized optimizer
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
# optimize method customized by yourself
def your_Opt_X(old_x, y, x_ip, z, w):
    new_x = ( old_x * z - y )*w + x_ip
    return new_x
Opt_X.your = your_Opt_X
```
6. **design each component in math and code**.\
   (1)To <img src="https://latex.codecogs.com/svg.image?\mathbf{y}_i" title="\mathbf{y}_i" /> , the optimize method designed as <img src="https://latex.codecogs.com/svg.image?\mathbf{y}_i(t&plus;1)=\mathbf{y}_i(t)\times&space;w_2" title="\mathbf{y}_i(t+1)=\mathbf{y}_i(t)\times w_2" />
```python
# initialize method selected in UNIOA
Init_Delta_Y.your = Init_Delta_Y.x_type
# optimize method customized by yourself
def your_Opt_Delta_Y(old_y, w):
    new_y = old_y * w
    return new_y
Opt_Delta_Y.your = your_Opt_Delta_Y
```
  (2)To <img src="https://latex.codecogs.com/svg.image?\mathbf{x}_{i_p}" title="\mathbf{x}_{i_p}" /> , the optimize method selected in UNIOA
```python
# initialize method selected in UNIOA
Init_Delta_X.your = Init_Delta_X.Personal_best
# optimize method selected in UNIOA
Opt_Delta_X.your = Opt_Delta_X.Personal_best
```
  (3)To <img src="https://latex.codecogs.com/svg.image?z" title="z" /> , the optimize method designed as <img src="https://latex.codecogs.com/svg.image?z(t&plus;1)=z(t)\times&space;w" title="z(t+1)=z(t)\times w" />
```python
# initialize and optimize method customized by yourself
def your_InitOpt_Delta_z(t, old_z, w):
    if t == 0:
        new_z = old_z
    else:
        new_z = old_z * w
    return new_z
InitOpt_Delta_z.your = your_InitOpt_Delta_z
```
  (4)To <img src="https://latex.codecogs.com/svg.image?w" title="w" /> , summarize all pre-set static parameters.
```python
# initialize/setup static numerical influencing factors
M = 10
z_0 = 1 # assizt z
w1 = 0.8 # assist z
w2 = 0.6 # assist to update y
w3 = 0.7 # assist to update x
```
7. **put each component in fixed position**. 
```python
# fixed 
class Your_Opt(NatureOpt): 
    def __init__(self, func, hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
```
```python
# open to the user
        self.M = hyperparams_set.get('M')
        self.z_0 = hyperparams_set.get('z_0')
        self.w1 = hyperparams_set.get('w1')
        self.w2 = hyperparams_set.get('w2')
        self.w3 = hyperparams_set.get('w3')
```
```python
# fixed
    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
```
```python
# fixed position, open inputs
        Y = self.Init_Delta_Y.x_type(X=X)
        X_ip, X_ip_Fit = self.Init_Delta_X.Personal_best(new_X=X, new_X_Fit=X_Fit)
        z = self.InitOpt_Delta_z.your(t=t, old_z=self.z_0,w=self.w1)
```
```python
# fixed
        while not self.stop:
```
```python
# fixed position, open inputs
            new_Y = self.Opt_Delta_Y.your(old_y=Y, w=self.w2)
            temp_X = self.Opt_X.your(old_x=X, y=new_Y, x_ip=X_ip, z=z, w=self.w3)
            temp_X_Fit = self.Evaluate_X(X=X)
            new_X, new_X_Fit = self.Selection.your(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit)

            t = t + 1
            z = self.InitOpt_Delta_z.your(t=t, old_z=z,w=self.w1)
            X_ip, X_ip_Fit = self.Opt_Delta_X.your(new_X=new_X, new_X_Fit=new_X_Fit, old_X_p=X_ip, old_X_p_Fit=X_ip_Fit)
            X = new_X
            X_Fit = new_X_Fit
```








<a name="ver"></a>

<a name="exm2"></a>
### benchmark and comparison


## Versions
`2021.12.31: only works in .py file now`