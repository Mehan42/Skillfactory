import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def test_automatic_tab_switching_by_input(driver):
    """Тест автоматического переключения табов при вводе данных"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Ждем загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Очищаем поле ввода и вводим email
    username_field = driver.find_element(By.NAME, "username")
    username_field.clear()
    username_field.send_keys("test@example.com")
    
    # Ожидаем автоматического переключения на таб "Почта"
    time.sleep(2)  # Небольшая задержка для обработки ввода
    
    # Проверяем, что текущий таб соответствует введенному формату данных
    current_placeholder = username_field.get_attribute("placeholder")
    assert "почта" in current_placeholder.lower() or "email" in current_placeholder.lower(), \
        f"Таб не переключился автоматически: {current_placeholder}"


def test_login_with_temporary_code_page_elements(driver):
    """Тест элементов страницы авторизации по временному коду"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Ждем загрузки страницы и находим ссылку "Войти по временному коду"
    try:
        temp_code_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "totp"))
        )
        temp_code_link.click()
        
        # Проверяем наличие элементов на странице ввода кода
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Проверяем наличие поля ввода номера телефона или почты
        assert driver.find_element(By.NAME, "username").is_displayed()
        
        # Проверяем наличие кнопки "Получить код"
        get_code_button = driver.find_element(By.ID, "otp_get_code")
        assert get_code_button.is_displayed()
        
    except TimeoutException:
        # На некоторых продуктах ссылка "Войти по временному коду" может быть недоступна
        pytest.skip("Страница авторизации по временному коду недоступна")


def test_password_recovery_by_sms(driver):
    """Тест восстановления пароля через SMS"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Переходим на страницу восстановления пароля
    forgot_password_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "forgot_password"))
    )
    forgot_password_link.click()
    
    # Ждем загрузки формы восстановления
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Вводим номер телефона (тестовый номер)
    username_field = driver.find_element(By.NAME, "username")
    username_field.clear()
    username_field.send_keys("+79991234567")
    
    # Нажимаем кнопку "Продолжить"
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "reset"))
    )
    continue_button.click()

    # Проверяем переход на страницу ввода кода
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='otp-field']"))
        )
        assert True
    except TimeoutException:
        # Проверяем наличие ошибки, если номер не зарегистрирован
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error, .alert, .notification"))
            )
            assert error_message.is_displayed()
        except TimeoutException:
            assert False, "Не удалось определить результат восстановления пароля"


def test_password_recovery_by_email(driver):
    """Тест восстановления пароля через email"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Переходим на страницу восстановления пароля
    forgot_password_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "forgot_password"))
    )
    forgot_password_link.click()
    
    # Ждем загрузки формы восстановления
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Переключаемся на таб "Почта", если он доступен
    try:
        mail_tab = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "t-btn-tab-mail"))
        )
        mail_tab.click()
    except TimeoutException:
        # Если таб "Почта" недоступен, продолжаем с текущего таба
        pass
    
    # Вводим email (тестовый email)
    username_field = driver.find_element(By.NAME, "username")
    username_field.clear()
    username_field.send_keys("test@example.com")
    
    # Нажимаем кнопку "Продолжить"
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "reset"))
    )
    continue_button.click()
    
    # Проверяем переход на страницу ввода кода
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='otp-field']"))
        )
        assert True
    except TimeoutException:
        # Проверяем наличие ошибки, если email не зарегистрирован
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error, .alert, .notification"))
            )
            assert error_message.is_displayed()
        except TimeoutException:
            assert False, "Не удалось определить результат восстановления пароля"


def test_region_selection_in_registration(driver):
    """Тест выбора региона при регистрации"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Переходим на страницу регистрации
    register_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "kc-register"))
    )
    register_link.click()
    
    # Ждем загрузки элементов регистрации
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "firstName"))
    )
    
    # Проверяем наличие выпадающего списка выбора региона
    region_dropdown = driver.find_element(By.XPATH, "//span[@class='rt-select__input']")
    assert region_dropdown.is_displayed()
    
    # Проверяем, что по умолчанию выбран регион Москва
    selected_region = region_dropdown.text
    assert "москва" in selected_region.lower(), f"По умолчанию выбран не регион Москва: {selected_region}"


@pytest.fixture
def driver():
    """Фикстура для инициализации веб-драйвера"""
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()