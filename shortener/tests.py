import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import URL

@pytest.mark.django_db
def test_signup_flow(client):
    signup_url = reverse('signup')
    response = client.get(signup_url)

    assert response.status_code == 200

    User = get_user_model()
    username = 'testuser123'
    password = 'testpassword123!'

    assert User.objects.filter(username=username).exists() is False

    response = client.post(signup_url, {
        'username': username,
        'password1': password,
        'password2': password,
    })

    assert response.status_code == 302
    assert response.url == reverse('my_urls')

    assert User.objects.filter(username=username).exists() is True


@pytest.mark.django_db
def test_signup_fail_password_mismatch(client):
    signup_url = reverse('signup')
    username = 'testuser2'

    response = client.post(signup_url, {
        'username': username,
        'password1': 'goodpassword123!',
        'password2': 'wrongpassword123!',
    })

    assert response.status_code == 200

    User = get_user_model()
    assert User.objects.filter(username=username).exists() is False


@pytest.mark.django_db
def test_signup_fail_password_too_common(client):
    signup_url = reverse('signup')
    username = 'testuser3'

    common_password = 'password'
    response = client.post(signup_url, {
        'username': username,
        'password1': common_password,
        'password2': common_password,
    })

    assert response.status_code == 200

    assert b'This password is too common.' in response.content

    User = get_user_model()
    assert User.objects.filter(username=username).exists() is False


@pytest.mark.django_db
def test_signup_fail_username_exists(client):
    existing_user = get_user_model().objects.create_user(
        username='existinguser',
        password='testpassword123!',
    )

    signup_url = reverse('signup')

    response = client.post(signup_url, {
        'username': 'existinguser',
        'password1': 'anotherpassword456!',
        'password2': 'anotherpassword456!',
    })

    assert response.status_code == 200

    assert b'A user with that username already exists.' in response.content

    assert get_user_model().objects.count() == 1


@pytest.mark.django_db
def test_my_urls_view_unauthenticated(client):
    my_urls_url = reverse('my_urls')
    response = client.get(my_urls_url)

    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_url_creation_and_list_view(client):
    User = get_user_model()
    user_a = User.objects.create_user(username='user_a', password='password123!')
    user_b = User.objects.create_user(username='user_b', password='password123!')

    URL.objects.create(
        original_url='https://google.com',
        owner=user_a,
    )
    URL.objects.create(
        original_url='https://naver.com',
        owner=user_b,
    )
    client.login(username='user_a', password='password123!')
    my_urls_url = reverse('my_urls')

    response = client.get(my_urls_url)
    assert response.status_code == 200

    assert b'https://google.com' in response.content
    assert b'https://naver.com' not in response.content

    response = client.post(my_urls_url, {'original_url': 'https://youtube.com'})

    assert response.status_code == 302
    assert response.url == my_urls_url

    assert URL.objects.filter(owner=user_a, original_url='https://youtube.com').exists()