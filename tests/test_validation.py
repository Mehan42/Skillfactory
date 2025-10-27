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

class TestValidation:
    """Класс для тестирования валидации данных"""
    
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
        
    def test_phone_validation_TC07(self):
        """TC-07: Валидация номера телефона"""
        try:
            # Переключаемся на вкладку "Телефон"
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
            phone_tab.click()
            
            # Вводим некорректный номер телефона
            phone_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            phone_input.clear()
            phone_input.send_keys("123")  # Слишком короткий номер
            
            # Пытаемся нажать кнопку "Войти"
            login_button = self.driver.find_element(By.ID, "kc-login")
            login_button.click()
            
            # Ждем появление сообщения об ошибке (ожидаем что-то связанное с номером)
            error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message, .rt-input-container__meta--error")))
            error_text = error_message.text.lower()
            
            # Проверяем, что есть сообщение об ошибке, связанное с номером телефона
            has_error = any(keyword in error_text for keyword in ["номер", "телефон", "format", "ошибк"])
            assert has_error, f"Ожидаем сообщение об ошибке номера телефона, но получили: {error_message.text}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC07_phone_validation_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC07 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Валидация номера телефона работает корректно")
            
        except Exception as e:
            logger.error("TC07 FAIL - Не удалось проверить валидацию номера телефона")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC07_phone_validation_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC07 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC07: Не удалось проверить валидацию номера телефона: {str(e)}")
    
    def test_email_validation_TC08(self):
        """TC-08: Валидация email"""
        try:
            # Переключаемся на вкладку "Почта"
            mail_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
            mail_tab.click()
            
            # Вводим некорректный email
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_input.clear()
            email_input.send_keys("invalid-email")  # Некорректный email
            
            # Пытаемся нажать кнопку "Войти"
            login_button = self.driver.find_element(By.ID, "kc-login")
            login_button.click()
            
            # Ждем появление сообщения об ошибке
            error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message, .rt-input-container__meta--error")))
            error_text = error_message.text.lower()
            
            # Проверяем, что есть сообщение об ошибке, связанное с email
            has_error = any(keyword in error_text for keyword in ["почту", "email", "ошибк", "формат"])
            assert has_error, f"Ожидаем сообщение об ошибке email, но получили: {error_message.text}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC08_email_validation_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC08 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Валидация email работает корректно")
            
        except Exception as e:
            logger.error("TC08 FAIL - Не удалось проверить валидацию email")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC08_email_validation_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC08 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC08: Не удалось проверить валидацию email: {str(e)}")
    
    def test_password_validation_registration_TC13(self):
        """TC-13: Валидация пароля при регистрации"""
        try:
            # Переходим на страницу регистрации
            register_link = self.wait.until(EC.element_to_be_clickable((By.ID, "kc-register")))
            register_link.click()
            
            # Ждем загрузки страницы регистрации
            self.wait.until(EC.presence_of_element_located((By.ID, "page-right")))
            
            # Заполняем поля
            name_input = self.driver.find_element(By.NAME, "firstName")
            name_input.clear()
            name_input.send_keys("Тест")
            
            surname_input = self.driver.find_element(By.NAME, "lastName")
            surname_input.clear()
            surname_input.send_keys("Тестов")
            
            email_or_phone_input = self.driver.find_element(By.ID, "address")
            email_or_phone_input.clear()
            email_or_phone_input.send_keys("test@example.com")
            
            # Вводим некорректный пароль (менее 8 символов)
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys("123")  # Слишком короткий пароль
            
            password_confirm_input = self.driver.find_element(By.ID, "password-confirm")
            password_confirm_input.clear()
            password_confirm_input.send_keys("123")
            
            # Нажимаем кнопку "Зарегистрироваться"
            register_button = self.driver.find_element(By.NAME, "register")
            register_button.click()
            
            # Ждем появление сообщения об ошибке
            error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message, .rt-input-container__meta--error")))
            error_text = error_message.text.lower()
            
            # Проверяем, что есть сообщение об ошибке, связанное с длиной пароля
            has_error = any(keyword in error_text for keyword in ["8", "символ", "длин", "password"])
            assert has_error, f"Ожидаем сообщение о длине пароля, но получили: {error_message.text}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC13_password_validation_registration_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC13 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Валидация пароля при регистрации работает корректно")
            
        except Exception as e:
            logger.error("TC13 FAIL - Не удалось проверить валидацию пароля при регистрации")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC13_password_validation_registration_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC13 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC13: Не удалось проверить валидацию пароля при регистрации: {str(e)}")
    
    def test_responsive_design_TC15(self):
        """TC-15: Проверка адаптивности интерфейса"""
        try:
            # Проверяем на мобильном разрешении
            self.driver.set_window_size(375, 667)  # iPhone 6/7/8
            
            # Ждем стабилизации интерфейса
            time.sleep(2)
            
            # Проверяем, что основные элементы адаптировались
            auth_container = self.wait.until(EC.presence_of_element_located((By.ID, "page-left")))
            
            # Проверяем наличие вкладок авторизации (проверяем видимость)
            phone_tab = self.driver.find_element(By.ID, "t-btn-tab-phone")
            mail_tab = self.driver.find_element(By.ID, "t-btn-tab-mail")
            login_tab = self.driver.find_element(By.ID, "t-btn-tab-login")
            ls_tab = self.driver.find_element(By.ID, "t-btn-tab-ls")
            
            assert phone_tab.is_displayed(), "Вкладка 'Телефон' не отображается на мобильном разрешении"
            assert mail_tab.is_displayed(), "Вкладка 'Почта' не отображается на мобильном разрешении"
            assert login_tab.is_displayed(), "Вкладка 'Логин' не отображается на мобильном разрешении"
            assert ls_tab.is_displayed(), "Вкладка 'Лицевой счет' не отображается на мобильном разрешении"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC15_responsive_design_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC15 SUCCESS - Screenshot saved: {screenshot_path}")
            
            # Возвращаем к десктопному разрешению
            self.driver.maximize_window()
            
            logger.info("✅ Адаптивность интерфейса работает корректно")
            
        except Exception as e:
            logger.error("TC15 FAIL - Не удалось проверить адаптивность интерфейса")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC15_responsive_design_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC15 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC15: Не удалось проверить адаптивность интерфейса: {str(e)}")
    
    def test_invalid_email_registration_TC16(self):
        """TC-16: Невалидный email при регистрации"""
        try:
            # Переходим на страницу регистрации
            register_link = self.wait.until(EC.element_to_be_clickable((By.ID, "kc-register")))
            register_link.click()
            
            # Ждем загрузки страницы регистрации
            self.wait.until(EC.presence_of_element_located((By.ID, "page-right")))
            
            # Заполняем поля с некорректным email
            name_input = self.driver.find_element(By.NAME, "firstName")
            name_input.clear()
            name_input.send_keys("Тест")
            
            surname_input = self.driver.find_element(By.NAME, "lastName")
            surname_input.clear()
            surname_input.send_keys("Тестов")
            
            email_or_phone_input = self.driver.find_element(By.ID, "address")
            email_or_phone_input.clear()
            email_or_phone_input.send_keys("invalid_email")  # Некорректный email
            
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys("TestPassword123!")
            
            password_confirm_input = self.driver.find_element(By.ID, "password-confirm")
            password_confirm_input.clear()
            password_confirm_input.send_keys("TestPassword123!")
            
            # Нажимаем кнопку "Зарегистрироваться"
            register_button = self.driver.find_element(By.NAME, "register")
            register_button.click()
            
            # Ждем появление сообщения об ошибке
            error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message, .rt-input-container__meta--error")))
            error_text = error_message.text.lower()
            
            # Проверяем, что есть сообщение об ошибке, связанное с email
            has_error = any(keyword in error_text for keyword in ["email", "адрес", "ошибк", "формат"])
            assert has_error, f"Ожидаем сообщение об ошибке email, но получили: {error_message.text}"
            
            # Делаем информативный скриншот после выполнения операции
            time.sleep(5)  # Ждем 5 секунд для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC16_invalid_email_registration_success.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC16 SUCCESS - Screenshot saved: {screenshot_path}")
            logger.info("✅ Проверка валидации некорректного email при регистрации выполнена")
            
        except Exception as e:
            logger.error("TC16 FAIL - Не удалось проверить валидацию некорректного email при регистрации")
            # Снимок экрана при ошибке
            time.sleep(5)  # Ждем 5 секунд перед снимком для отображения результата
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC16_invalid_email_registration_error.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"TC16 ERROR - Screenshot saved: {screenshot_path}")
            pytest.fail(f"TC16: Не удалось проверить валидацию некорректного email при регистрации: {str(e)}")