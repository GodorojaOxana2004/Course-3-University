# Лабораторная работа 2 — Pipelines (Java)

**Автор:** ты

**Краткое описание:**
Реализован универсальный `Pipeline<TContext>` с шагами `IPipelineStep<TContext>` и набором готовых шагов для работы с текстом. В проекте показаны: абстракция, полиморфизм, контекст, паттерны Adapter/Decorator/Strategy/Visitor/Singleton, интроспекция, data-oriented подход, возможность остановки цепочки (Responsibility Chain), а также набор утилит для изменения последовательности шагов и unit-тест.

---

# Структура проекта (важные файлы)

```
├───.idea
├───src
│   ├───main
│   │   └───java
│   │       └───com
│   │           └───example
│   │               └───pipeline
│   │                   ├───context
│   │                   ├───decorators
│   │                   ├───introspect
│   │                   ├───singleton
│   │                   ├───steps
│   │                   └───visitor
│   └───test
│       └───java
│           └───com
│               └───example
│                   └───pipeline
└───target
    ├───classes
    │   └───com
    │       └───example
    │           └───pipeline
    │               ├───context
    │               ├───decorators
    │               ├───introspect
    │               ├───singleton
    │               ├───steps
    │               └───visitor
    ├───generated-sources
    │   └───annotations
    ├───generated-test-sources
    │   └───test-annotations
    └───test-classes
        └───com
            └───example
                └───pipeline
```

---

# Как собрать и запустить (Windows)

1. Открой проект в IntelliJ IDEA (File → Open → укажи корень `lr2-pipelines`). IDEA распознает `pom.xml` как Maven-проект.
2. Или в PowerShell/Command Prompt выполни:
   ```powershell
   cd D:\lr2-pipelines-java\lr2-pipelines-java
   mvn clean package
   java -jar target\pipelines-1.0-SNAPSHOT.jar
   ```

> В `pom.xml` прописан `Main-Class` (при сборке JAR через Maven), поэтому `java -jar` запустит программу.

---

# Что делает программа — пошагово

1. **Создаётся контекст** `TextContext`, содержащий строку и объект `AuditContext` для логирования событий.
2. **Формируется `Pipeline<TextContext>`** и добавляются шаги в нужном порядке: `TrimStep`, `ReplaceStep`, `LowercaseStep`, `ReplaceStep`, `WordCountStep`.
3. **Все шаги оборачиваются `LoggingDecorator`** (с помощью `pipeline.wrapAll(...)`) — это пример паттерна Декоратор: мы добавляем поведение *вокруг* шага без изменения самой реализации шага.
4. **Выполняется `pipeline.execute(context)`** — последовательное выполнение шагов. Каждый шаг может модифицировать `TextContext` и писать событие в `AuditContext`.
5. **Интроспекция**: после выполнения вызывается `pipeline.introspect()`, который собирает описание шагов через `describe()` каждого шага и выводит их.

---

# Соответствие требованиям лабораторной работы

Ниже — пункт за пунктом как реализовано.

### Обязательные пункты
- **Создать свой pipeline** — реализовано в `Pipeline.java`.
- **Сконфигурируйте тестовый pipeline в `Main`** — реализовано (`Main.java`).

### Дополнительные задания (реализованные)
- **Используйте generics чтобы задавать тип контекста** — `Pipeline<TContext>` и `IPipelineStep<TContext>` реализованы (файлы: `Pipeline.java`, `IPipelineStep.java`, `AbstractPipelineStep.java`).
- **Улучшите систему интроспекции** — есть `describe(StringBuilder sb)` у каждого шага и `Introspection.appendHeader(...)` (файл `introspect/Introspection.java`).
- **Вспомогательные функции для изменения массива шагов** — реализованы:
  - `replaceFirstInstance(Class, IPipelineStep)` — `Pipeline.replaceFirstInstance(...)`
  - `replaceAll(Class, IPipelineStep)` — `Pipeline.replaceAll(...)`
  - `wrapAll(Function<IPipelineStep, IPipelineStep>)` — `Pipeline.wrapAll(...)`
  - `moveTo(Class, int)` — `Pipeline.moveTo(...)`
- **Паттерн Декоратор** — `LoggingDecorator` и `TimingDecorator` (папка `decorators/`) — показано, как оборачивать шаги.
- **Singleton для общих шагов** — `singleton/CommonSteps.java` содержит статические экземпляры `TRIM` и `LOWER`.
- **Unit tests** — есть тест `PipelineTest.java` (Junit 5), демонстрирует базовую проверку `TrimStep` + `LowercaseStep`.
- **Responsibility Chain (остановка выполнения)** — `StopOnProfanityStep` помечает контекст `setDone(true)`; `Pipeline.execute(...)` проверяет `ContextUtils.isDone(context)` и прекращает выполнение следующих шагов.
- **Visitor** — интерфейс `visitor/IPipelineVisitor.java` и простой `PrintVisitor` для демонстрации `accept(...)`.

### Частично / не реализовано (честно)
- **Демонстрация работы с 2 разными видами контекста** — в коде есть `TextContext` и `AuditContext` (audit — вспомогательный объект внутри текстового контекста). Но демонстрация двух *отдельных* pipeline`ов с разными TContext (например `TextContext` и `NumericContext`) в `Main` пока не сделана. Это легко добавить: например, создать `NumericContext` и реализовать шаги `MultiplyStep`, `ClampStep` и показать второй pipeline.

---

# Ключевые классы — кратко

- `Pipeline<TContext>` — хранит `List<IPipelineStep<TContext>>`, умеет `add`, `execute`, `introspect`, а также высокоуровневые операции `replaceFirstInstance`, `replaceAll`, `wrapAll`, `moveTo`.
- `IPipelineStep<TContext>` — интерфейс шага: `execute(TContext)`, `describe(StringBuilder)`.
- `AbstractPipelineStep<TContext>` — базовый класс для шагов с полем `name`.
- `ContextUtils` — утилита для проверки `isDone(context)` через reflection (метод `isDone()` или поле `done`).
- `LoggingDecorator<TContext>` / `TimingDecorator<TContext>` — декораторы, добавляют логирование/тайминг вокруг шага.
- `CommonSteps` — singleton-экземпляры общих шагов (Trim, Lowercase).
- `TextContext` / `AuditContext` — контекст обработки текста и журнал аудита.
- `StopOnProfanityStep` — пример шага, который может остановить выполнение всего pipeline, выставив `context.setDone(true)`.

---

# Пример вывода

```
[LOG] Starting step: TrimStep(Trim whitespace)
[LOG] Finished step: TrimStep(Trim whitespace)
[LOG] Starting step: ReplaceStep(Replace 'WORLD' -> 'Java')
[LOG] Finished step: ReplaceStep(Replace 'WORLD' -> 'Java')
[LOG] Starting step: LowercaseStep(To lowercase)
[LOG] Finished step: LowercaseStep(To lowercase)
[LOG] Starting step: ReplaceStep(Replace 'badword' -> '***')
[LOG] Finished step: ReplaceStep(Replace 'badword' -> '***')
[LOG] Starting step: WordCountStep(Word count)
[LOG] Finished step: WordCountStep(Word count)
Final text: 'hello java! ***'
Audit events:
TrimStep: trimmed
ReplaceStep: replaced WORLD
LowercaseStep: lowered
ReplaceStep: replaced badword
WordCountStep: 3
--- Introspection ---
Pipeline introspection for: Pipeline
LoggingDecorator(TrimStep)
TrimStep - Trim whitespace
LoggingDecorator(ReplaceStep)
ReplaceStep - Replace 'WORLD' -> 'Java'
LoggingDecorator(LowercaseStep)
LowercaseStep - To lowercase
LoggingDecorator(ReplaceStep)
ReplaceStep - Replace 'badword' -> '***'
LoggingDecorator(WordCountStep)
WordCountStep - Word count
```

Это демонстрирует: порядок выполнения, что декоратор видим в интроспекции и что аудит логирует события.

---

# Заключение

Проект реализует основные требования ЛР и ряд дополнительных заданий: generics, декораторы, high-level операции над списком шагов, singleton-шаги, visitor-интерфейс, интроспекция и остановка выполнения. Код модульный, легко расширяемый.

