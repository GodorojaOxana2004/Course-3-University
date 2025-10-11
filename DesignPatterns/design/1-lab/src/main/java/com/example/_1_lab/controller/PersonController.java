package com.example._1_lab.controller;

import com.example._1_lab.model.Person;
import com.example._1_lab.model.Role;
import com.example._1_lab.repository.PersonRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.stream.Collectors;
import com.example._1_lab.mask.FieldMask;

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

    @GetMapping("/people/masked")
    public List<PersonDTO> getPeopleWithMask(
            @RequestParam(required = false) String name,

            @RequestParam(defaultValue = "true") boolean id,
            @RequestParam(defaultValue = "true") boolean nameField,
            @RequestParam(defaultValue = "true") boolean salary,
            @RequestParam(defaultValue = "true") boolean role,
            @RequestParam(defaultValue = "true") boolean active
    ) {
        List<Person> list = repo.findByName(name);

        FieldMask mask = new FieldMask(id, nameField, salary, role, active);

        return list.stream()
                .map(p -> new PersonDTO(p, mask))
                .collect(Collectors.toList());
    }

}