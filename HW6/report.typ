#set text(font: "New Computer Modern") 
#align(center, text(20pt)[
  *Mcahine Vision HW6 Report*
])
#align(right, [資工三 110590004 林奕廷])
= Dependencies
```toml
python = ">=3.9,<4"
opencv-python = "^4.9.0.80"
alive-progress = "^3.1.5"
```
= Run
```bash
python 110590004_hw6.py
```

= Question 1
== Canny Edge Detector
- Implement Canny edge detector.
=== Step 1 Noise Reduction 
- Apply a Gaussian filter to smooth the image in order to reduce noise. Using
  kernel size 5x5 and sigma 0.9.
=== Step 2 Finding Intensity Gradient of the Image 
- Use Sobel operator to calculate the gradient and direction of each pixel. 
=== Step 3 Non-maximum Suppression
- Thin the edges by removing pixels that are not considered to be part of an edge.
=== Step 4 Double Threshold
- Use two thresholds to determine potential edges.
=== Step 5 Edge Tracking by Hysteresis
- Track edges by hysteresis: pixels that are weak and not connected to strong
  edges are removed.
=== Result
- The result of Canny edge detector is shown below.


#pagebreak()
