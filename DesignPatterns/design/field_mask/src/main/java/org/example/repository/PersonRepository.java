package org.example.repository;

import org.example.model.Person;
import java.util.ArrayList;
import java.util.List;

public class PersonRepository {
    private final List<Person> people = new ArrayList<>();

    public void addPerson(Person person) {
        people.add(person);
    }

    public List<Person> findByName(String name) {
        if(name == null || name.isEmpty()) return people;
        List<Person> result = new ArrayList<>();
        for (Person p : people) {
            if (p.getName().equals(name)) {
                result.add(p);
            }
        }
        return result;
    }
}
