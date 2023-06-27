import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from students.models import Course, Student


@pytest.mark.django_db
def test_get_course(client, course_factory):
    '''
    проверка получения 1 курса
    '''
    # Arrange
    course = course_factory(_quantity=1)
    course_id = course[0].id
    course_name = course[0].name
    url = reverse('courses-list') + f'{course_id}/'

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert course_name == data['name']
    assert course_id == data['id']


@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    '''
    проверка получения списка курсов
    '''
    # Arrange
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    for ind, course in enumerate(data):
        assert course['name'] == courses[ind].name
        assert  course['id'] == courses[ind].id


@pytest.mark.django_db
def test_get_course_filtered_by_id(client, course_factory):
    '''
    проверка получения одного курса по id из списка
    '''
    # Arrange
    courses = course_factory(_quantity=10)
    target_id = courses[3].id
    target_name = courses[3].name
    url = reverse('courses-list')

    # Act
    response = client.get(url, {'id': target_id})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id']  == target_id
    assert data[0]['name'] == target_name


@pytest.mark.django_db
def test_get_course_filtered_by_name(client, course_factory):
    '''
    проверка получения одного курса по названию из списка
    '''
    # Arrange
    courses = course_factory(_quantity=10)
    target_id = courses[3].id
    target_name = courses[3].name
    url = reverse('courses-list')

    # Act
    response = client.get(url, {'name': target_name})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id']  == target_id
    assert data[0]['name'] == target_name


@pytest.mark.django_db
def test_create_course(client):
    '''
    проверка создания курса
    '''
    # Arrange
    course_name = 'Python для чайников'
    course = {'name': course_name}
    url = reverse('courses-list')

    # Act
    response = client.post(url, course)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert course_name == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    '''
    проверка внесения изменений в курс - новое название и новое кол-во студентов
    '''
    # Arrange
    course_name = 'Python для чайников'
    course = course_factory(name=course_name)
    url = reverse('courses-detail', args=(course.id,))
    new_name = 'Python для профессионалов'
    students = student_factory(_quantity=5)
    new_course = {
        'name': new_name,
        'students': [st.id for st in students]
    }

    # Act
    response = client.patch(url, new_course)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert new_name == data['name']
    assert len(data['students']) == 5
    # проверка правильности id студентов курса
    for ind, student_id in enumerate(data['students']):
        assert students[ind].id == student_id


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    '''
    проверка удаления курса
    '''
    # Arrange
    course_name = 'Python для детского сада'
    course = course_factory(name=course_name)
    url = reverse('courses-detail', args=(course.id,))

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 204
    # проверяем список всех курсов в модели Course с фильтром name = 'Python для детского сада'
    courses = Course.objects.filter(name=course_name)
    assert len(courses) == 0

