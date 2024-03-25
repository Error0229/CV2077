#set text(
  font: "New Computer Modern"
) 
#align(center, text(20pt)[
  *Mcahine Vision HW2 Report*
])
#align(right, [資工三 110590004 林奕廷])
= Dependencies
```toml
python = ">=3.9,<4"
opencv-python = "^4.9.0.80"
alive-progress = "^3.1.5"
matplotlib = "^3.8.3" # optional, for visualing the histogram
```
= Run
```bash
python 110590004_hw2.py
```

= Question 1
=== Grayscaling and Binarization
- Use $(0.3 times R) + (0.59 times G) + (0.11 times B)$ to convert the RGB image to grayscale image.
- Implement Triangle algorithm to binarize the grayscale image.
  - Apply smoothing in the histogram to get a better threshold.
  - If the `matplotlib` is installed, the histogram and threshold will be shown in `debug` folder.
  - Thresholds: `img_1`: 234, `img_2`: 218, `img_3`: 239, `img_4`: 230.
=== N-Connected Component Labeling
- Use disjoint set to handle the color's labels grouping and query.
- The principle is to greedily fill colors, if a neighbor has color then fill the same color, otherwise assign a new color.
- For the case that a pixel has multiple neighbors with different colors, assign one of the colors to the pixel and union the rest of the colors.
- Finally, create a mapping from label to n random color, where n is the number of components.
- From 4 connected to 8 connected, there are more neighbors to check, but the principle is the same.
#pagebreak()
== Result
==== 4 Connected
#grid(
  columns: 2,
  rows: 2,
  align: horizon,
  grid.cell(
    figure(
    image("results/img1_4.png"),
      caption: [`img_1`, 5 components]
    ),
    
  ),
  grid.cell(
    figure(
    image("results/img2_4.png"),
      caption: [`img_2`, 424 components]
    ),
  ),
  grid.cell(
    figure(
    image("results/img3_4.png"),
      caption: [`img_3`, 36 components]
    ),
  ),
  grid.cell(
    figure(
    image("results/img4_4.png"),
      caption: [`img_4`, 26 components]
    ),
  ),
)
#pagebreak()
==== 8 Connected
#grid(
  columns: 2,
  rows: 2,
  align: horizon,
  grid.cell(
    figure(
    image("results/img1_8.png"),
      caption: [`img_1`, 5 components]
    ),
    
  ),
  grid.cell(
    figure(
    image("results/img2_8.png"),
      caption: [`img_2`, 236 components]
    ),
  ),
  grid.cell(
    figure(
    image("results/img3_8.png"),
      caption: [`img_3`, 31 components]
    ),
  ),
  grid.cell(
    figure(
    image("results/img4_8.png"),
      caption: [`img_4`, 23 components] 
    ),
  ), 

)
