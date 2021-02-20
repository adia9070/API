import unittest
import requests

class TestApi(unittest.TestCase):
	

	def test_1_get(self):
		endpoint = 'http://127.0.0.1'
		#Getting all songs. Song already has some records
		r = requests.get("{}/get/song".format(endpoint))
		#200 should be code
		self.assertEqual(r.status_code, 200)
		#Length of reeceived JSON > 0 as song has some records
		self.assertNotEqual(len(r.json()), 0)

		#Getting single song
		r = r = requests.get("{}/get/song/1".format(endpoint))
		#Status code
		self.assertEqual(r.status_code, 200)
		#length of JSON
		self.assertEqual(len(r.json()), 1)
		#Received JSON id should be 1
		self.assertEqual(r.json()[0]['id'], 1)

		#When calling Wrong API end point
		r = requests.get("{}/get/songs".format(endpoint))
		#Should get 400
		self.assertEqual(r.status_code, 400)


	def test_2_create(self):
		endpoint = 'http://127.0.0.1'
		r1 = requests.get("{}/get/podcast".format(endpoint))
		#talking latest max  podcast id so that we can create new records
		id = max([i['id'] for i in r1.json()])
		initial_count = len(r1.json())
		json_data = {
			"id":id+1, 
			"name":"Happiness for life 4", 
			"duration":1200, 
			"uploaded_time":"2021-02-20 22:16:00",
			"host":"Aditya Agarwal",
			"participants":["Lucy J", "Andrew G"] 
		}
		#podcast is created , count should increment by 1
		r2 = requests.post("{}/create/podcast".format(endpoint), json=json_data)
		#Getting lastest count
		r3 = requests.get("{}/get/podcast".format(endpoint))
		self.assertEqual(r2.status_code, 200)
		self.assertEqual(len(r3.json()), initial_count+1)

	def test_3_create(self):
		endpoint = 'http://127.0.0.1'
		#trying to create a song with existing id
		r1 = requests.get("{}/get/song".format(endpoint))
		id = r1.json()[0]['id']
		json_data={
			"id":id,
			"name":"Dance on floor",
			"duration":120,
			"uploaded_time":"2021-02-20 22:18:00"
		}
		r2 = requests.post("{}/create/song".format(endpoint), json=json_data)
		#should be getting 400
		self.assertEqual(r2.status_code, 400)

		#sending a create request without json data
		r3 = requests.post("{}/create/song".format(endpoint))
		#should be getting 400
		self.assertEqual(r3.status_code, 400)

	def test_4_create(self):
		endpoint = 'http://127.0.0.1'

		#sending create command with in complete JSON data
		json_data = {
		"id":100,
		"name":"Hello"
		}
		r1 = requests.post("{}/create/song".format(endpoint), json=json_data)
		#should be getting 400
		self.assertEqual(r1.status_code, 400)

		#sending wrong data to API 
		json_data = {
		"id":100,
		"name":"Hello",
		"duration":"Duration is int not string",
		"uploaded_time":"2021-02-20 22:20:00"
		}
		r2 = requests.post("{}/create/song".format(endpoint), json=json_data)
		#shoud be getting 400
		self.assertEqual(r2.status_code, 400)

	def test_5_update(self):
		endpoint = 'http://127.0.0.1'
		
		r1 = requests.get("{}/get/podcast/1".format(endpoint))
		initial_duration = r1.json()[0]['duration']

		#let update this podcast with id = 1
		json_data = {
		"id":1,
		"name":"Happiness in the life",
		"duration":initial_duration + 100,
		"uploaded_time":"2021-02-20 22:20:00",
		"host":"Aditya Agarwal"
		}
		r2 = requests.put("{}/update/podcast/1".format(endpoint), json = json_data)
		#should get 200
		self.assertEqual(r2.status_code, 200)
		r3 = requests.get("{}/get/podcast/1".format(endpoint))
		#duration should not match
		self.assertNotEqual(r3.json()[0]['duration'], initial_duration)

	def test_6_delete(self):
		endpoint = 'http://127.0.0.1'

		r1 = requests.get("{}/get/podcast".format(endpoint))
		initial_count = len(r1.json())
		max_id = max([i['id'] for i in r1.json()])

		#delete
		r2 = requests.delete("{}/delete/podcast/{}".format(endpoint, max_id))
		#should get 200
		self.assertEqual(r2.status_code, 200)
		#getting count
		r3 = requests.get("{}/get/podcast".format(endpoint))
		self.assertEqual(len(r3.json()), initial_count-1)


if __name__ == '__main__':
    unittest.main()