import unittest
from app import create_app
from extensions import db
from models.groups import Groups

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client(self)
        group = Groups.query.filter_by(group_name = 'test').first()
        if not group:
            group = Groups(group_name='test')
            group.save()
        
    
    def test_signup(self):
        """REGISTERING USER TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        status_code=signip_response.status_code
        self.assertEqual(status_code,201)
    
        
    def test_login(self):
        """"LOGIN USER TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        
        status_code=login_response.status_code
        self.assertEqual(status_code,200)
        
        
        
    def test_create_post(self):
        """CREATING POST TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_post_response=self.client.post(
            '/posts',
            json={
                "title":"test post",
                "body":"test post description"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        status_code = create_post_response.status_code
        
        self.assertEqual(status_code, 201)
        
    def test_update_post(self):
        """UPDATING POST TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_post_response=self.client.post(
            '/posts',
            json={
                "title":"test post",
                "body":"test post description"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        
        id = create_post_response.json['id']
    
        update_response=self.client.put(
            f'posts/{id}',
            json={
                'title':'Renamed',
                'body':'Updated description'},
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        status_code = update_response.status_code
        self.assertEqual(status_code,200)
        
        
    def test_get_all_posts(self):
        """GETTING POSTS TEST"""
        """TEST GETTING ALL POSTS"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_post_response=self.client.post(
            '/posts',
            json={
                "title":"test post",
                "body":"test post description"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        response=self.client.get(
            '/posts',
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        status_code=response.status_code
        self.assertEqual(status_code, 200)
        
        
    def test_get_one_post(self):
        """GETTING POST BY ID TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_post_response=self.client.post(
            '/posts',
            json={
                "title":"test post",
                "body":"test post description"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        id = create_post_response.json['id']
        
        response=self.client.get(
            f'posts/{id}',
            headers={
                "Authorization":f'Bearer {access_token}'
            })
    
        status_code=response.status_code
        
        self.assertEqual(status_code,200)
    
        
    def test_delete_post(self):
        """DELETING POST TEST"""
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                  "email":"test_user@gmail.com", 
                  "password":"test_user", 
                  "group":["test"]}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_post_response=self.client.post(
            '/posts',
            json={
                "title":"test post",
                "body":"test post description"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        
        id = create_post_response.json['id']
        
        delete_response = self.client.delete(
            f'posts/{id}',
            headers={
                "Authorization":f'Bearer {access_token}'
            }
            ) 
        status_code = delete_response.status_code
        self.assertEqual(status_code, 204)
    
    
    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        
if __name__=='__main__':
    unittest.main()