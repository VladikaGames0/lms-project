import requests

BASE_URL = "http://localhost:8000/api"


def test_courses():
    print("\n=== Тестирование курсов ===")

    course_data = {
        "title": "Python для начинающих",
        "description": "Базовый курс по Python"
    }
    response = requests.post(f"{BASE_URL}/courses/", json=course_data)
    print(f"POST /courses/: {response.status_code}")
    print(f"Создан курс: {response.json()}")

    if response.status_code == 201:
        course_id = response.json()['id']

        response = requests.get(f"{BASE_URL}/courses/")
        print(f"\nGET /courses/: {response.status_code}")
        print(f"Список курсов: {response.json()}")

        response = requests.get(f"{BASE_URL}/courses/{course_id}/")
        print(f"\nGET /courses/{course_id}/: {response.status_code}")
        print(f"Курс: {response.json()}")

        update_data = {"title": "Python для продвинутых"}
        response = requests.patch(f"{BASE_URL}/courses/{course_id}/", json=update_data)
        print(f"\nPATCH /courses/{course_id}/: {response.status_code}")
        print(f"Обновленный курс: {response.json()}")

        return course_id
    return None


def test_lessons(course_id):
    print("\n=== Тестирование уроков ===")

    lesson_data = {
        "title": "Введение в Python",
        "description": "Первый урок курса",
        "video_link": "https://www.youtube.com/watch?v=example",
        "course": course_id
    }
    response = requests.post(f"{BASE_URL}/lessons/", json=lesson_data)
    print(f"POST /lessons/: {response.status_code}")
    print(f"Создан урок: {response.json()}")

    if response.status_code == 201:
        lesson_id = response.json()['id']

        response = requests.get(f"{BASE_URL}/lessons/")
        print(f"\nGET /lessons/: {response.status_code}")
        print(f"Список уроков: {response.json()}")

        response = requests.get(f"{BASE_URL}/lessons/{lesson_id}/")
        print(f"\nGET /lessons/{lesson_id}/: {response.status_code}")
        print(f"Урок: {response.json()}")

        update_data = {"title": "Python - введение в программирование"}
        response = requests.patch(f"{BASE_URL}/lessons/{lesson_id}/", json=update_data)
        print(f"\nPATCH /lessons/{lesson_id}/: {response.status_code}")
        print(f"Обновленный урок: {response.json()}")

        response = requests.delete(f"{BASE_URL}/lessons/{lesson_id}/")
        print(f"\nDELETE /lessons/{lesson_id}/: {response.status_code}")


if __name__ == "__main__":
    course_id = test_courses()
    if course_id:
        test_lessons(course_id)
