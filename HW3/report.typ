#set text(font: "New Computer Modern") 
#align(center, text(20pt)[
  *Mcahine Vision HW3 Report*
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
python 110590004_hw3.py
```

= Question 1
=== Grayscaling and Binarization
- Use $(0.3 times R) + (0.59 times G) + (0.11 times B)$ to convert the RGB image
  to grayscale image.
- Implement Triangle algorithm to binarize the grayscale image.
  - Apply smoothing in the histogram to get a better threshold.
  - If the `matplotlib` is installed, the histogram and threshold will be shown in
    `debug` folder.
  - Thresholds: `img_1`: 237, `img_2`: 242, `img_3`: 241, `img_4`: 234.
== Part 1
=== N-Connected Distance Transform
- Implement the 4-connected and 8-connected distance transform.
- Using the following formula to calculate the distance:

$ f^0[i,j]  &=f[i,j] \
f^m [i,j] &=f^0[i,j] +min (f^(m-1)[u, v])\
"where "  & (u, v) "is n-neighbors of " (i, j) $

== Part 2
=== Skeletonization
+ Start with the smallest number $h = 1$ in the distance transform.
+ Iteratively remove the points with height $h$ that are not the local maximum of
  4-neighbors. 
+ If removing the point would leads to a connectivity lose, then keep the point.
+ Increase the height $h$ and repeat the process until the height is larger than
  the maximum height in the distance transform.
+ Use the structure element to do thinning on the skeleton. The structure element
  is defined as:
#align(
  center,
  grid(
    columns: 2,
    gutter: 10pt,
    grid.cell(table(columns: 3, [0], [0], [0], [], [1], [], [1], [1], [1])),
    grid.cell(table(columns: 3, [], [0], [0], [1], [1], [0], [], [1], [])),
  ),
)
6. At each iteration, the image is first thinned by the left hand structuring
  element, and then by the right hand one, and then with the remaining six 90°
  rotations of the two elements.
== Result
==== 4-Connected Distance Transform
#grid(
  columns: 2,
  rows: 2,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1-1_4.jpg"))),
  grid.cell(figure(image("results/img2_q1-1_4.jpg"))),
  grid.cell(figure(image("results/img3_q1-1_4.jpg"))),
  grid.cell(figure(image("results/img4_q1-1_4.jpg"))),
)
#pagebreak()
==== 8-Connected Distance Transform
#grid(
  columns: 2,
  rows: 2,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1-1_8.jpg"))),
  grid.cell(figure(image("results/img2_q1-1_8.jpg"))),
  grid.cell(figure(image("results/img3_q1-1_8.jpg"))),
  grid.cell(figure(image("results/img4_q1-1_8.jpg"))),
)
#pagebreak()
==== Skeletonization
#grid(
  columns: 2,
  rows: 2,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1-2.jpg"))),
  grid.cell(figure(image("results/img2_q1-2.jpg"))),
  grid.cell(figure(image("results/img3_q1-2.jpg"))),
  grid.cell(figure(image("results/img4_q1-2.jpg"))),
)
