# tasq
Receive user job requests inside queue and dequeue / process the jobs.
Aims to be used for homework by students for aggressive time sharing.

# Usage
Run `tasq_server.py` alone and run `tasq` with next usage.

`$ tasq <enq | list> [command] [output]`

## Example
```
$ tasq enq nvcc --output-file matmul matmul.cu output
$ tasq enq ./matmul output2
$ tasq list
```

# License
GPL v3

# Author
SeongJae Park (sj38.park@gmail.com)
