# Лабораторная работа: Возможности представления свойств объекта в системе

## Цель работы

Изучить возможности представления свойств объекта в системе, реализовать механизм динамических свойств для объектов, обеспечивающий типобезопасность и централизованное управление ключами. Демонстрация возможности одного проекта работать с сущностями, определёнными в другом проекте, с использованием динамических свойств.

---

## Концепты и подходы

### 1. Статическая иерархия классов

* Свойства задаются статически через иерархию классов.
* Используются интерфейсы для обхода ограничения на множественное наследование.
* Паттерн traits помогает избежать дублирования хранения свойств.
* **Минусы:** невозможность конфигурировать свойства во время выполнения программы.

### 2. `object[]`

* Примитивный подход: массив свойств `object[]`.
* Можно группировать свойства в компоненты и использовать тег для различения типов.
* **Минусы:** отсутствие типовой безопасности, необходимость ручных проверок.

### 3. Fat Struct

* Простая структура хранения всех свойств в фиксированном объекте.
* **Минусы:** затраты памяти на все свойства, необходимость проверок на наличие значения.
* **Не подходит**, если библиотека не знает заранее, какие свойства будут использовать пользователи.

### 4. Ассоциативный массив (словари)

* Свойства хранятся по строковому ключу.
* Ключи можно типизировать через generic-обёртку.
* Можно использовать integer-ключ и централизованный реестр для согласованности между проектами.
* **Минусы:** память используется на объекты ключей и значения.

### 5. Продвинутый уровень: ECS (Entity Component System)

* Sparse Set (например, EnTT)
* Архетипический ECS (например, Unity DOTS)
* Используется в высокопроизводительных игровых системах.

---

## Задача лабораторной

* Реализовать **динамический контекст**, позволяющий библиотеке не знать заранее, какие данные будут храниться.
* Создать **централизованный реестр ключей** (`KeyRegistry`) для предотвращения конфликтов.
* Использовать **типизированные ключи (`TypedKey<T>`)**, обеспечивающие типовую безопасность.
* Реализовать пример проекта с сущностями (`Book`), расширяемыми через динамические свойства.

---

## Реализация

### Структура проекта

```
com.example.dynamiclib      // библиотека динамических свойств
com.example.dynamiclib.model // модель Book
com.example.bookapp         // приложение-пример
```

---

### DynamicContext.java

```java
package com.example.dynamiclib;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

public final class DynamicContext {
    private final Map<Integer, Object> map = new ConcurrentHashMap<>();

    public <T> void put(TypedKey<T> key, T value) {
        if (value != null && !key.type().isInstance(value)) {
            throw new ClassCastException("Value for key " + key.name() + " is not of type " + key.type());
        }
        map.put(key.id(), value);
    }

    @SuppressWarnings("unchecked")
    public <T> Optional<T> get(TypedKey<T> key) {
        Object v = map.get(key.id());
        if (v == null) return Optional.empty();
        return Optional.of(key.type().cast(v));
    }

    public <T> T getOrDefault(TypedKey<T> key, T defaultValue) {
        return get(key).orElse(defaultValue);
    }

    public boolean contains(TypedKey<?> key) {
        return map.containsKey(key.id());
    }

    public void remove(TypedKey<?> key) {
        map.remove(key.id());
    }
}
```

---

### TypedKey.java

```java
package com.example.dynamiclib;

public final class TypedKey<T> {
    private final int id;
    private final String name;
    private final Class<T> type;

    TypedKey(int id, String name, Class<T> type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }

    public int id() { return id; }
    public String name() { return name; }
    public Class<T> type() { return type; }

    @Override
    public String toString() {
        return "TypedKey{" + name + "#" + id + " -> " + type.getSimpleName() + "}";
    }
}
```

---

### KeyRegistry.java

```java
package com.example.dynamiclib;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public final class KeyRegistry {
    private final AtomicInteger counter = new AtomicInteger(1);
    private final ConcurrentHashMap<String, Integer> nameToId = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<Integer, Class<?>> idToType = new ConcurrentHashMap<>();

    public <T> TypedKey<T> register(String namespacedName, Class<T> type) {
        Integer existing = nameToId.putIfAbsent(namespacedName, -1);
        if (existing != null) {
            Integer id = nameToId.get(namespacedName);
            Class<?> registeredType = idToType.get(id);
            if (!registeredType.equals(type)) {
                throw new KeyAlreadyRegisteredException("Key '" + namespacedName + "' already registered with different type: " + registeredType);
            }
            return new TypedKey<>(id, namespacedName, type);
        }

        int id = counter.getAndIncrement();
        nameToId.put(namespacedName, id);
        idToType.put(id, type);
        return new TypedKey<>(id, namespacedName, type);
    }

    public boolean isRegistered(String namespacedName) {
        return nameToId.containsKey(namespacedName);
    }
}
```

---

### KeyAlreadyRegisteredException.java

```java
package com.example.dynamiclib;

public class KeyAlreadyRegisteredException extends RuntimeException {
    public KeyAlreadyRegisteredException(String msg) { super(msg); }
}
```

---

### Book.java

```java
package com.example.dynamiclib.model;

import com.example.dynamiclib.DynamicContext;

public class Book {
    private final int id;
    private final String title;
    private final String author;
    private final DynamicContext context = new DynamicContext();

    public Book(int id, String title, String author) {
        this.id = id;
        this.title = title;
        this.author = author;
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public DynamicContext getContext() { return context; }

    @Override
    public String toString() {
        return "Book{id=" + id + ", title='" + title + "', author='" + author + "'}";
    }
}
```

---

### BookExtensions.java

```java
package com.example.bookapp;

import com.example.dynamiclib.KeyRegistry;
import com.example.dynamiclib.TypedKey;

import java.util.List;

public class BookExtensions {
    public final TypedKey<Double> RATING;
    public final TypedKey<List> GENRES;
    public final TypedKey<Integer> SALES;

    public BookExtensions(KeyRegistry registry) {
        RATING = registry.register("book.rating", Double.class);
        GENRES = registry.register("book.genres", List.class);
        SALES = registry.register("book.sales", Integer.class);
    }
}
```

---

### BookRepository.java

```java
package com.example.bookapp;

import com.example.dynamiclib.model.Book;
import java.util.ArrayList;
import java.util.List;

public class BookRepository {
    private final List<Book> books = new ArrayList<>();

    public void add(Book book) { books.add(book); }
    public List<Book> findAll() { return books; }
}
```

---

### App.java

```java
package com.example.bookapp;

import com.example.dynamiclib.KeyRegistry;
import com.example.dynamiclib.model.Book;
import java.util.Arrays;

public class App {
    public static void main(String[] args) {
        KeyRegistry registry = new KeyRegistry();
        BookExtensions ext = new BookExtensions(registry);
        BookRepository repo = new BookRepository();

        Book b1 = new Book(1, "1984", "George Orwell");
        Book b2 = new Book(2, "Brave New World", "Aldous Huxley");

        b1.getContext().put(ext.RATING, 9.2);
        b1.getContext().put(ext.GENRES, Arrays.asList("Dystopian", "Political Fiction"));

        b2.getContext().put(ext.RATING, 8.8);
        b2.getContext().put(ext.SALES, 1500000);

        repo.add(b1);
        repo.add(b2);

        for (Book b : repo.findAll()) {
            System.out.println(b);
            System.out.println("  Rating: " + b.getContext().get(ext.RATING).orElse(null));
            System.out.println("  Genres: " + b.getContext().get(ext.GENRES).orElse(null));
            System.out.println("  Sales: " + b.getContext().get(ext.SALES).orElse(null));
        }
    }
}
```

---

## Объяснение выбранного подхода

1. FatStruct не подходит, так как библиотека не знает заранее, какие свойства будут нужны пользователям.
2. Используем DynamicContext + TypedKey + KeyRegistry, что позволяет:

    * добавлять свойства во время выполнения;
    * обеспечивать типовую безопасность;
    * иметь централизованный реестр ключей для нескольких проектов;
    * работать с сущностями, определёнными в других проектах.

## Пример использования

```java
b1.getContext().put(ext.RATING, 9.2);          // Double
b1.getContext().put(ext.GENRES, Arrays.asList("Dystopian", "Political Fiction")); // List<String>
```

* Система проверяет тип значения при записи.
* Попытка записать несовместимый тип вызовет ошибку на этапе выполнения.

## Вывод

* Реализована библиотека для динамических свойств объектов с типовой безопасностью.
* Использован паттерн Registry для централизованного хранения ключей.
* Использован паттерн Type Object для хранения информации о типе.
* Использован паттерн Extension Object, позволяющий расширять объекты без изменения их исходного кода.
* Подход подходит для библиотек, где пользовательские проекты задают свойства и операции на лету.

## Литература и ссылки

* ASP.NET Core AuthenticationProperties.Items
* MVC ActionExecutingContext.ActionParameters
* Middleware HttpContext.Items
* FluentValidation ValidationContext.RootContextData
* ECS: EnTT, Unity DOTS
