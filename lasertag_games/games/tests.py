from django.test import SimpleTestCase


class PagesTest(SimpleTestCase):
    def test_home_shows_count(self):
        r = self.client.get('/')
        self.assertContains(r, 'Всего игр: 8.')

    def test_arenas(self):
        self.assertContains(self.client.get('/arenas/'), 'Фортец')

    def test_filter_differs(self):
        a = self.client.get('/games/?players=1').content.decode()
        b = self.client.get('/games/?players=20').content.decode()
        self.assertGreater(a.count('class="card'), b.count('class="card'))

    def test_filter_empty(self):
        self.assertContains(self.client.get('/games/?players=999'), 'не найдено')

    def test_sql_injection_param_is_safe(self):
        r = self.client.get("/games/?players=1;DROP TABLE games&sort=x;DROP")
        self.assertEqual(r.status_code, 200)

    def test_limit(self):
        r = self.client.get('/games/?limit=3').content.decode()
        self.assertEqual(r.count('class="card'), 3)

    def test_detail_and_404(self):
        self.assertContains(self.client.get('/games/flag-capture/'), 'Фортец')
        self.assertEqual(self.client.get('/games/nope/').status_code, 404)

    def test_statistics_route_before_slug(self):
        r = self.client.get('/games/statistics/')
        self.assertContains(r, 'КОМАНДНЫЙ')

    def test_db_error_no_traceback(self):
        from django.test import override_settings
        with override_settings(GAMES_DB_PATH='/nonexistent/x.db'):
            r = self.client.get('/games/')
        self.assertEqual(r.status_code, 500)
        self.assertNotContains(r, 'Traceback', status_code=500)
