#%% [markdown]
# # EX4: Circle Hough transform
# In the ex. we will implement step by step circle hough transform.
# Follow the code and fill in the missing parts
# ## Prep
# %%
# to run in google colab
import sys
if 'google.colab' in sys.modules:
    ! apt-get install subversion
    ! svn export https://github.com/YoniChechik/AI_is_Math/trunk/p_04_curve_fitting/ex4/circles.bmp

# %%
from matplotlib import pyplot as plt
import cv2
import numpy as np

fig_size = (10, 10)
# %%
# to run interactively with vscode
import os
if os.getcwd().endswith("AI_is_Math"):
    os.chdir("p_04_curve_fitting/ex4")

# %% [markdown]
# ## Import an image
# %%
im3 = cv2.imread("circles.bmp")
im3 = cv2.cvtColor(im3, cv2.COLOR_BGR2RGB)

im = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)

plt.figure(figsize=fig_size)
plt.imshow(im3, cmap='gray', vmin=0, vmax=255)
plt.title("original image")
plt.show()


# %% [markdown]
# ## Find edges of an image using Canny
# %%
# TODO: Canny edge detection of image 
mag_im = []

plt.figure(figsize=fig_size)
plt.imshow(mag_im)
plt.title("edge image")
plt.show()

# %% [markdown]
# ## Initialize accumulation matrix
# %%
# TODO: state parameters for accumulation matrix
# What parameters a circle accumulation matrix needs?
# Hint: very similar to what we did in line Hough transform
# If you need more clues, try assuming you already finished this part and continue with the ex.
# (6-8 lines- but all are similar to each other)
some_params_here = None

# TODO: init accumulation matrix (one line)
acc_mat = []

# %% [markdown]
# ## Fill accumulation matrix
# %%
# get indices of edges
edge_inds = np.argwhere(mag_im > 0)

# run on all a,b and edge indices and find corresponding R
for yx in edge_inds:
    x = yx[1]
    y = yx[0]

    for a_ind, a0 in enumerate(a):
        for b_ind, b0 in enumerate(b):

            # TODO: find best corresponding R (~3 lines)
            # Hint: this can be done faster if you add TH to max_r

            r0 = np.round(r0/r_step)*r_step
            r_ind = np.argmin(np.abs(r0-r))

            # TODO: update accumulation matrix (one line)

#%%
plt.figure(figsize=fig_size)
plt.imshow(np.sum(acc_mat, axis=2), extent=[b.min(), b.max(), a.max(), a.min()],aspect='auto')
plt.xlabel('a')
plt.ylabel('b')
plt.title('accumulation matrix summed over r axis')
plt.colorbar()
plt.show()

# %% [markdown]
# ## Threshold accumulation matrix
# %%
TH = 25
acc_mat_th = acc_mat > TH

plt.figure(figsize=fig_size)
plt.imshow(np.sum(acc_mat_th, axis=2), extent=[b.min(), b.max(), a.max(), a.min()],aspect='auto')
plt.xlabel('a')
plt.ylabel('b')
plt.title('accumulation matrix TH summed over r axis')
plt.colorbar()
plt.show()
# %% [markdown]
# ## Min distance
# This is a new feature that deals with noise in the accumulation matrix.
# 1. Search in the neighborhood of each above TH bin for other above TH bins
# 2. compare the two and delete the less important one
#%%
edge_inds = np.argwhere(acc_mat_th > 0)

min_dist = 15

acc_mat_th_dist = acc_mat_th.copy()
# run on all above TH bins
for i in range(edge_inds.shape[0]):
    b0, a0, r0 = edge_inds[i]

    # search in all other above TH bins
    for j in range(i+1, edge_inds.shape[0]):
        b1, a1, r1 = edge_inds[j]
        
        # if the two above are neighbors (below min_dist) - delete the less important
        if ((r0-r1)*r_step)**2+((a0-a1)*a_step)**2+((b0-b1)*b_step)**2 < min_dist**2:
            if acc_mat[b0, a0, r0] >= acc_mat[b1, a1, r1]:
                #TODO: one line fill here
                pass
            else:
                #TODO: one line fill here
                pass
#%%
plt.figure(figsize=fig_size)
plt.imshow(np.sum(acc_mat_th_dist, axis=2), extent=[b.min(), b.max(), a.max(), a.min()],aspect='auto')
plt.xlabel('a')
plt.ylabel('b')
plt.title('accumulation matrix TH and min_dist summed over r axis')
plt.colorbar()
plt.show()

# %% [markdown]
# ## Plot circles found by hough
# %%
# get indices of acc_mat_th_dist
edge_inds = np.argwhere(acc_mat_th_dist > 0)

res = im3.copy()
for b_ind, a_ind, r_ind in edge_inds:
    r0 = r[r_ind]
    a0 = a[a_ind]
    b0 = b[b_ind]

    # draw the outer circle
    res = cv2.circle(res, (a0, b0), r0, (0, 255, 0), 1)

plt.figure(figsize=fig_size)
plt.imshow(res)
plt.title("final result")
plt.show()
#%% [markdown]
# ## Comparison to cv2.HoughCircles
# %%
res = im3.copy()

# explanation can ve found here:
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1,
                           10, param1=100, param2=8, minRadius=5, maxRadius=30)

for xyr in circles[0, :]:
    # draw the outer circle
    res = cv2.circle(res, (xyr[0], xyr[1]), xyr[2], (0, 255, 0), 1)

plt.figure(figsize=fig_size)
plt.imshow(res)
plt.title("final result- cv2.HoughCircles")
plt.show()

#%%
