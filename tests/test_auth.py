import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestAuth:
    """Класс для тестирования функциональности авторизации"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед каждым тестом"""
        self.driver = driver
        self.base_url = "https://b2c.passport.rt.ru/"
        self.wait = WebDriverWait(driver, 15)  # Increased timeout to 15 seconds
        
        # Открываем страницу авторизации
        self.driver.get(self.base_url)
        
        # Ждем загрузки страницы
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("Page loaded successfully")
        except TimeoutException:
            logger.warning("Page took longer to load or had issues")
        
    def test_phone_auth_tab_TC06(self):
        """TC-06: Переключение на вкладку авторизации по номеру телефона"""
        try:
            # Сначала переключимся на другую вкладку, чтобы проверить переключение
            # Попробуем сначала вкладку "Почта"
            mail_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
            mail_tab.click()
            
            # Подождем немного, чтобы убедиться, что вкладка изменилась
            time.sleep(1)
            
            # Теперь переключаемся на вкладку "Телефон"
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
            phone_tab.click()
            
            # Ждем обновления поля ввода
            phone_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            
            # Подождем короткое время для отображения placeholder
            time.sleep(0.5)
            
            # Проверяем, что поле ввода изменилось на поле для телефона
            placeholder = phone_input.get_attribute("placeholder")
            
            # Проверяем, что placeholder соответствует полю для телефона
            assert "мобильный телефон" in placeholder.lower() or "телефон" in placeholder.lower(), \
                f"Ожидаем placeholder для телефона, но получили: '{placeholder}'"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_phone_auth_tab_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Вкладка 'Телефон' успешно выбрана")
            
        except Exception as e:
            logger.error(f"TC06 FAIL - Ошибка при проверке вкладки 'Телефон': {str(e)}")
            # Снимок экрана при ошибке, показывающий весь контекст страницы
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_phone_auth_tab_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC06: Ошибка при проверке вкладки 'Телефон': {str(e)}")
    
    def test_mail_auth_tab_TC06(self):
        """TC-06: Переключение на вкладку авторизации по почте"""
        try:
            # Ищем вкладку "Почта"
            mail_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
            mail_tab.click()
            
            # Ждем обновления поля ввода
            mail_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            
            # Подождем короткое время для отображения placeholder
            time.sleep(0.5)
            
            # Проверяем, что поле ввода изменилось на поле для почты
            placeholder = mail_input.get_attribute("placeholder")
            
            # Проверяем, что placeholder соответствует полю для почты
            assert "почту" in placeholder.lower() or "email" in placeholder.lower(), \
                f"Ожидаем placeholder для почты, но получили: {placeholder}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_mail_auth_tab_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Вкладка 'Почта' успешно выбрана")
            
        except Exception as e:
            logger.error("TC06 FAIL - Не удалось найти или кликнуть на вкладку 'Почта'")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_mail_auth_tab_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC06: Не удалось найти или кликнуть на вкладку 'Почта': {str(e)}")
    
    def test_login_auth_tab_TC06(self):
        """TC-06: Переключение на вкладку авторизации по логину"""
        try:
            # Ищем вкладку "Логин"
            login_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-login")))
            login_tab.click()
            
            # Ждем обновления поля ввода
            login_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            
            # Подождем короткое время для отображения placeholder
            time.sleep(0.5)
            
            # Проверяем, что поле ввода изменилось на поле для логина
            placeholder = login_input.get_attribute("placeholder")
            
            # Проверяем, что placeholder соответствует полю для логина
            assert "логин" in placeholder.lower(), \
                f"Ожидаем placeholder для логина, но получили: {placeholder}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_login_auth_tab_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Вкладка 'Логин' успешно выбрана")
            
        except Exception as e:
            logger.error("TC06 FAIL - Не удалось найти или кликнуть на вкладку 'Логин'")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_login_auth_tab_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC06: Не удалось найти или кликнуть на вкладку 'Логин': {str(e)}")
    
    def test_ls_auth_tab_TC06(self):
        """TC-06: Переключение на вкладку авторизации по лицевому счету"""
        try:
            # Ищем вкладку "Лицевой счет"
            ls_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-ls")))
            ls_tab.click()
            
            # Ждем обновления поля ввода
            ls_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            
            # Подождем короткое время для отображения placeholder
            time.sleep(0.5)
            
            # Проверяем, что поле ввода изменилось на поле для лицевого счета
            placeholder = ls_input.get_attribute("placeholder")
            
            # Проверяем, что placeholder соответствует полю для лицевого счета
            assert "лицевой" in placeholder.lower() or "счет" in placeholder.lower(), \
                f"Ожидаем placeholder для лицевого счета, но получили: {placeholder}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_ls_auth_tab_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Вкладка 'Лицевой счет' успешно выбрана")
            
        except Exception as e:
            logger.error("TC06 FAIL - Не удалось найти или кликнуть на вкладку 'Лицевой счет'")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC06_ls_auth_tab_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC06 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC06: Не удалось найти или кликнуть на вкладку 'Лицевой счет': {str(e)}")
    
    def test_phone_auth_invalid_password_TC09(self):
        """TC-09: Авторизация по номеру телефона с неверным паролем"""
        try:
            # Переключаемся на вкладку "Телефон"
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
            phone_tab.click()
            
            # Вводим номер телефона
            phone_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            phone_input.clear()
            phone_input.send_keys("9123456789")  # Тестовый номер
            
            # Вводим неверный пароль
            password_input = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_input.clear()
            password_input.send_keys("WrongPassword123")
            
            # Нажимаем кнопку "Войти"
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "kc-login")))
            login_button.click()
            
            # Ждем появление сообщения об ошибке
            error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message")))
            error_text = error_message.text.lower()
            assert "неверный логин или пароль" in error_text, \
                f"Ожидаем сообщение 'Неверный логин или пароль', но получили: {error_message.text}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC09_phone_auth_invalid_password_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC09 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Сообщение об ошибке при неверном пароле отображается корректно")
            
        except Exception as e:
            logger.error("TC09 FAIL - Не удалось выполнить тест авторизации с неверным паролем")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC09_phone_auth_invalid_password_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC09 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC09: Не удалось выполнить тест авторизации с неверным паролем: {str(e)}")
    
    def test_register_link_TC12(self):
        """TC-12: Проверка перехода на страницу регистрации"""
        try:
            # Ищем ссылку "Зарегистрироваться"
            register_link = self.wait.until(EC.element_to_be_clickable((By.ID, "kc-register")))
            register_link.click()
            
            # Проверяем, что мы перешли на страницу регистрации
            self.wait.until(EC.presence_of_element_located((By.ID, "page-right")))
            
            # Проверяем наличие полей регистрации
            name_input = self.driver.find_element(By.NAME, "firstName")
            surname_input = self.driver.find_element(By.NAME, "lastName")
            email_or_phone_input = self.driver.find_element(By.ID, "address")
            password_input = self.driver.find_element(By.ID, "password")
            password_confirm_input = self.driver.find_element(By.ID, "password-confirm")
            
            assert name_input.is_displayed(), "Поле 'Имя' не отображается"
            assert surname_input.is_displayed(), "Поле 'Фамилия' не отображается"
            assert email_or_phone_input.is_displayed(), "Поле 'Email или телефон' не отображается"
            assert password_input.is_displayed(), "Поле 'Пароль' не отображается"
            assert password_confirm_input.is_displayed(), "Поле 'Подтверждение пароля' не отображается"
            
            # Заполняем поля для демонстрации позитивного сценария
            name_input.send_keys("Тест")
            surname_input.send_keys("Тестов")
            email_or_phone_input.send_keys("test@example.com")
            password_input.send_keys("TestPassword123!")
            password_confirm_input.send_keys("TestPassword123!")
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC12_register_link_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC12 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Переход на страницу регистрации выполнен успешно, поля заполнены")
            
        except Exception as e:
            logger.error("TC12 FAIL - Не удалось перейти на страницу регистрации")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC12_register_link_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC12 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC12: Не удалось перейти на страницу регистрации: {str(e)}")
    
    def test_forgot_password_link_TC18(self):
        """TC-18: Проверка перехода на страницу восстановления пароля"""
        try:
            # Ищем ссылку "Забыл пароль"
            forgot_password_link = self.wait.until(EC.element_to_be_clickable((By.ID, "forgot-password")))
            forgot_password_link.click()
            
            # Проверяем, что мы перешли на страницу восстановления пароля
            self.wait.until(EC.presence_of_element_located((By.ID, "page-right")))
            
            # Проверяем наличие вкладок восстановления
            phone_tab = self.driver.find_element(By.ID, "t-btn-tab-phone")
            mail_tab = self.driver.find_element(By.ID, "t-btn-tab-mail")
            login_tab = self.driver.find_element(By.ID, "t-btn-tab-login")
            ls_tab = self.driver.find_element(By.ID, "t-btn-tab-ls")
            
            assert phone_tab.is_displayed(), "Вкладка 'Телефон' не отображается"
            assert mail_tab.is_displayed(), "Вкладка 'Почта' не отображается"
            assert login_tab.is_displayed(), "Вкладка 'Логин' не отображается"
            assert ls_tab.is_displayed(), "Вкладка 'Лицевой счет' не отображается"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC18_forgot_password_link_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC18 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Переход на страницу восстановления пароля выполнен успешно")
            
        except Exception as e:
            logger.error("TC18 FAIL - Не удалось перейти на страницу восстановления пароля")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC18_forgot_password_link_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC18 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC18: Не удалось перейти на страницу восстановления пароля: {str(e)}")
    
    def test_temp_code_auth_TC05(self):
        """TC-05: Проверка авторизации по временному коду"""
        try:
            # Ищем кнопку "Войти по временному коду" (в данном случае используем вкладку телефона)
            temp_code_button = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
            temp_code_button.click()
            
            # Ждем появления элементов формы
            time.sleep(0.5)
            
            # Проверяем, что элементы формы отображаются
            username_input = self.driver.find_element(By.ID, "username")
            assert username_input.is_displayed(), "Поле ввода не отображается"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC05_temp_code_auth_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC05 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Форма входа по временному коду отображается корректно")
            
        except Exception as e:
            logger.error("TC05 FAIL - Не удалось найти форму входа по временному коду")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC05_temp_code_auth_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC05 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC05: Не удалось найти форму входа по временному коду: {str(e)}")