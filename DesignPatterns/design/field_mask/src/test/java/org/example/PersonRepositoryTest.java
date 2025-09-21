package org.example;

import org.example.model.Person;
import org.example.model.Role;
import org.example.repository.PersonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class PersonRepositoryTest {
    private PersonRepository repo;

    @BeforeEach
    void setup() {
        repo = new PersonRepository();
        repo.addPerson(new Person(1, "Alice", 2500.5f, Role.ADMIN, true));
        repo.addPerson(new Person(2, "Bob", 1800.0f, Role.USER, false));
        repo.addPerson(new Person(3, "Alice", 3000.0f, Role.USER, true));
    }

    @Test
    void testFindByName_Found() {
        List<Person> result = repo.findByName("Alice");
        assertEquals(2, result.size());
    }

    @Test
    void testFindByName_NotFound() {
        List<Person> result = repo.findByName("Charlie");
        assertTrue(result.isEmpty());
    }
}
