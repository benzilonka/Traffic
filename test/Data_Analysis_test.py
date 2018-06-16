import unittest
import Data_Analysis

class TestDataAnalysis (unittest.TestCase):

    def test_addTTC(self):
        vehicles = {'objects' : ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [300, 200, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.add_ttc(vehicles,5)
        self.assertEqual(result['objects'][0]['distance'],0)
        self.assertEqual(result['objects'][1]['distance'],0)
        self.assertEqual(result['objects'][2]['distance'],0)
        self.assertEqual(result['objects'][0]['ttc'],-1)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],-1)
        vehicles = {'objects' : ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 20, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 550, 0,0], 'speed' : 30, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 350, 0,0], 'speed' : 10, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.add_ttc(vehicles,5)
        self.assertEqual(result['objects'][0]['distance'],30)
        self.assertEqual(result['objects'][1]['distance'],0)
        self.assertEqual(result['objects'][2]['distance'],40)
        self.assertEqual(result['objects'][0]['ttc'],3/5)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],-1)
        vehicles = {'objects' : ({ 'bounding_box' : [100, 50, 0,0], 'speed' : 103, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 200, 0,0], 'speed' : 97, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 500, 0,0], 'speed' : 93, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.add_ttc(vehicles,5)
        self.assertEqual(result['objects'][0]['distance'],30)
        self.assertEqual(result['objects'][1]['distance'],60)
        self.assertEqual(result['objects'][2]['distance'],0)
        self.assertEqual(result['objects'][0]['ttc'],1)
        self.assertEqual(result['objects'][1]['ttc'],3)
        self.assertEqual(result['objects'][2]['ttc'],-1)
        vehicles = {'objects' : ({ 'bounding_box' : [100, 50, 0,0], 'speed' : 0, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 200, 0,0], 'speed' : 6, 'distance' : 0, 'ttc': 0},{ 'bounding_box' : [100, 500, 0,0], 'speed' : 5, 'distance' : 0, 'ttc': 0})}
        result = Data_Analysis.add_ttc(vehicles,5)
        self.assertEqual(result['objects'][0]['distance'],30)
        self.assertEqual(result['objects'][1]['distance'],60)
        self.assertEqual(result['objects'][2]['distance'],0)
        self.assertEqual(result['objects'][0]['ttc'],-1)
        self.assertEqual(result['objects'][1]['ttc'],-1)
        self.assertEqual(result['objects'][2]['ttc'],-1)
        
        

    def test_calcTTC(self):
        vehicles = ({ 'bounding_box' : [100, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [300, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [400, 200, 0,0], 'speed' : 10})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),-1)
        vehicles = ({ 'bounding_box' : [200, 400, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 100, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 130, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 0},{ 'bounding_box' : [200, 300, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 250, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 205, 0,0], 'speed' : 10})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 400, 0,0], 'speed' : 9})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),-1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 20},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 400, 0,0], 'speed' : 10})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),4/5)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0], 'speed' : 20},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 200, 0,0], 'speed' : 10},{ 'bounding_box' : [200, 400, 0,0], 'speed' : 12})
        self.assertEqual(Data_Analysis.calc_ttc(vehicles[0],vehicles,5),1)              
    
    def test_getDistance(self):
        vehicles = ({ 'bounding_box' : [100, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [300, 200, 0,0]},{ 'bounding_box' : [400, 200, 0,0]})
        self.assertEqual(Data_Analysis.get_distance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.get_distance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 400, 0,0]},{ 'bounding_box' : [200, 100, 0,0]},{ 'bounding_box' : [200, 130, 0,0]},{ 'bounding_box' : [200, 200, 0,0]})
        self.assertEqual(Data_Analysis.get_distance(vehicles[0],vehicles),0)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 300, 0,0]},{ 'bounding_box' : [200, 250, 0,0]},{ 'bounding_box' : [200, 205, 0,0]})
        self.assertEqual(Data_Analysis.get_distance(vehicles[0],vehicles),1)
        vehicles = ({ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 200, 0,0]},{ 'bounding_box' : [200, 330, 0,0]})
        self.assertEqual(Data_Analysis.get_distance(vehicles[0],vehicles),130/5)        
        
    
    def test_areInSameLane(self):
        self.assertTrue(Data_Analysis.are_in_same_lane(85,80))
        self.assertFalse(Data_Analysis.are_in_same_lane(0,30))
        self.assertTrue(Data_Analysis.are_in_same_lane(0,22))
        self.assertFalse(Data_Analysis.are_in_same_lane(40,120))
        self.assertFalse(Data_Analysis.are_in_same_lane(-30,5))

    def test_is_vehicle_passed_in_red_light(self): 
        lanes = {"right": [49, 60], "forward": [38, 49], "left": [27, 38]}
        frame1 = {'objects': [{'confidence': 0.8, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 9.932450653113678, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [48, 232, 90, 132], 'new': False, 'counted': False}], 'light_status': {'right' :'red','forward' :'red','left':'red'}, 'frame_index': 6348724}
        frame2 = {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 9.404605335094026, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [48, 234, 92, 132], 'new': False, 'counted': False}],  'light_status': {'right' :'grean','forward' :'red','left':'red'}, 'frame_index': 6348732}
        frame3 = {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [48, 236, 91, 131], 'new': False, 'counted': False}], 'light_status': {'right' :'red','forward' :'red','left':'red'}, 'frame_index': 6348741}
        frame4 = {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 2.367083004736198, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [48, 239, 92, 132], 'new': False, 'counted': False}],  'light_status': {'right' :'red','forward' :'red','left':'red'},'frame_index': 6348747}
        frame5 = {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [48, 240, 91, 131], 'new': False, 'counted': False}],  'light_status': {'right' :'red','forward' :'red','left':'red'}, 'frame_index': 6348753} 
        
        frame1 = Data_Analysis.is_vehicle_passed_in_red_light(frame1, None, 200, lanes)
        self.assertFalse(frame1['objects'][0]['passed_in_red'])
        frame2 = Data_Analysis.is_vehicle_passed_in_red_light(frame2, frame1, 200, lanes)
        self.assertFalse(frame2['objects'][0]['passed_in_red'])
        frame3 = Data_Analysis.is_vehicle_passed_in_red_light(frame3, frame2, 235, lanes)
        self.assertTrue(frame3['objects'][0]['passed_in_red'])
        frame4 = Data_Analysis.is_vehicle_passed_in_red_light(frame4, frame3, 238, lanes)
        self.assertTrue(frame4['objects'][0]['passed_in_red'])
        frame5= Data_Analysis.is_vehicle_passed_in_red_light(frame5, frame4, 238, lanes)
        self.assertFalse(frame5['objects'][0]['passed_in_red'])

    def test_add_zigzag_count(self):
        lanes = {"right": [49, 60], "forward": [38, 49], "left": [27, 38]}
        frames = [{'objects': [{'confidence': 0.8, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 9.932450653113678, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [524, 232, 90, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 5, 'speed': 7.883500926853487, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [377, 326, 68, 50], 'new': False, 'counted': True}, {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 8, 'speed': 6.006274599496227, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [424, 280, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348724},
        {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 9.404605335094026, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 234, 92, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 6, 'speed': 7.46454395779037, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [376, 328, 68, 50], 'new': False, 'counted': True}, {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 9, 'speed': 5.687080068679144, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [424, 281, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348732},
        {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 230, 91, 131], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 7, 'speed': 6.193790879731843, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [374, 329, 68, 51], 'new': False, 'counted': True}, {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 0, 'speed': 18.3427258131377, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [414, 289, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348741},
        {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 2.367083004736198, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 232, 92, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 8, 'speed': 8.171683387944562, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [373, 330, 69, 51], 'new': False, 'counted': True}, {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 18.43761832602244, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [413, 290, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348747},
        {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 232, 91, 131], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 8, 'speed': 8.204357854743904, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [372, 331, 70, 52], 'new': False, 'counted': True}, {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 18.51134117483986, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [414, 290, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348753},  
        {'objects': [{'confidence': 0.7, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 232, 91, 134], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 10, 'speed': 8.614160325384688, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [370, 332, 70, 52], 'new': False, 'counted': True}, {'confidence': 0.76, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 23.706263884080034, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [410, 292, 52, 35], 'new': False, 'counted': False}], 'frame_index': 6348759}
        ]
        frames[0] = Data_Analysis.add_zigzag_count(frames[0], None, 1, 0)
        self.assertTrue(frames[0]['objects'][0]['change_lane_count']==0)
        self.assertFalse(frames[0]['objects'][0]['against_direction_flag'])
        frames[1] = Data_Analysis.add_zigzag_count(frames[1], frames[0], 1, 0)
        self.assertTrue(frames[1]['objects'][0]['change_lane_count']==1)
        self.assertFalse(frames[1]['objects'][0]['against_direction_flag'])
        frames[2] = Data_Analysis.add_zigzag_count(frames[2], frames[1], 1, 0)
        self.assertTrue(frames[2]['objects'][0]['change_lane_count']==1)
        self.assertTrue(frames[2]['objects'][0]['against_direction_flag'])
        frames[3] = Data_Analysis.add_zigzag_count(frames[3], frames[2], 1, 0)
        self.assertTrue(frames[3]['objects'][0]['change_lane_count']==1)
        self.assertFalse(frames[3]['objects'][0]['against_direction_flag'])
        frames[4]= Data_Analysis.add_zigzag_count(frames[4], frames[3], 1, 0)
        self.assertTrue(frames[4]['objects'][1]['change_lane_count']==4)
        self.assertFalse(frames[4]['objects'][1]['against_direction_flag'])
    
    
if __name__=='__main__':
    unittest.main()