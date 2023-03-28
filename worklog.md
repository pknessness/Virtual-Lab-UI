# Work Log

## March 9 [1:00PM - 5:00PM]

Began working on project, got a basic outline of the framework, displaying videos at a speed, displaying multiple videos, and displaying videos that are at length (2 Hours)

## March 10 [4:00PM - 6:00PM]

Set up UI using pyQT5. Set up all the basic buttons, split files for simulation and main (UI). Also set up choosing a file directory and exporting files to the user's computer. Reorganized folders to better work with both videos and raw data.

## March 14 [1:00PM - 5:00PM]

Added more and different types of tests (Fatigue, Hardness, Charpy). Reorganized folders to be more condusive to this. Videos werent running fast enough, attempted to run things threaded to speed this up, however this ended in faults. Also began working with the time slider, to see if we could pick and choose where in the video the user is. This may end up being a massive change in the simulation code

## March 27 [10:00AM - 12:00PM] [4:00PM - 8:00PM]

Began looking into AWS, most optimal seems like Amazon S3. AWS will take a bit to load, so I next began working on the time skipping, fast forwarding problem. I experimented with a good few new rendering methods. I've figured out how I can skip to a specific frame, and am now working on getting a consistent framerate, no matter the speed of the computer itself, which will lead directly into the time-bar.

## March 28 [12:00AM - 1:00AM] [2:00AM - 3:30AM] [3:00PM - ?:00PM]

Working on multi-processes, and transferring data between two processes. May need to use threading instead.