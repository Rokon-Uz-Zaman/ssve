# ssve
Super Simple Video Editor

The super simple video editor is an answer to the problem of quickly trimming and stacking video clips.  It is a python script which reads from a simple grammer file and then makes calls to ffmpeg to do the actual heavy lifting.

The grammer file uses the following format.

```
===sources===
name file_path
name2 file_path
===clips===
clip1 name start_timestamp end_timestamp
clip2 name2 start_timestamp end_timestamp
===timeline===
clip1 clip2
```

This will cut a clip out of the two source videos and then concatenate them together.  The example.ssve file in the repository provides a full example using two downloaded youtube videos.
