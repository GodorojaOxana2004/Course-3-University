package com.example._1_lab.controller;

import com.example._1_lab.model.Person;
import com.example._1_lab.mask.FieldMask;
import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class PersonDTO {
    public Integer id;
    public String name;
    public Float salary;
    public String role;
    public Boolean active;

    public PersonDTO(Person p, FieldMask mask) {
        if (mask.showId())     this.id = p.getId();
        if (mask.showName())   this.name = p.getName();
        if (mask.showSalary()) this.salary = p.getSalary();
        if (mask.showRole())   this.role = p.getRole().name();
        if (mask.showActive()) this.active = p.isActive();
    }
}
