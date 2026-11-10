# -*- coding: utf-8 -*-
import cv2
import numpy as np

# Load segmented masks
mask_s = cv2.imread(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\segmented_s.png', cv2.IMREAD_GRAYSCALE)
mask_f = cv2.imread(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\segmented_f.png', cv2.IMREAD_GRAYSCALE)

h, w = mask_s.shape

# 1. CLEAN S:
# Find outer contour of S
contours_s, hier_s = cv2.findContours(mask_s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c_s = max(contours_s, key=cv2.contourArea)

# Draw solid S
solid_s = np.zeros((h, w), dtype=np.uint8)
cv2.drawContours(solid_s, [c_s], -1, 255, -1)

# Now, S has two natural hollow spaces (inner bays/eyes):
# Upper inner bay (inside upper curve): roughly x: 230 to 350, y: 220 to 320
# Lower inner bay (inside lower curve): roughly x: 250 to 420, y: 360 to 480
# Let's extract those exact hollow contours from the original mask
contours_all, hier = cv2.findContours(mask_s, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# Holes have hierarchy[0][i][3] != -1 (child of outer contour)
for i, c in enumerate(contours_all):
    if hier[0][i][3] == 0: # directly inside outer contour
        area = cv2.contourArea(c)
        # The true hollow eyes of S have area > 1500 px
        if area > 1200:
            cv2.drawContours(solid_s, [c], -1, 0, -1)

# Round the top arch of the S so it is 100% continuous and never flat!
# Elliptical arc center at (292, 145), axes (84, 38)
cv2.ellipse(solid_s, (292, 145), (84, 38), 0, 180, 360, 255, -1)

# Smooth the contour slightly with Gaussian blur + threshold to eliminate any 1-pixel jagged steps
solid_s_smooth = cv2.GaussianBlur(solid_s, (5, 5), 0)
_, solid_s_smooth = cv2.threshold(solid_s_smooth, 127, 255, cv2.THRESH_BINARY)

# 2. CLEAN F:
contours_f, _ = cv2.findContours(mask_f, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c_f = max(contours_f, key=cv2.contourArea)
solid_f = np.zeros((h, w), dtype=np.uint8)
cv2.drawContours(solid_f, [c_f], -1, 255, -1)

# F has hollow bays between its horizontal arms:
# Upper bay between top bar and middle crossbar
# Lower bay below middle crossbar
contours_f_all, hier_f = cv2.findContours(mask_f, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for i, c in enumerate(contours_f_all):
    if hier_f[0][i][3] == 0:
        area = cv2.contourArea(c)
        if area > 1000:
            cv2.drawContours(solid_f, [c], -1, 0, -1)

solid_f_smooth = cv2.GaussianBlur(solid_f, (5, 5), 0)
_, solid_f_smooth = cv2.threshold(solid_f_smooth, 127, 255, cv2.THRESH_BINARY)

# 3. CENTRAL DIAL
dial = np.zeros((h, w), dtype=np.uint8)
cv2.circle(dial, (495, 325), 65, 255, -1)
cv2.circle(dial, (495, 325), 45, 0, -1)
cv2.circle(dial, (495, 325), 35, 255, -1)

# Save the solid masks
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\solid_s.png', solid_s_smooth)
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\solid_f.png', solid_f_smooth)
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\solid_dial.png', dial)

print('Solid embroidery masks generated successfully!')
