#! /usr/bin/python
import sys
from collections import deque

class Solution:
  

  def worker(self):
    '''It seems the answer from the test has multiple errors of data rounding. As a result, I can't pass the test. For instance, if I do it manually
    by calculating the average error for a particular sliding time window. I got exactly same answer as my own output. But this is different from the
    test answer provided. For example, the sliding time window 120-123 for the test_1'''
    actualFile = sys.argv[2]
    predictFile = sys.argv[3]
    windowFile = sys.argv[1]
    comparisonFile = sys.argv[4]    
    actualFileInput = open(actualFile, 'r')
    predictFileInput = open(predictFile, 'r')
    windowFileInput = open(windowFile, 'r')
    window = int(windowFileInput.readline())
    windowFileInput.close()
    comparisonFileOutput = open(comparisonFile, 'w')
    x = actualFileInput.tell() # remember the first line position
    startTimeStamp = int(actualFileInput.readline().split('|')[0])  #get start time
    actualFileInput.seek(x) #go back to first line
    timeStamp = startTimeStamp
    totalNotIgnore = 0 #total number of non-ignore entries in current time window
    totalError = 0 #total error in current time window
    avgError = 0 #average error in current time window
    formatString = "%d|%d|%.2f\n" #format output string
    errorQueue = deque() # error queue that stores the error and number of entries that are not 'ignore' at particular time stamp
    endTimeStamp = startTimeStamp + window - 1
    while timeStamp <= endTimeStamp:
      timeStamp, notIgnore, error = self.readLinesForTime(actualFileInput, predictFileInput, timeStamp)
      errorQueue.append((notIgnore, error)) #push the current error and number of non-ignore entries into the queue
      totalNotIgnore += notIgnore #add number of non-ignore entries to the total count
      totalError += error #add current error to the total error
    avgError = (totalError / totalNotIgnore) # calculate the average error at current time window
    comparisonFileOutput.write(formatString % (startTimeStamp, endTimeStamp, avgError)) #write to output
    startTimeStamp += 1 #slide time window
    endTimeStamp += 1 #slide time window
    while timeStamp != 'end-of-file':
      timeStamp, notIgnore, error = self.readLinesForTime(actualFileInput, predictFileInput, timeStamp)
      errorQueue.append((notIgnore, error)) #push the current error and number of non-ignore entries into the queue
      prevNotIgnore, prevError = errorQueue.popleft() #pop the item whose time is not in current window anymore
      totalError = totalError - prevError + error # deduct the error that not in current window anymore and add new error
      totalNotIgnore = totalNotIgnore - prevNotIgnore + notIgnore # deduct the number of non-ignore entries not in current window anymore, add new
      avgError = totalError / totalNotIgnore # calculate the average error for current time window
      comparisonFileOutput.write(formatString % (startTimeStamp, endTimeStamp, avgError)) #write to output
      startTimeStamp += 1 #slide the time window
      endTimeStamp += 1 #slide the time window
    
    

  def readLinesForTime(self, actualFileInput, predictFileInput, timeStamp):
    ''' read lines corresponding to timeStamp and calculate the errors and number of non-ignore entries'''
#    print timeStamp
    actualDict = {}
    predictDict = {}
    errorDict = {}

    rowString = predictFileInput.readline()

    while rowString != None and rowString != "" and rowString != '\n' and int(rowString.split('|')[0]) == timeStamp:
      stockName = rowString.split('|')[1]
      stockPrice = float(rowString.split('|')[2])
      predictDict[stockName] = stockPrice
      x = predictFileInput.tell()
      rowString = predictFileInput.readline()
    if rowString != None and rowString != "" and rowString != '\n':
      predictFileInput.seek(x)

    rowString = actualFileInput.readline()
    while rowString != None and rowString != "" and rowString != '\n' and int(rowString.split('|')[0]) == timeStamp:
      stockName = rowString.split('|')[1]
      stockPrice = float(rowString.split('|')[2])
      actualDict[stockName] = stockPrice
      x = actualFileInput.tell()
      rowString = actualFileInput.readline()
    if rowString != None and rowString != "" and rowString != '\n':
      timeStamp = int(rowString.split('|')[0])
      actualFileInput.seek(x)
    else:
      timeStamp = 'end-of-file'
        
    for key in actualDict:
      if key not in predictDict:
        errorDict[key] = 'ignore'
      else:
        errorDict[key] = abs(actualDict[key] - predictDict[key])
    notIgnore = 0
    error = 0
    for key in errorDict:
      if errorDict[key] != 'ignore':
        notIgnore += 1
        error += errorDict[key]
#    print len(errorDict), notIgnore, error
#    for key in actualDict:
#      if key not in predictDict:
#        print key, actualDict[key], 'NA', errorDict[key]
#      else:
#        print key, actualDict[key], predictDict[key], errorDict[key]
 
    return timeStamp, notIgnore, error

if __name__ == "__main__":
  sol = Solution()
  sol.worker()
