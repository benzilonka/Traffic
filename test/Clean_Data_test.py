import unittest

from server.Clean_Data import *

class TestCleanData (unittest.TestCase):

    def test_checkForDirection(self):
        locFrom = [2,4]
        locTo = [1, 5]
        self.assertEqual(checkForDirection(locFrom,locTo,0),'down')
        self.assertEqual(checkForDirection(locFrom,locTo,1),'up')
        locTo = [2, 4]
        self.assertEqual(checkForDirection(locFrom,locTo,0),'unknown')
        self.assertEqual(checkForDirection(locFrom,locTo,1),'unknown')

    def test_checkIfLinear(self):
        locFrom = [2,4]
        locTo = [3,2]
        direction = 'up'
        self.assertTrue(checkIfLinear(locFrom, locTo, direction, 0))
        self.assertFalse(checkIfLinear(locFrom, locTo, direction, 1))
        direction = 'down'
        self.assertFalse(checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(checkIfLinear(locFrom, locTo, direction, 1))
        locTo = [2, 2]
        direction = 'up'
        self.assertTrue(checkIfLinear(locFrom, locTo, direction, 0))
        direction = 'down'
        self.assertTrue(checkIfLinear(locFrom, locTo, direction, 0))
    
    def test_checkInRangeAndFit(self):
        self.assertEqual(checkInRangeAndFit(1,3,2),2)
        self.assertEqual(checkInRangeAndFit(3,1,2),2)
        self.assertEqual(checkInRangeAndFit(1,3,4),3)
        self.assertEqual(checkInRangeAndFit(3,1,4),3)
        self.assertEqual(checkInRangeAndFit(1,3,0),1)
        self.assertEqual(checkInRangeAndFit(3,1,0),1)

        self.assertEqual(checkInRangeAndFit(0,3,2),2)
        self.assertEqual(checkInRangeAndFit(3,-1,2),2)
        self.assertEqual(checkInRangeAndFit(-1,3.6,4),3.6)
        self.assertEqual(checkInRangeAndFit(3,1,4.1),3)
        self.assertEqual(checkInRangeAndFit(-1,3,-2),-1)
        self.assertEqual(checkInRangeAndFit(3,-1.2,-1.3),-1.2)
    
    def test_checkForLegalSpeedAndFit(self):
        max_spead = 120.0/3.6
        self.assertEqual(checkForLegalSpeedAndFit(34),max_spead)
        self.assertEqual(checkForLegalSpeedAndFit(33),33)
        self.assertEqual(checkForLegalSpeedAndFit(32.676734),32.676734)
        self.assertEqual(checkForLegalSpeedAndFit(0), 0)
        self.assertEqual(checkForLegalSpeedAndFit(33.33), 33.33)

    def test_linearMovement(self):
        start = [2,3]
        end = [6,6]
        path = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]]
        result_path = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [7,7.7]
        end = [3,4]
        path = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        result_path = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [2,3]
        end = [6,6]
        path = [[2,3],[3,4],[2.3,4.4], [5,4.1],[6,6]]
        result_path = [[2,3],[3,4],[3,4.4], [5,4.4],[6,6]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [7,7.7]
        end = [4.4,4]
        path = [[7,7.7],[6.3,7.1],[5,7.8], [4.4,4.1],[5.1,4]]
        result_path = [[7,7.7],[6.3,7.1],[5,7.1], [4.4,4.1],[4.4,4]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [2,3]
        end = [6,6]
        path = [[2,3],[2,4],[2.3,4.4], [5,4.1],[6,6]]
        result_path = [[2,3],[2,4],[2.3,4.4], [5,4.4],[6,6]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [7,7.7]
        end = [4.4,4]
        path = [[7,7.7],[6.3,7.7],[5,7.6], [4.4,4.1],[5.1,4]]
        result_path = [[7,7.7],[6.3,7.7],[5,7.6], [4.4,4.1],[4.4,4]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [7,7.7]
        end = [4.4,4]
        path = [[7,7.7],[6.3,8],[5,7.7], [4.4,4.1],[5.1,4]]
        result_path = [[7,7.7],[6.3,7.7],[5,7.7], [4.4,4.1],[4.4,4]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [2,3]
        end = [2,3]
        path = [[2,3],[2,3],[2,3],[2,3],[2,3]]
        result_path = [[2,3],[2,3],[2,3],[2,3],[2,3]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        start = [7,7.7]
        end = [7,7.7]
        path = [[7,7.7]]
        result_path = [[7,7.7]]
        self.assertEqual(linearMovement(start,end,path),result_path)
        # tests for the first part of the function (the if part)
        start = [2, 7.7]
        end = [12, 7.7]
        path = [[2,7.7], [3, 6], [8, 3], [2, 10], [12,7.7]]
        result_path = [[2,7.7], [3, 7.7], [8, 7.7], [8, 7.7], [12, 7.7]]
        self.assertEqual(linearMovement(start, end, path), result_path)
        start = [2, 7.7]
        end = [2, 20.3]
        path = [[2, 7.7], [3, 6], [8, 3], [2, 10], [2, 20.3]]
        result_path = [[2, 7.7], [2, 7.7], [2, 7.7], [2, 10], [2, 20.3]]
        self.assertEqual(linearMovement(start, end, path), result_path)
        start = [1, 12]
        end = [1, 12]
        path = [[1, 12], [1, 6], [25, 3], [2, 12], [1, 12]]
        result_path = [[1, 12], [1, 12], [1, 12], [1, 12], [1, 12]]
        self.assertEqual(linearMovement(start, end, path), result_path)
    
    def test_linearMovementHelper(self):
        vehiclesPath = [[2,3],[4,5],[3,6],[5,5],[4,4]]        
        vehiclesPath_result = [[2,3],[4,5],[4,6],[5,6],[5,6]]
        result = linearMovementHelper('up','up',vehiclesPath,0)
        self.assertEqual( result,vehiclesPath_result)
        vehiclesPath = [[7,6],[6,5],[7,4.5],[5,7],[7,8]]
        vehiclesPath_result = [[7,6],[6,5],[6,4.5],[5,4.5],[5,4.5]]
        result = linearMovementHelper('douwn','douwn',vehiclesPath,0)
        self.assertEqual( result,vehiclesPath_result)
        vehiclesPath = [[7, 6], [6, 5], [7, 4.5], [5, 7], [7, 8]]
        vehiclesPath_result = [[7, 6], [7, 5], [7, 4.5], [7, 4.5], [7, 4.5]]
        result = linearMovementHelper('up', 'douwn', vehiclesPath, 0)
        self.assertEqual(result, vehiclesPath_result)
        vehiclesPath = [[7, 6], [6, 5], [7, 4.5], [5, 7], [7, 8]]
        vehiclesPath_result = [[7, 6], [6, 6], [6, 6], [5, 7], [5, 8]]
        result = linearMovementHelper('douwn', 'up', vehiclesPath, 0)
        self.assertEqual(result, vehiclesPath_result)

    def test_checkForLegalDifferSpeed(self):
        spead_list = {}
        vehiclesPath_result = {}
        ans_speed = {}

        spead_list[111] = [1,2,3,4]
        spead_list[222] = [1,2,3,4]
        spead_list[333] = [1,2,3,4]
        vehiclesPath_result[111] = [[2,3],[3.3,4],[3.3,4.4], [6,5],[6,6]] 
        vehiclesPath_result[222] = [[100,70.7],[6.3,7.2],[5,6], [4.4,4.1],[3.3,4]]
        vehiclesPath_result[333] = [[2,3],[3,4],[3,4.1], [5,4.4],[120.5,30]]
        ans_speed[111] = checkForLegalDifferSpeed(spead_list[111],vehiclesPath_result[111])
        ans_speed[222] = checkForLegalDifferSpeed(spead_list[222],vehiclesPath_result[222])
        ans_speed[333] = checkForLegalDifferSpeed(spead_list[333],vehiclesPath_result[333])
        id = [111,222,333]
        
        for path in id:
            for place in range(len(vehiclesPath_result[path])-1):
                    spead_list[path][place] = calcDistance(vehiclesPath_result[path][place],vehiclesPath_result[path][place+1])/(1/15)
                    if(spead_list[path][place]> 120/3.6):
                        spead_list[path][place] = 120/3.6
        for path in id:
            for place in range(len(ans_speed[path])):
                self.assertTrue(-0.1 <= (ans_speed[path][place]- spead_list[path][place]) and (ans_speed[path][place]- spead_list[path][place])<=0.1)

    def test_normalizeData(self):
        vehiclesPath = {}
        vehiclesSpeed = {}
        vehiclesPath_result = {}
        vehiclesSpeed_result = {}
        vehiclesPath[111] = [[2,3],[3,4],[3.3,4.4],[5,5],[6,6]]
        vehiclesPath[222] = [[7,7.7],[6.3,7.1],[5,5],[4.4,4.1],[3,4]] 
        vehiclesPath[333] = [[2,3],[3,4],[2.3,4.4], [5,4.1],[6,6]]
        
        vehiclesPath_result[111] = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]] 
        vehiclesPath_result[222] = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        vehiclesPath_result[333] = [[2,3],[3,4],[3,4.4], [5,4.4],[6,6]]
       
        vehiclesSpeed[111] = [0.2,0.2003,0.2006,0.2008]
        vehiclesSpeed[222] = [0.2,0.1998,0.1995,0.1993]
        vehiclesSpeed[333] = [20.2,20.2003,20.2006,20.2004,20.2002]
        
        vehiclesSpeed_result[111] = [0.2,0.2003,0.2006,0.2008]
        vehiclesSpeed_result[222] = [0.2,0.1998,0.1995,0.1993]
        vehiclesSpeed_result[333] = [20.2,20.2003,20.2006,20.2004,20.2002]
       
        vehiclesPath_result = smoothData(vehiclesPath_result)
        ans_path, ans_spead = normalizeData(vehiclesPath, vehiclesSpeed)

        id =[111,222,333]
        for path in id:
            for place in range(len(ans_path[path])-1):
                        vehiclesSpeed_result[path][place] = calcDistance(vehiclesPath_result[path][place],vehiclesPath_result[path][place+1])/(1/15)
                        if(vehiclesSpeed_result[path][place]> 120/3.6):
                            vehiclesSpeed_result[path][place] = 120/3.6
        for path in id:
            for place in range(len(ans_path[path])):
                self.assertTrue(-0.0001 <= (ans_path[path][place][0]- vehiclesPath_result[path][place][0]) and (ans_path[path][place][0]- vehiclesPath_result[path][place][0])<=0.0001)
                self.assertTrue(-0.0001 <= (ans_path[path][place][1]- vehiclesPath_result[path][place][1]) and (ans_path[path][place][1]- vehiclesPath_result[path][place][1])<=0.0001)
        for path in id:
            for place in range(len(ans_spead[path])):        
                self.assertTrue(-0.1 <= (ans_spead[path][place]- vehiclesSpeed_result[path][place]) and (ans_spead[path][place]- vehiclesSpeed_result[path][place])<=0.1)

    
if __name__=='__main__':
    unittest.main()