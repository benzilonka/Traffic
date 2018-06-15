import unittest
from server.DBL import *

class TestDB (unittest.TestCase):
    dbl = DBL.DB_Layer()
    def test_empty_all_tables(self):
        self.dbl.check_tables()
        # Connect to the database
        vidio_info = {'name' :'aaa'}
        self.dbl.add_dataset(1,vidio_info)
        self.dbl.empty_all_tables()
        simulation = self.dbl.get_datasets(0)
        junction = self.dbl.get_junctions()
        vidio_info = self.dbl.get_datasets(1)
        self.assertEqual(simulation,())
        self.assertEqual(junction,())
        self.assertEqual(vidio_info,())        


    def test_drop_all_tables(self):
        # Connect to the database
        self.dbl.drop_all_tables()
        self.assertFalse(self.dbl.check_table_exists('junction_info'))
        self.assertFalse(self.dbl.check_table_exists('vidio_info'))
        self.assertFalse(self.dbl.check_table_exists('simulation_info'))
        



    def test_check_tables(self):
        self.dbl.check_tables()
        self.assertTrue(self.dbl.check_table_exists('junction_info'))
        self.assertTrue(self.dbl.check_table_exists('vidio_info'))
        self.assertTrue(self.dbl.check_table_exists('simulation_info'))

    def test_add_junction(self):
        self.dbl.empty_all_tables()
        self.assertEqual( self.dbl.get_junctions(),())
        junction1 = {'name' :'aaa', 'lat' : 21.1111, 'lon' : 31.3333}
        self.dbl.add_junction(junction1)
        junctions = [{'id' : 1, 'name' :'aaa', 'lat' : 21.1111, 'lng' : 31.3333}]
        self.assertEqual( self.dbl.get_junctions(),junctions)
        junction2 = {'name' :'bbb', 'lat' : 21.1111, 'lon' : 31.3333}
        junction3 = {'name' :'ccc', 'lat' : 21.1111, 'lon' : 31.3333}
        junctions = [{'id' : 1, 'name' :'aaa', 'lat' : 21.1111, 'lng' : 31.3333},{'id' : 2, 'name' :'bbb', 'lat' : 21.1111, 'lng' : 31.3333},{'id' : 3, 'name' :'ccc', 'lat' : 21.1111, 'lng' : 31.3333}]
        self.dbl.add_junction(junction2)
        self.dbl.add_junction(junction3)
        self.assertEqual(self.dbl.get_junctions(),junctions)
   
    def test_delete_junction(self):
        self.dbl.empty_all_tables()
        junction1 = {'name' :'aaa', 'lat' : 21.1111, 'lon' : 31.3333}
        junction2 = {'name' :'bbb', 'lat' : 21.1111, 'lon' : 31.3333}
        junction3 = {'name' :'ccc', 'lat' : 21.1111, 'lon' : 31.3333}
        self.dbl.add_junction(junction1)
        self.dbl.add_junction(junction2)
        self.dbl.add_junction(junction3)
       
        print(self.dbl.get_junctions())
        self.dbl.delete_junction_db(3)
        print('junctions')
        print(self.dbl.get_junctions())
        junctions2 = [{'id' : 1, 'name' :'aaa', 'lat' : 21.1111, 'lng' : 31.3333}, {'id' : 2, 'name' :'bbb', 'lat' : 21.1111, 'lng' : 31.3333}]
        self.assertEqual(self.dbl.get_junctions(),junctions2)
        self.dbl.delete_junction_db(4)
        junctions2 = [{'id' : 1, 'name' :'aaa', 'lat' : 21.1111, 'lng' : 31.3333}, {'id' : 2, 'name' :'bbb', 'lat' : 21.1111, 'lng' : 31.3333}]
        self.assertEqual(self.dbl.get_junctions(),junctions2)
        self.dbl.delete_junction_db(3)
        junctions2 = [{'id' : 1, 'name' :'aaa', 'lat' : 21.1111, 'lng' : 31.3333}, {'id' : 2, 'name' :'bbb', 'lat' : 21.1111, 'lng' : 31.3333}]
        self.assertEqual(self.dbl.get_junctions(),junctions2)

   
    def test_add_dataset(self):
        self.dbl.empty_all_tables()
        self.assertEqual(self.dbl.get_datasets(1),())
        vidio_info1 = {'name': 'Aa'}
        vidio_infos = [{'id' : 1, 'junction_id' : 1, 'name': 'Aa'}]
        self.dbl.add_dataset(1,vidio_info1)
        self.assertEqual(self.dbl.get_datasets(1),vidio_infos)
        vidio_info2 = {'name': 'Bb'}
        vidio_info3 = {'name': 'Cc'}
        self.dbl.add_dataset(2,vidio_info2)
        self.dbl.add_dataset(2,vidio_info3)
        vidio_infos = [{'id' : 2, 'junction_id' : 2, 'name': 'Bb'},{'id' : 3, 'junction_id' : 2, 'name': 'Cc'}]
        self.assertEqual(self.dbl.get_datasets(2),vidio_infos)
        print('::::::::::::::::::::::::::::simul:::::::::::::::::::::::::::::::')
        print(self.dbl.get_datasets(0))
        self.assertEqual(self.dbl.get_datasets(0),())
        simulation1 = {'name' : 'Aa', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'aaa'}
        self.dbl.add_dataset(0,simulation1)
        print('::::::::::::::::::::::::::::simul:::::::::::::::::::::::::::::::')
        print(self.dbl.get_datasets(0))
        simulations = [{'id' : 1 ,'name' : 'Aa', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'aaa'}]
        simulation2 = {'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'}
        
        self.assertEqual(self.dbl.get_datasets(0),simulations)
        self.dbl.add_dataset(0,simulation2)
        simulation3 = {'name' : 'Cc', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}
        self.dbl.add_dataset(0,simulation3)
        simulations = [{'id' : 1 ,'name' : 'Aa', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'aaa'},{'id' : 2 ,'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'},{'id' : 3 ,'name' : 'Cc', 'duration' : 30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}]
        self.assertEqual(self.dbl.get_datasets(0),simulations)
       
        

    
    def test_delete_simulation(self):
        vidio_info1 = {'name': 'Aa'}
        
        self.dbl.add_dataset(1,vidio_info1)        
        vidio_info2 = {'name': 'Bb'}
        vidio_info3 = {'name': 'Cc'}
        self.dbl.add_dataset(2,vidio_info2)
        self.dbl.add_dataset(2,vidio_info3)        
        simulation1 = {'name' : 'Aa', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'aaa'}
        self.dbl.add_dataset(0,simulation1)        
        simulation2 = {'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'}
        self.dbl.add_dataset(0,simulation2)        
        simulation3 = {'name' : 'Cc', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}
        self.dbl.add_dataset(0,simulation3) 

        self.dbl.delete_simulation(1)
        simulations = [{'id' : 2 ,'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'},{'id' : 3 ,'name' : 'Cc', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}]
        self.assertEqual(self.dbl.get_datasets(0),simulations)
        self.dbl.delete_simulation(4)
        simulations = [{'id' : 2 ,'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'},{'id' : 3 ,'name' : 'Cc', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}]
        self.assertEqual(self.dbl.get_datasets(0),simulations)
        self.dbl.delete_simulation(1)
        simulations = [{'id' : 2 ,'name' : 'Bb', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'bbb'},{'id' : 3 ,'name' : 'Cc', 'duration' :30, 'cars_per_second' : 30, 'vehicle_info' : 'ccc'}]
        self.assertEqual(self.dbl.get_datasets(0),simulations)
        

    
    def test_delete_vidio_info(self):
        self.dbl.delete_vidio_info(3)
        vidio_infos = [{'id' : 2, 'junction_id' : 2, 'name': 'Bb'}]
        self.assertEqual(self.dbl.get_datasets(2),vidio_infos)
        self.dbl.delete_vidio_info(4)
        vidio_infos = [{'id' : 2, 'junction_id' : 2, 'name': 'Bb'}]
        self.assertEqual(self.dbl.get_datasets(2),vidio_infos)
        self.dbl.delete_vidio_info(3)
        vidio_infos = [{'id' : 2, 'junction_id' : 2, 'name': 'Bb'}]
        self.assertEqual(self.dbl.get_datasets(2),vidio_infos)
        self.dbl.delete_vidio_info(1)        
        self.assertEqual(self.dbl.get_datasets(1),())


        
        
   

    
if __name__=='__main__':
    unittest.main()