import unittest
import Data_Analysis

class TestDataAnalysis (unittest.TestCase):

    def test_addTTC(self):
        vehicles = {'objects' : ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [300, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.addTTC(vehicles)
        self.assertEqual(result['objects'][0]['distance'],0)
        self.assertEqual(result['objects'][1]['distance'],0)
        self.assertEqual(result['objects'][2]['distance'],0)
        self.assertEqual(result['objects'][0]['ttc'],-1)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],-1)
        vehicles = {'objects' : ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 450, 0,0], 'speed' : 30, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 350, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.addTTC(vehicles)
        self.assertEqual(result['objects'][0]['distance'],30)
        self.assertEqual(result['objects'][1]['distance'],0)
        self.assertEqual(result['objects'][2]['distance'],20)
        self.assertEqual(result['objects'][0]['ttc'],3)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],2)
        vehicles = {'objects' : ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 5, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 450, 0,0], 'speed' : 0, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 350, 0,0], 'speed' : 15, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.addTTC(vehicles)
        self.assertEqual(result['objects'][0]['distance'],30)
        self.assertEqual(result['objects'][1]['distance'],0)
        self.assertEqual(result['objects'][2]['distance'],20)
        self.assertEqual(result['objects'][0]['ttc'],-1)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],20/15)
        

    def test_calcTTC(self):
        vehicles = ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [300, 200, 0,0]},{ 'bounding_box' : [400, 200, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),-1)
        vehicles = ({ 'bounding_box' : [200, 400, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 100, 0,0]},{ 'bounding_box' : [200, 130, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 0},{ 'bounding_box' : [200, 300, 0,0]},{ 'bounding_box' : [200, 250, 0,0]},{ 'bounding_box' : [200, 205, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 430, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 20},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 330, 0,0]})
        self.assertEqual(Data_Analysis.calcTTC(vehicles[0],vehicles),130/5/20)              
    
    def test_getDistance(self):
        vehicles = ({ 'bounding_box' : [100, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [300, 200, 0,0]},{ 'bounding_box' : [400, 200, 0,0]})
        self.assertEqual(Data_Analysis.getDistance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.getDistance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 400, 0,0]},{ 'bounding_box' : [200, 100, 0,0]},{ 'bounding_box' : [200, 130, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.getDistance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 300, 0,0]},{ 'bounding_box' : [200, 250, 0,0]},{ 'bounding_box' : [200, 205, 0,0]})
        self.assertEqual(Data_Analysis.getDistance(vehicles[0],vehicles),1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 330, 0,0]})
        self.assertEqual(Data_Analysis.getDistance(vehicles[0],vehicles),130/5)        
        
    
    def test_areInSameLane(self):
        self.assertTrue(Data_Analysis.areInSameLane(85,90))
        self.assertFalse(Data_Analysis.areInSameLane(0,30))
        self.assertTrue(Data_Analysis.areInSameLane(0,22))
        self.assertFalse(Data_Analysis.areInSameLane(40,120))
        self.assertFalse(Data_Analysis.areInSameLane(-30,5))

    
    
if __name__=='__main__':
    unittest.main()