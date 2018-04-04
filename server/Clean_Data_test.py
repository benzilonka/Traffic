import unittest
import Clean_Data

class TestCleanData (unittest.TestCase):

    def test_checkForDirection(self):
        locFrom = [2,4]
        locTo = [1, 5]
        self.assertEqual(Clean_Data.checkForDirection(locFrom,locTo,0),'down')
        self.assertEqual(Clean_Data.checkForDirection(locFrom,locTo,1),'up')
        locTo = [2, 4]
        self.assertEqual(Clean_Data.checkForDirection(locFrom,locTo,0),'unknown')
        self.assertEqual(Clean_Data.checkForDirection(locFrom,locTo,1),'unknown')

    def test_checkIfLinear(self):
        locFrom = [2,4]
        locTo = [3,2]
        direction = 'up'
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertFalse(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
        locTo = [2,4]
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
        locTo = [3,2]
        direction = 'down'
        self.assertFalse(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
        locTo = [2,4]
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
        direction = 'unknown'
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
        locTo = [3,2]
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 0))
        self.assertTrue(Clean_Data.checkIfLinear(locFrom, locTo, direction, 1))
    
    def test_checkInRangeAndFit(self):
        self.assertEqual(Clean_Data.checkInRangeAndFit(1,3,2),2)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,1,2),2)
        self.assertEqual(Clean_Data.checkInRangeAndFit(1,3,4),3)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,1,4),3)
        self.assertEqual(Clean_Data.checkInRangeAndFit(1,3,0),1)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,1,0),1)

        self.assertEqual(Clean_Data.checkInRangeAndFit(0,3,2),2)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,-1,2),2)
        self.assertEqual(Clean_Data.checkInRangeAndFit(-1,3.6,4),3.6)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,1,4.1),3)
        self.assertEqual(Clean_Data.checkInRangeAndFit(-1,3,-2),-1)
        self.assertEqual(Clean_Data.checkInRangeAndFit(3,-1.2,-1.3),-1.2)
    
    def test_checkForLegalSpeedAndFit(self):
        max_spead = 120.0/3.6
        self.assertEqual(Clean_Data.checkForLegalSpeedAndFit(34),max_spead)
        self.assertEqual(Clean_Data.checkForLegalSpeedAndFit(33),33)
        self.assertEqual(Clean_Data.checkForLegalSpeedAndFit(32.676734),32.676734)

    def test_linearMovement(self):
        start = [2,3]
        path = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]]
        result_path = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [7,7.7]
        path = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        result_path = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [2,3]
        path = [[2,3],[3,4],[2.3,4.4], [5,4.1],[6,6]]
        result_path = [[2,3],[3,4],[3,4.4], [5,4.4],[6,6]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [7,7.7]
        path = [[7,7.7],[6.3,7.1],[5,7.8], [4.4,4.1],[5.1,4]]
        result_path = [[7,7.7],[6.3,7.1],[5,7.1], [4.4,4.1],[4.4,4]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [2,3]
        path = [[2,3],[2,4],[2.3,4.4], [5,4.1],[6,6]]
        result_path = [[2,3],[2,4],[2.3,4.4], [5,4.4],[6,6]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [7,7.7]
        path = [[7,7.7],[6.3,7.7],[5,7.6], [4.4,4.1],[5.1,4]]
        result_path = [[7,7.7],[6.3,7.7],[5,7.6], [4.4,4.1],[4.4,4]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [2,3]
        path = [[2,3],[2,3],[2,3],[2,3],[2,3]]
        result_path = [[2,3],[2,3],[2,3],[2,3],[2,3]]
        self.assertEqual( Clean_Data.linearMovement(start,path),result_path)
        start = [7,7.7]
        path = [[7,7.7]]
        result_path = [[7,7.7]]
        self.assertEqual( Clean_Data.linearMovement(start,path),None)
    
    def test_checkForLegalDifferSpeed(self):
        maxSpeed_dif = ((120.0/3.6) / 1000 / 66.66666666666667)
        maxSpeed_dif = maxSpeed_dif * 66.66666666666667
        spead_list = [0.2,0.2003,0.2006,0.2008] 
        result_spead_list = [0.2,0.2003,0.2006,0.2008]  
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
        spead_list = [0.2,0.1998,0.1995,0.1993] 
        result_spead_list =[0.2,0.1998,0.1995,0.1993]   
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
        spead_list = [20.2,20.2003,20.2006,20.2004,20.2002] 
        result_spead_list = [20.2,20.2003,20.2006,20.2004,20.2002]  
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
        spead_list = [0.2,0.2003,0.2410,0.2008] 
        result_spead_list = [0.2,0.2003,0.2003+maxSpeed_dif,0.2008]  
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
        spead_list = [0.2,0.1594,0.1995,0.1993] 
        result_spead_list =[0.2,0.2-maxSpeed_dif,0.1995,0.1993] 
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
        spead_list = [0.2,] 
        result_spead_list = [0.2]  
        self.assertEqual( Clean_Data.checkForLegalDifferSpeed(spead_list),result_spead_list)
    def test_normalizeData(self):
       
        vehiclesPath = {}
        vehiclesSpeed = {}
        vehiclesPath_result = {}
        vehiclesSpeed_result = {}
        vehiclesPath[111] = [[2,3],[3,4],[3.3,4.4],[5,5],[6,6]]
        vehiclesPath[222] = [[7,7.7],[6.3,7.1],[5,5],[4.4,4.1],[3,4]] 
        vehiclesPath[333] = [[2,3],[3,4],[2.3,4.4], [5,4.1],[6,6]]
        vehiclesPath[444] = [[7,7.7]]
        vehiclesPath_result[111] = [[2,3],[3,4],[3.3,4.4], [5,5],[6,6]] 
        vehiclesPath_result[222] = [[7,7.7],[6.3,7.1],[5,5], [4.4,4.1],[3,4]]
        vehiclesPath_result[333] = [[2,3],[3,4],[3,4.4], [5,4.4],[6,6]]
        vehiclesPath_result[444] = None
        vehiclesSpeed[111] = [0.2,0.2003,0.2006,0.2008]
        vehiclesSpeed[222] = [0.2,0.1998,0.1995,0.1993]
        vehiclesSpeed[333] = [20.2,20.2003,20.2006,20.2004,20.2002]
        vehiclesSpeed[444] =  [0.2]
        vehiclesSpeed_result[111] = [0.2,0.2003,0.2006,0.2008]
        vehiclesSpeed_result[222] = [0.2,0.1998,0.1995,0.1993]
        vehiclesSpeed_result[333] = [20.2,20.2003,20.2006,20.2004,20.2002]
        vehiclesSpeed_result[444] = [0.2]
        ans_path, ans_spead = Clean_Data.normalizeData(vehiclesPath, vehiclesSpeed)
        self.assertEqual(ans_path, vehiclesPath_result)
        self.assertEqual(ans_spead, vehiclesSpeed_result)
    
if __name__=='__main__':
    unittest.main()