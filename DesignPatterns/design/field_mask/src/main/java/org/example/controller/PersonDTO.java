package org.example.controller;

import org.example.model.Person;

public class PersonDTO {
    public String name;
    public String role;

    public PersonDTO(Person p) {
        this.name = p.getName();
        this.role = p.getRole().name();
    }
}
