package org.example.controller;

import org.example.model.Person;
import org.example.model.Role;
import org.example.repository.PersonRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.stream.Collectors;

// REST-контроллер Spring, который обрабатывает запросы к /people,
// и возвращает список людей из репозитория (с фильтрацией по имени, если передан параметр)


@RestController
public class PersonController {
    private final PersonRepository repo = new PersonRepository();

    public PersonController() {
        repo.addPerson(new Person(1, "Alice", 2500.5f, Role.ADMIN, true));
        repo.addPerson(new Person(2, "BigBob", 1800.0f, Role.USER, false));
        repo.addPerson(new Person(3, "Ketrin", 3000.0f, Role.USER, true));
    }

    @GetMapping("/people")
    public List<PersonDTO> getPeople(@RequestParam(required = false) String name) {
        List<Person> list = repo.findByName(name);
        return list.stream().map(PersonDTO::new).collect(Collectors.toList());
    }
}
