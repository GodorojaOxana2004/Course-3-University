package com.example._1_lab.controller;

import com.example._1_lab.model.Person;
// Этот файл описывает класс PersonDTO — объект передачи данных (DTO).
// Одля того, чтобы отправлять наружу только необходимые поля из модели

public class PersonDTO {
    public String name;
    public String role;

    public PersonDTO(Person p) {
        this.name = p.getName();
        this.role = p.getRole().name();
    }
}
