# Solution Outline
1. In this challenge we try to calculate the average error of stock price estimation in a sliding time window.
2. To calculate that, we keep a queue that stores the total error and total number of non-ignorable item for everytime
stamp found in the sliding time window.
3. As we move forward the time window, we append new error and number of non-ignorable item at new time into the queue
and pop out the expired item that corresponds to the time falls out of the time window.
4. As we move the sliding window, we update the average error
5. So everytime, we are only reading chuck of the data from the text files into memory. If we read all the data from the
text files into memory at once, this will consumes lots of memory. Using the queue implementation here, we are saving lots
of memory.
6. For quick lookup for stock prices and corresponding predicted stock prices, we utilize dictionary data structure in
python for O(1) lookup.
