# Лабораторная работа №1 — Field Mask

**Тема:** Field Mask

**Коротко:** реализована доменная модель (`Person`), абстракция репозитория (`PersonRepository`), маска полей (`FieldMask`), утилиты для работы с маской (`MaskUtils`), а также печать по маске (`MaskPrinter`). В проект включён контроллер (`PersonController`) и DTO для REST-возврата. Есть unit-тесты (`MaskUtilsTest`, `PersonRepositoryTest`). Ниже — отчёт, архитектура проекта, описание реализации и инструкции по запуску.

---

## 1. Что было реализовано (обязательная часть)

1. Доменная модель: `Person` с полями `id (int)`, `name (String)`, `salary (float)`, `role (enum Role)`, `rating (float)`.
2. Абстракция репозитория: `PersonRepository`, хранящий объекты `Person` (in-memory, под капотом коллекция).
3. Маска полей: `FieldMask` (enum с флагами, реализовано как битовая маска).
4. Метод поиска: `PersonRepository.findByName(String)`.
5. Класс `MaskPrinter` — печать объекта `Person` в консоль по маске.
6. Unit-тесты: проверяют корректность работы `MaskUtils` и `PersonRepository`.

---

## 2. Дополнительные задания (выполненные)

1. **Переделана маска на основе битов** — `FieldMask` реализован как enum с `@Flags`‑подобным подходом, поддерживает побитовые операции.
2. **Unit-тесты** — реализованы через JUnit (классы `MaskUtilsTest` и `PersonRepositoryTest`).
3. **REST API** — реализован через Spring Boot контроллер `PersonController`, который позволяет получать DTO с выборочными полями (по маске).

---

## 3. Архитектура проекта

```
1-lab/
├─ pom.xml                     # Maven конфигурация
├─ src/
│  ├─ main/java/com/example/_1_lab/
│  │  ├─ Application.java       # Точка входа (Spring Boot)
│  │  ├─ controller/
│  │  │  ├─ PersonController.java # REST контроллер
│  │  │  └─ PersonDTO.java        # DTO для API
│  │  ├─ mask/
│  │  │  ├─ FieldMask.java       # битовая маска полей
│  │  │  ├─ MaskPrinter.java     # печать по маске
│  │  │  └─ MaskUtils.java       # вспомогательные методы
│  │  ├─ model/
│  │  │  ├─ Person.java          # доменная модель
│  │  │  └─ Role.java            # enum Role
│  │  └─ repository/
│  │     └─ PersonRepository.java # in-memory база
│  └─ main/resources/
│     └─ application.properties
└─ src/test/java/com/example/_1_lab/
   ├─ MaskUtilsTest.java
   └─ PersonRepositoryTest.java
```

### Краткое описание компонентов

- **`Person`** — доменная модель.
- **`Role`** — перечисление ролей.
- **`FieldMask`** — enum для маскирования полей.
- **`MaskUtils`** — утилиты для работы с масками.
- **`MaskPrinter`** — печать объекта по маске.
- **`PersonRepository`** — in-memory репозиторий, реализует `findByName`.
- **`PersonController`** — REST API, возвращает DTO с учётом маски.
- **Тесты** — проверяют корректность утилит и репозитория.

---

## 4. Важные решения и примеры кода

### Person.java
```java
public class Person {
    private int id;
    private String name;
    private float salary;
    private Role role;
    private float rating;
    // геттеры/сеттеры
}
```

### Role.java
```java
public enum Role {
    JUNIOR, MID, SENIOR, LEAD
}
```

### FieldMask.java
```java
public enum FieldMask {
    ID(1 << 0),
    NAME(1 << 1),
    SALARY(1 << 2),
    ROLE(1 << 3),
    RATING(1 << 4);

    private final int bit;
    FieldMask(int bit) { this.bit = bit; }
    public int getBit() { return bit; }
}
```

### PersonRepository.java
```java
@Repository
public class PersonRepository {
    private final List<Person> persons = new ArrayList<>();

    public void add(Person p) { persons.add(p); }

    public List<Person> getAll() { return persons; }

    public List<Person> findByName(String name) {
        return persons.stream()
                .filter(p -> p.getName().equalsIgnoreCase(name))
                .collect(Collectors.toList());
    }
}
```

### MaskPrinter.java
```java
public class MaskPrinter {
    public static void print(Person p, int mask) {
        if((mask & FieldMask.ID.getBit()) != 0) System.out.print("id=" + p.getId() + " ");
        if((mask & FieldMask.NAME.getBit()) != 0) System.out.print("name=" + p.getName() + " ");
        if((mask & FieldMask.SALARY.getBit()) != 0) System.out.print("salary=" + p.getSalary() + " ");
        if((mask & FieldMask.ROLE.getBit()) != 0) System.out.print("role=" + p.getRole() + " ");
        if((mask & FieldMask.RATING.getBit()) != 0) System.out.print("rating=" + p.getRating() + " ");
        System.out.println();
    }
}
```

---

## 5. Unit tests

Примеры из `MaskUtilsTest` и `PersonRepositoryTest`:
- Проверка правильности комбинации масок.
- Проверка фильтрации объектов по имени.
- Проверка печати по маске.

Запуск: `mvn test`.

---

## 6. Инструкция по запуску

1. Установите JDK 17+ и Maven.
2. В корне (`1-lab/`) выполните:
   ```bash
   mvn spring-boot:run
   ```
3. Приложение поднимется на `http://localhost:8080`.
4. Тесты запустить:
   ```bash
   mvn test
   ```

