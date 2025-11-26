from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo

class TodoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo", description="Test Description")

    def test_todo_list(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_todo_create(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)
        new_todo = Todo.objects.last()
        self.assertEqual(new_todo.title, 'New Todo')

    def test_todo_create_with_date(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'Dated Todo',
            'description': 'Description',
            'due_date': '2023-12-31'
        })
        self.assertEqual(response.status_code, 302)
        todo = Todo.objects.get(title='Dated Todo')
        self.assertEqual(str(todo.due_date), '2023-12-31')

    def test_todo_update(self):
        response = self.client.post(reverse('todo_update', args=[self.todo.pk]), {
            'title': 'Updated Todo',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_todo_delete(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_resolve(self):
        response = self.client.post(reverse('todo_resolve', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
