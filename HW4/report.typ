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
```
= Run
```bash
python 110590004_hw4.py
```

= Question 1
== Part 1
=== Image Labeling
- Use different colors to label different objects in the image.
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1-1.png"))),
  grid.cell(figure(image("results/img2_q1-1.png"))),
  grid.cell(figure(image("results/img3_q1-1.png"))),
)

== Part 2
=== Flooding Process
+ Start with putting all labeled pixel into the priority queue.
+ Reapetedly pop the pixel with the highest priority from the queue. 
+ The priority of given pixel $p$ is determined by the following formula:
$ "priority" = "Distance("p", mean("p"'s 25-neighbors")) + 2 dot "Variance("p"'s 25-neighbors)"+ "Sobel("p")" $
4. The Sobel operator is implemented following the definition in #link("https://en.wikipedia.org/wiki/Sobel_operator")[wikipedia].
+ If the pixel is not labeled, check its neighbors. If the neighbor is labeled,
  assign the label to the pixel. If there are multiple labels, assign the pixel as
  a boundary pixel.
+ If the pixel is labeled, skip it.
+ Put the pixel's neighbors into the queue.
+ If the queue is not empty, back to step 2.
+ Done.
#pagebreak()
== Result
#grid(
  rows: 3,
  gutter: 10pt,
  align: horizon,
  grid.cell(figure(image("results/img1_q1-2.png"))),
  grid.cell(figure(image("results/img2_q1-2.png"))),
  grid.cell(figure(image("results/img3_q1-2.png"))),
)
