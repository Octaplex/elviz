Elviz is a set of utilities for visualizing electromagnetic phenomena. Thank
you — thank you very much — for checking it out.

# Installation

Elviz depends only on VPython and Python 2.7.9.
VPython provides downloads for
[windows](http://vpython.org/contents/download_windows.html),
[mac](http://vpython.org/contents/download_mac.html), and
[linux](http://vpython.org/contents/download_linux.html).

There isn't an installer yet, so to run Elviz you'll have to clone this repo.

# Running

The `bin/elviz` executable will import and run the `go` function in the `elviz`
module. To run it, you can:

- execute it directly in a shell
- open it in VIDLE and click `Run > Run Module`

# Hacking

The `go` function in the file `elviz/__init__.py` is currently the main
entrypoint. It contains some objects that you can play around with, but it's
much more fun to make your own scene! Some tips:

- You can change properties of the scene by editing the setup section; for
  example, you can change the color by editing the `BField` declaration (note:
  while colors are in RGB format, each value ranges from 0 to 1).
- Make sure you add any inducers you make to the `BField` itself, whatever you
  name it (in the example, it is called `B`).
- The call to `draw` takes the following arguments, in order:
    - Origin (vector)
    - Size (vector in <l, w, h> or scalar if all components are the same)
    - Step (vector or scalar; how often to draw field lines)
    - Radius (radius of drawing); leave empty for a rectangular drawing

The following magnetic inducers are supported (look at `shapes.py` for more
information):

- Wire
- Coil
- Bar
- Particle
