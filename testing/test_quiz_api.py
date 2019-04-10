from testing.base import Base


class TestQuizApi(Base):
    def test_get(self):
        r = self.client.get('/quiz/', headers=self.headers)
        assert r.status_code == 200
        assert 'count' in r.json

    def test_post(self):
        data = dict(creator_id=1, description='Summary on C', name='Summary',
                    video_url="https://www.youtube.com/embed/2NWeucMKrLI")
        r = self.client.post('/quiz/', headers=self.headers, json=data)
        assert r.status_code == 201
        assert r.json['message'] == 'Successfully created!'

    def test_put(self):
        data = dict(id=1, description='Introduction to C')
        r = self.client.put('/quiz/', headers=self.headers, json=data)
        assert r.status_code == 200
        assert r.json['message'] == 'Successfully updated!'


    def delete(self):
        data = dict(id=1, description='Introduction to C')
        r = self.client.put('/quiz/', headers=self.headers, json=data)
        assert r.status_code == 200
        assert r.json['message'] == 'Successfully deleted!'