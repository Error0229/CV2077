#set text(font: "New Computer Modern") 
#align(center, text(20pt)[
  *Mcahine Vision HW5 Report*
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
python 110590004_hw5.py
```

= Question 1
== Mean Filter
- Implement a mean filter with a kernel size of 3x3 and 7x7.
=== 3x3
- Kernel:
#align(center, table(
  columns: 3,
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
  [$1/9$],
))
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1_3.jpg"))),
  grid.cell(figure(image("results/img2_q1_3.jpg"))),
  grid.cell(figure(image("results/img3_q1_3.jpg"))),
)
#pagebreak()
=== 7x7
- Kernel:
#align(center, table(
  columns: 7,
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
  [$1/49$],
)) 
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1_7.jpg"))),
  grid.cell(figure(image("results/img2_q1_7.jpg"))),
  grid.cell(figure(image("results/img3_q1_7.jpg"))),
)

== Median Filter
- Implement a median filter with a kernel size of 3x3 and 7x7.
- Find the median value of the pixel values in the kernel and assign it to the
  center pixel.
=== 3x3
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q2_3.jpg"))),
  grid.cell(figure(image("results/img2_q2_3.jpg"))),
  grid.cell(figure(image("results/img3_q2_3.jpg"))),
)
=== 7x7
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q2_7.jpg"))),
  grid.cell(figure(image("results/img2_q2_7.jpg"))),
  grid.cell(figure(image("results/img3_q2_7.jpg"))),
)

== Gaussian Filter
- Implement a Gaussian filter with a kernel size of 5x5
- Kernel:
#align(center, table(
  columns: 5,
  [$1/273$],
  [$4/273$],
  [$7/273$],
  [$4/273$],
  [$1/273$],
  [$4/273$],
  [$16/273$],
  [$26/273$],
  [$16/273$],
  [$4/273$],
  [$7/273$],
  [$26/273$],
  [$41/273$],
  [$26/273$],
  [$7/273$],
  [$4/273$],
  [$16/273$],
  [$26/273$],
  [$16/273$],
  [$4/273$],
  [$1/273$],
  [$4/273$],
  [$7/273$],
  [$4/273$],
  [$1/273$],
))
=== Result
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q3.jpg"))),
  grid.cell(figure(image("results/img2_q3.jpg"))),
  grid.cell(figure(image("results/img3_q3.jpg"))),
)
= Bonus
== Customized Filter
- Implement a customized filter with a kernel size of 3x3
- Kernel:
```py
kernel = (np.ones((3, 3)) * 0.3)/ (9) + 0.7 * (median of the neighbors)
```
=== Result
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q4.jpg"))),
  grid.cell(figure(image("results/img2_q4.jpg"))),
  grid.cell(figure(image("results/img3_q4.jpg"))),
)


= Discussion
- The mean filter is a simple filter that replaces the center pixel with the
  average of the pixel values in the kernel. It is effective in removing noise but
  may blur the image.
- The median filter is a non-linear filter that replaces the center pixel with the
  median value of the pixel values in the kernel. It is effective in removing
  noise while preserving edges.
- The Gaussian filter is a linear filter that uses a Gaussian kernel to blur the
  image. It is effective in removing noise and preserving edges.
- The customized filter is a combination of the mean filter and the median filter.
  It replaces the center pixel with a weighted average of the pixel values in the
  kernel and the median value of the pixel values in the kernel. It is effective
  in removing noise while preserving edges.
 
