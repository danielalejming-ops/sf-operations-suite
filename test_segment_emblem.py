# -*- coding: utf-8 -*-
import cv2
import numpy as np

# Load high-res crop of the logo
img = cv2.imread(r'C:\Users\danie\Downloads\SF\Referencias\Logo.jpeg')
# y: 350 to 970, x: 800 to 1750
monogram = img[350:970, 800:1750]
h, w, _ = monogram.shape

# 1. SEGMENT CENTRAL CIRCULAR DIAL
# In monogram, the dial center is around x=495, y=325, radius roughly 65 px
dial_cx, dial_cy, dial_r = 495, 325, 68
mask_dial = np.zeros((h, w), dtype=np.uint8)
cv2.circle(mask_dial, (dial_cx, dial_cy), dial_r, 255, -1)

# 2. SEGMENT S LETTER (left of dial)
# S is located roughly between x=60 and x=500
# Mask gold areas of S
hsv = cv2.cvtColor(monogram, cv2.COLOR_BGR2HSV)
_, s_ch, v_ch = cv2.split(hsv)

# Gold letter mask: V > 60, not dark red background
# Red has hue 160-180 and 0-15
h_ch = hsv[:, :, 0]
is_red = ((h_ch < 15) | (h_ch > 165)) & (s_ch > 80) & (v_ch < 160)
mask_gold = (v_ch > 55) & (~is_red)

# S region
mask_s = np.zeros((h, w), dtype=np.uint8)
# S letter coordinates: x from 60 to 520, y from 80 to 560
mask_s[80:560, 60:520] = mask_gold[80:560, 60:520]
# Exclude dial area
mask_s[mask_dial > 0] = 0
# Exclude upper title text (y < 95)
mask_s[:95, :] = 0

# Clean S mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
mask_s = cv2.morphologyEx(mask_s, cv2.MORPH_CLOSE, kernel)
# Fill small holes inside the stroke
contours_s, _ = cv2.findContours(mask_s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if len(contours_s) > 0:
    c_s_main = max(contours_s, key=cv2.contourArea)
    mask_s_filled = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(mask_s_filled, [c_s_main], -1, 255, -1)
    
    # Also find inner holes of S (the loop)
    # The true hole of S is inside the upper loop and lower loop
    # Let's extract the actual hollows
    hollow_mask = np.zeros((h, w), dtype=np.uint8)
    # Upper hollow roughly x: 230 to 350, y: 220 to 330
    # Lower hollow roughly x: 250 to 420, y: 360 to 480
    gray = cv2.cvtColor(monogram, cv2.COLOR_BGR2GRAY)
    is_dark = gray < 60
    mask_s_final = mask_s_filled.copy()
    # Subtract inner dark regions
    inner_holes = is_dark & (mask_s_filled > 0)
    # Morphological clean on inner holes
    inner_holes = cv2.morphologyEx(inner_holes.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)
    mask_s_final[inner_holes > 0] = 0
else:
    mask_s_final = mask_s

# FIX THE TOP ARCH OF S (Smooth out the flat cut at the top-left)
# Elliptical arc bridging x=200 to x=360 at y=110 to 140
cv2.ellipse(mask_s_final, (290, 142), (82, 38), 0, 180, 360, 255, -1)

# 3. SEGMENT F LETTER (right of dial)
mask_f = np.zeros((h, w), dtype=np.uint8)
# F is located x from 480 to 880, y from 90 to 560
mask_f[90:560, 480:880] = mask_gold[90:560, 480:880]
mask_f[mask_dial > 0] = 0
mask_f[:95, :] = 0

mask_f = cv2.morphologyEx(mask_f, cv2.MORPH_CLOSE, kernel)
contours_f, _ = cv2.findContours(mask_f, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if len(contours_f) > 0:
    c_f_main = max(contours_f, key=cv2.contourArea)
    mask_f_filled = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(mask_f_filled, [c_f_main], -1, 255, -1)
    
    # F hollows between arms
    # Upper bay between top bar and middle bar: x: 580 to 800, y: 180 to 320
    # Lower bay below middle bar: x: 580 to 800, y: 380 to 520
    is_dark = (cv2.cvtColor(monogram, cv2.COLOR_BGR2GRAY) < 60)
    mask_f_final = mask_f_filled.copy()
    inner_f = is_dark & (mask_f_filled > 0)
    inner_f = cv2.morphologyEx(inner_f.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)
    mask_f_final[inner_f > 0] = 0
else:
    mask_f_final = mask_f

# Save segmentation previews
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\segmented_s.png', mask_s_final)
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\segmented_f.png', mask_f_final)
cv2.imwrite(r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\segmented_dial.png', mask_dial)

print('Segmentation complete! Masks saved.')
