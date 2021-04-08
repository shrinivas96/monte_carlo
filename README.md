# IMU Tilt and Bias Estimation with Particle Filters


This document and repository is a small summary of what I understand of the concepts Monte Carlo Methods, Importance Sampling Principle and Particle Filters.

The main resources that I have followed are:

- "Monte Carlo Methods and Importance Sampling'' by Eric C. Anderson, written for the course Stat578C at U.C. Berkeley. Here is the [link to the document](http://ib.berkeley.edu/labs/slatkin/eriq/classes/guest_lect/mc_lecture_notes.pdf).

- "Particle Filters'' taught by Cyrill Stachniss for the course [Mobile Sensing and Robotics](https://youtube.com/playlist?list=PLgnQpQtFTOGQJXx-x0t23RmRbjp_yMb4v) at the University of Bonn and [SLAM Course](https://youtube.com/playlist?list=PLgnQpQtFTOGQrZ4O5QzbIHgl3b1JHimN_) at the  University of Freiburg. 

- Chapter 4 - Non-parametric Filters, of the book Probabilistic Robotics by Sebastian Thrun, Wolfram Burgard and Dieter Fox.

## Monte Carlo Methods
Monte Carlo Methods (MCM), developed by mathematicians Stanislaw Ulam and John von Neumann, are sample-based techniques to approximate properties of a probability distribution by repeated random sampling of the set. For state estimation purposes, we are interested in estimating the underlying probability distributions. 

We first look at finding the expectation of a function of a random variable, as we are often interested in some transformation of the state. 

Consider a random variable $X$ distributed according to some probability function $p_{X}(x)$, such that $p_{X}(x)$ is greater than $0$ for a set of values $\mathcal{A}$. The expectation of the random variable is given by:

<img src="https://render.githubusercontent.com/render/math?math=E[X] = \sum_{x \in \mathcal{A}} x p_X (x)">,

for a discrete random variable, and,

<img src="https://render.githubusercontent.com/render/math?math=E[X] = \int_{x \in \mathcal{A}} x p_X (x) dx">,

for a continuous random variable.


## Work in Progress. 
This document is incomplete and will be expanded more. 
The current work-around for writing math equations in GitHub Markdown was found from here: [A hack for showing LaTeX formulas in GitHub markdown.](https://gist.github.com/a-rodin/fef3f543412d6e1ec5b6cf55bf197d7b)