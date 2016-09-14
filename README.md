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

## On the command line

1. Navigate to the `elviz` directory, wherever you cloned it.
2. (*optional*) Modify the file `elviz.py` to your liking (see [hacking]).
3. Execute `python2 elviz.py` in a terminal (or whatever command your distro
   uses for python 2).

## In VIDLE

VPython comes with a modification of Python's IDLE, called VIDLE, that can also
be used to run Elviz:

1. Open `elviz.py`, wherever you stored it.
2. (*optional*) Modify the file to your liking (see [hacking])
3. Click `Run > Run Module` to launch the program.

# Hacking

The sample `elviz.py` contains some objects that you can play around with, but
it's much more fun to make your own scene! Some tips:

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
