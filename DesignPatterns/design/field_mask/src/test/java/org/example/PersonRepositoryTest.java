package org.example;

import org.example.model.Person;
import org.example.model.Role;
import org.example.repository.PersonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

// поле:
// - repo — экземпляр PersonRepository, который создаётся заново перед каждым тестом (@BeforeEach)
//
// методы:
// 1) setup()
//    - выполняется перед каждым тестом
//    - создаёт новый репозиторий и добавляет три объекта Person (Alice, BigBob, Ketrin)
// 2) testFindByName_Found()
//    - проверяет метод findByName при поиске существующего имени
//    - ожидается, что найден список людей с именем "Alice"
//    - assertEquals проверяет, что размер списка равен ожидаемому 
// 3) testFindByName_NotFound()
//    - проверяет метод findByName при поиске несуществующего имени
//    - ожидается пустой список
//    - assertTrue проверяет, что список действительно пустой

public class PersonRepositoryTest {
    private PersonRepository repo;

    @BeforeEach
    void setup() {
        repo = new PersonRepository();
        repo.addPerson(new Person(1, "Alice", 2500.5f, Role.ADMIN, true));
        repo.addPerson(new Person(2, "BigBob", 1800.0f, Role.USER, false));
        repo.addPerson(new Person(3, "Ketrin", 3000.0f, Role.USER, true));
    }

    @Test
    void testFindByName_Found() {
        List<Person> result = repo.findByName("Alice");
        assertEquals(1, result.size());
    }

    @Test
    void testFindByName_NotFound() {
        List<Person> result = repo.findByName("BonBon");
        assertTrue(result.isEmpty());
    }
}
