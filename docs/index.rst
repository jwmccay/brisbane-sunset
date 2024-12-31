.. brisbane_sunset documentation master file, created by
   sphinx-quickstart on Mon Dec 30 20:40:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Brisbane Sunset Documentation
============================================

This documentation is a low-priority work-in-progress. It serves two purposes:

* Theory and API breadcrumbs
* A framework for better documentation if it is ever desired


Theory
=====

The idea behind the calculation is to send a ray from an observer to the sun and check if that ray intersects the terrain. The search starts at sunset and goes backwards in time until the ray is no longer blocked. Both time and intersection searches happen at discrete intervals. Time is only checked every minute and intersections are checked at a resolution specified by the user, which is usually around 100 m. This is relatively accurate given the resolution of the input data.

However, some improvements could be made for both speed and accuracy. A bisection search in the time domain would reduce the number of iterations, and a ray-tracing style intersection algorithm could remove the need for the user to carefully specify the number of points.

API
===

`time_blocked` is the core function. It calculates sunset time for a given point on a given day.

.. autofunction:: brisbane_sunset.dusk.time_blocked

.. toctree::
   :maxdepth: 2
   :caption: Contents:

