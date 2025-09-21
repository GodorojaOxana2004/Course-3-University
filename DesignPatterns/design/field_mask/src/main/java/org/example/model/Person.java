package org.example.model;

import org.example.model.Role;

public class Person {
    private int id;
    private String name;
    private float salary;
    private Role role;
    private boolean active;

    public Person(int id, String name, float salary, Role role, boolean active) {
        this.id = id;
        this.name = name;
        this.salary = salary;
        this.role = role;
        this.active = active;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public float getSalary() { return salary; }
    public Role getRole() { return role; }
    public boolean isActive() { return active; }
}
