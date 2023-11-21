# Таблица сценариев

| Описание сценария                                    | Шаги                                                                                                      | Ожидаемый результат                                                                                       | Выполнено/Ошибка |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|------------------|
| 1. Аутентификация                                    | 1. В появившемся диалоговом окне ввести корректный логин.<br>2. Ввести корректный пароль.<br>3. Нажать "ОК" или подтвердить ввод.                                   | Появление основного окна приложения.                                                                    | Выполнено        |
| 2. Ввод корректных данных о вкладе                   | 1. Ввести корректные данные о сумме вклада, процентной ставке и сроке вклада.<br>2. Нажать кнопку "Сохранить вклад".                                                   | Данные успешно сохранены в базе данных, и общая сумма вложенных денег обновлена.                         | Выполнено        |
| 3. Попытка сохранения вклада некорректными данными   | 1. Ввести некорректные данные о сумме вклада, процентной ставке или сроке вклада.<br>2. Нажать кнопку "Сохранить вклад".                                                | Появление сообщения об ошибке и предотвращение сохранения некорректных данных в базе.                   | Выполнено        |
| 4. Сброс таблицы                                      | 1. Нажать кнопку "Сбросить таблицу".                                                                     | Все данные о вкладах удалены из базы данных, и общая сумма вложенных денег сброшена.                   | Выполнено        |
| 5. Обновление общей суммы вложенных денег            | 1. Ввести корректные данные о вкладе и сохранить.                                                        | Общая сумма вложенных денег в интерфейсе обновлена после добавления нового вклада.                     | Выполнено        |