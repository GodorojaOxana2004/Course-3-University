package org.example.repository;

import org.example.model.Person;
import java.util.ArrayList;
import java.util.List;

// Имитирую работу базы данных, используя список (ArrayList).
// какие поля имеются:
// - people — список объектов Person, в котором хранятся все добавленные пользователи
// методы:
// - addPerson(Person person) — добавляет нового человека в список
// - findByName(String name) — ищет людей по имени:
//      • если name = null или пустая строка -> возвращает весь список
//      • иначе проходит по списку и возвращает только тех, у кого имя совпадает с заданным
//
// PersonRepository служит слоем доступа к данным (DAO)

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
