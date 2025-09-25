package org.example.controller;

import org.example.model.Person;
// Этот файл описывает класс PersonDTO — объект передачи данных (DTO).
// Он используется для того, чтобы отправлять наружу (например, через API)
// только необходимые поля из модели Person (тут: name и role),
// скрывая остальные внутренние данные (например, зарплату или статус активности)

public class PersonDTO {
    public String name;
    public String role;

    public PersonDTO(Person p) {
        this.name = p.getName();
        this.role = p.getRole().name();
    }
}
