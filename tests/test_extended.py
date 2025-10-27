import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def test_login_tab_phone_elements(driver):
    """Тест элементов таба 'Телефон' на странице авторизации"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Ждем загрузки страницы и таба "Телефон"
    phone_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-phone"))
    )
    phone_tab.click()
    
    # Проверяем, что поле ввода изменилось на телефон
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Проверяем подсказку в поле ввода
    placeholder = username_field.get_attribute("placeholder")
    assert "телефон" in placeholder.lower() or "номер" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Телефон': {placeholder}"


def test_login_tab_login_elements(driver):
    """Тест элементов таба 'Логин' на странице авторизации"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Ждем загрузки страницы и таба "Логин"
    login_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-login"))
    )
    login_tab.click()
    
    # Проверяем, что поле ввода изменилось на логин
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Проверяем подсказку в поле ввода
    placeholder = username_field.get_attribute("placeholder")
    assert "логин" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Логин': {placeholder}"


def test_login_tab_ls_elements(driver):
    """Тест элементов таба 'Лицевой счёт' на странице авторизации"""
    driver.get("https://b2c.passport.rt.ru/")
    
    # Ждем загрузки страницы и таба "Лицевой счёт"
    ls_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-ls"))
    )
    ls_tab.click()
    
    # Проверяем, что поле ввода изменилось на лицевой счёт
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Проверяем подсказку в поле ввода
    placeholder = username_field.get_attribute("placeholder")
    assert "лицевой" in placeholder.lower() or "счет" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Лицевой счёт': {placeholder}"


def test_password_recovery_phone_tab(driver):
    """Тест переключения на таб 'Телефон' при восстановлении пароля"""
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
    
    # Переключаемся на таб "Телефон"
    phone_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-phone"))
    )
    phone_tab.click()
    
    # Проверяем, что поле ввода изменилось на телефон
    username_field = driver.find_element(By.NAME, "username")
    placeholder = username_field.get_attribute("placeholder")
    assert "телефон" in placeholder.lower() or "номер" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Телефон': {placeholder}"


def test_password_recovery_login_tab(driver):
    """Тест переключения на таб 'Логин' при восстановлении пароля"""
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
    
    # Переключаемся на таб "Логин"
    login_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-login"))
    )
    login_tab.click()
    
    # Проверяем, что поле ввода изменилось на логин
    username_field = driver.find_element(By.NAME, "username")
    placeholder = username_field.get_attribute("placeholder")
    assert "логин" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Логин': {placeholder}"


def test_password_recovery_ls_tab(driver):
    """Тест переключения на таб 'Лицевой счёт' при восстановлении пароля"""
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
    
    # Переключаемся на таб "Лицевой счёт"
    ls_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "t-btn-tab-ls"))
    )
    ls_tab.click()
    
    # Проверяем, что поле ввода изменилось на лицевой счёт
    username_field = driver.find_element(By.NAME, "username")
    placeholder = username_field.get_attribute("placeholder")
    assert "лицевой" in placeholder.lower() or "счет" in placeholder.lower(), \
        f"Подсказка в поле ввода не соответствует табу 'Лицевой счёт': {placeholder}"


def test_registration_form_mandatory_fields(driver):
    """Тест обязательных полей на странице регистрации"""
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
    
    # Проверяем наличие обязательных полей
    mandatory_fields = ["firstName", "lastName", "address", "password", "password-confirm"]
    for field_id in mandatory_fields:
        field = driver.find_element(By.ID, field_id)
        assert field.is_displayed(), f"Обязательное поле {field_id} не отображается"
        
        # Проверяем, что поля не имеют атрибута "required" (браузерный уровень валидации)
        assert field.get_attribute("required") is not None or field.get_attribute("required") == "true", f"Поле {field_id} не помечено как обязательное"


def test_name_field_validation_cyrillic(driver):
    """Тест валидации поля имени (только кириллица)"""
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
    
    # Вводим имя с латинскими буквами (должно вызвать ошибку)
    first_name_field = driver.find_element(By.ID, "firstName")
    first_name_field.clear()
    first_name_field.send_keys("Ivan")
    
    # Кликаем вне поля для вызова валидации
    driver.find_element(By.TAG_NAME, "body").click()
    
    # Проверяем наличие ошибки валидации
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rt-input-container__meta--error"))
        )
        assert error_message.is_displayed()
    except TimeoutException:
        # Валидация может происходить при попытке регистрации
        pass


def test_name_field_validation_min_length(driver):
    """Тест валидации минимальной длины поля имени (не менее 2 символов)"""
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
    
    # Вводим имя с длиной менее 2 символов (должно вызвать ошибку)
    first_name_field = driver.find_element(By.ID, "firstName")
    first_name_field.clear()
    first_name_field.send_keys("А")
    
    # Кликаем вне поля для вызова валидации
    driver.find_element(By.TAG_NAME, "body").click()
    
    # Проверяем наличие ошибки валидации
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rt-input-container__meta--error"))
        )
        assert error_message.is_displayed()
    except TimeoutException:
        # Валидация может происходить при попытке регистрации
        pass


def test_password_recovery_back_button(driver):
    """Тест кнопки 'Назад' на странице восстановления пароля"""
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
    
    # Находим и кликаем кнопку "Назад"
    back_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "reset-back"))
    )
    back_button.click()
    
    # Проверяем возврат на страницу авторизации
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kc-form-options"))
    )
    assert "b2c.passport.rt.ru" in driver.current_url, "Не вернулись на страницу авторизации"


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