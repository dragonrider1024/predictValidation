#! /usr/bin/python
import sys
from collections import deque

class Solution:
  

  def worker(self):
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
    startTimeStamp = int(actualFileInput.readline().split('|')[0])
    actualFileInput.seek(x)
    timeStamp = startTimeStamp
    totalNotIgnore = 0
    totalError = 0
    formatString = "%d|%d|%.2f\n"
    errorQueue = deque()
    while timeStamp < startTimeStamp + window:
      timeStamp, notIgnore, error = self.readLinesForTime(actualFileInput, predictFileInput, timeStamp)
      errorQueue.append((notIgnore, error))
      totalNotIgnore += notIgnore
      totalError += error
    comparisonFileOutput.write(formatString % (startTimeStamp, startTimeStamp + window - 1, totalError / totalNotIgnore))
    startTimeStamp += 1
    while timeStamp != 'end-of-file':
      timeStamp, notIgnore, error = self.readLinesForTime(actualFileInput, predictFileInput, timeStamp)
      errorQueue.append((notIgnore, error))
      prevNotIgnore, prevError = errorQueue.popleft()
      totalNotIgnore = totalNotIgnore - prevNotIgnore + notIgnore
      totalError = totalError - prevError + error
      comparisonFileOutput.write(formatString % (startTimeStamp, startTimeStamp + window - 1, totalError / totalNotIgnore))
      startTimeStamp += 1
      

    
    
    

  def readLinesForTime(self, actualFileInput, predictFileInput, timeStamp):
    actualDict = {}
    predictDict = {}
    errorDict = {}

    rowString = predictFileInput.readline()
    while rowString and rowString != "" and rowString != '\n' and int(rowString.split('|')[0]) == timeStamp:
      stockName = rowString.split('|')[1]
      stockPrice = float(rowString.split('|')[2])
      predictDict[stockName] = stockPrice
      x = predictFileInput.tell()
      rowString = predictFileInput.readline()
    if rowString and rowString != "" and rowString != '\n':
      predictFileInput.seek(x)

    rowString = actualFileInput.readline()
    while rowString and rowString != "" and rowString != '\n' and int(rowString.split('|')[0]) == timeStamp:
      stockName = rowString.split('|')[1]
      stockPrice = float(rowString.split('|')[2])
      actualDict[stockName] = stockPrice
      x = actualFileInput.tell()
      rowString = actualFileInput.readline()
    if rowString and rowString != "" and rowString != '\n':
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
    return timeStamp, notIgnore, error

if __name__ == "__main__":
  sol = Solution()
  sol.worker()
