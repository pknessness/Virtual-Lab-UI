# Work Log

## March 9 [1:00PM - 5:00PM]

Began working on project, got a basic outline of the framework, displaying videos at a speed, displaying multiple videos, and displaying videos that are at length (2 Hours)

## March 10 [4:00PM - 6:00PM]

Set up UI using pyQT5. Set up all the basic buttons, split files for simulation and main (UI). Also set up choosing a file directory and exporting files to the user's computer. Reorganized folders to better work with both videos and raw data.

## March 14 [1:00PM - 5:00PM]

Added more and different types of tests (Fatigue, Hardness, Charpy). Reorganized folders to be more condusive to this. Videos werent running fast enough, attempted to run things threaded to speed this up, however this ended in faults. Also began working with the time slider, to see if we could pick and choose where in the video the user is. This may end up being a massive change in the simulation code

## March 27 [10:00AM - 12:00PM] [4:00PM - 8:00PM]

Began looking into AWS, most optimal seems like Amazon S3. AWS will take a bit to load, so I next began working on the time skipping, fast forwarding problem. I experimented with a good few new rendering methods. I've figured out how I can skip to a specific frame, and am now working on getting a consistent framerate, no matter the speed of the computer itself, which will lead directly into the time-bar.

## March 28 [12:00AM - 1:00AM] [2:00AM - 3:30AM] [3:00PM - 6:00PM]

Working on multi-processes, and transferring data between two processes. May need to use threading instead. Fixed a number of bugs with the slider bar, processes, and threading. Still need to work on transferring data between the slider and the video, as my first attempt made everything incredibly slow.

## March 29 [12:30AM - 2:30AM]

AWS has loaded, have begun attempting to do light tests with streaming video from AWS. So far, the stream data I'm getting seems to be garbage. Need to figure out what's going wrong with getting the stream data. The second issue is that the stream data is incredibly slow. May need to set up a backup method to run this.

## March 31 [10:00PM - 2:00AM] April 1

Have set up a basic auto-download-dependencies framework
Also, am now running the videos purely from AWS, no local copies, and that works well, and at a reasonable speed (Slightly slow), but can likely be sped up.

Having major issues with time jumping. Time jumping seems to cause values out of range and a fault. Need to figure out whats happening there. May be a result of the PyQt5 multiprocessing methods. May need to pipeline or thread, or perhaps switch to an entirely pygame timejump method.

## April 3 [2:00PM - 3:00PM] [7:00PM - 8:30PM]

Had meeting with John, need him to give me randomizer +-. May also have him downgrade videos to 720p and see if it becomes faster that way. Need to figure out how to compile python file into one exe that is usable by anyone.

Beyond this, need to do time bar stuff for the pygame window, looking into libraries to help with that. Looking like theres something called PygameGUI I can use

## April 4 [5:00PM - 7:00PM]

Tried some things with the time bar gui, so far nothing that is what I am looking for. Attempted pygame_gui and thorpy. Thorpy seems slightly viable, but am going to try some others.

## April 5 [1:00PM - 3:00PM]

Pygame widgets seems to be working. I've set up a resizing, so it changes with the window size. Still need to set up time jumping. Also need to test 720p video.

## April 10 [2:00AM - 5:00AM] [10:30AM - 11:30AM] [2:00PM - 7:00PM]

Working more on time bar, it now reflects the positon of the video, but need video to freeze when the time bar is held, and reflect where it is dragged to. Having bugs with the closing windows, and bugs with the videos not playing all the way through. The time bar is now complete, minus the potential functionality of a preview.

Also worked more on building as a single exe, once I get something that seems to work on my computer, need to send to John. Having issues with some of the libraries being grabbed correctly.

Time bar is very slow, jumping takes an innane amount of time. Perhaps this will be fixed by the720p.

Also am able to compile into a single exe, but need John to test on a separate device to make sure this is usable by anyone.

Time bar looks a little better now, and with 720p its very very fast and absolutely usable.

## April 24 [2:00 PM - 3:00PM] [5:00PM - 7:00PM]

Meeting with john. 
Disabled time bar as it seems finnicky, but turns out it was just the zoom in being funky. Need to fix zoom in, but it seems the priority is on data randomization, so going to do that first

Finished data randomization, need to move all raw data onto the aws

Also need to have auto-file detection and auto-menu generation, worked on that a bit, need to finish

### Finished Entering All Times

## April 25 [12:30PM - 3:30PM]

Began indexing bucket to generate menu. Now adding a file will automatically add its menu entry. Added more error codes for raw data, and moved all of that to the AWS as well.

## April 27 [1:00PM - 2:00PM] (Release V1.0)

Wrote up a basic explanation on my code and what it does. Also emailed a bit with Professor Porter, the first person who will be testing the code.

## May 3 [1:30PM - 3:00PM]

Meeting with John, met with new guy (Eric?), and talked with him and John about releasing new versions, improvements, etc. Started working on subtitles and looking into permanent data storage on user computer

## May 4 [12:30PM - 2:00PM]

Working on subtitles. Seems to work, need to get the actual sub file from John or make one myself.

Also need to set it up with the aws.