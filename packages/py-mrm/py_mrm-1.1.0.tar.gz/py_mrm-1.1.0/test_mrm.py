import numpy as np
import scipy.sparse.linalg as sla
import py_mrm as mrm

# Sample input data
Nx = 10
x_f = np.linspace(-1, 1, Nx+1)  # Positions of cell faces
x_c = 0.5*(x_f[1:] + x_f[0:-1]) # Cell-centered positions
bc = {
    'a': [0, 0],
    'b': [1, 1],
    'd': [x_f[0], x_f[-1]]
}

sz = Nx  # Number of cells in each dimension  
Grad, grad_bc = mrm.construct_grad(0, sz, x_c, x_f, bc)


# Call the function
dim = 1
sz = [1,Nx,1]  # Number of cells in each dimension  
Grad, grad_bc = mrm.construct_grad(dim, sz, x_c, x_f, bc)

# Print the result
print("Grad matrix:")
print(Grad.toarray())
print("grad_bc column vector:")
print(grad_bc.toarray())
print("grad(x_c):")
print(Grad.dot(x_c.reshape(-1,1)) + grad_bc)

nu = lambda r: r
Div = mrm.construct_div(dim, sz, x_f, 1)
print("Div matrix:")
print(Div.toarray())
print("div(x_f):")
print(Div.dot(x_f.reshape(-1,1)))

rng = np.random.default_rng()
c = rng.random((2,3,2,5))
f = lambda c: c*c[:,:,(1,0),:]
Jac, val = mrm.numjac_local(2, f, c)

bc = {
    'a': [0, 0],
    'b': [1, 1],
    'd': [2, 2.1]
}
dim = 1
sz = [2, 2, 5,2]
Conv, conv_bc =  mrm.construct_convflux_upwind(dim, sz, x_c, x_f, bc, -1)
print("Conv matrix:")
print(Conv.toarray()) 
print("conv_bc column vector:")
print(conv_bc.toarray())   
    
    