package org.example.mask;

public class FieldMask {
    private boolean id;
    private boolean name;
    private boolean salary;
    private boolean role;
    private boolean active;

    public FieldMask(boolean id, boolean name, boolean salary, boolean role, boolean active) {
        this.id = id;
        this.name = name;
        this.salary = salary;
        this.role = role;
        this.active = active;
    }

    public boolean showId() { return id; }
    public boolean showName() { return name; }
    public boolean showSalary() { return salary; }
    public boolean showRole() { return role; }
    public boolean showActive() { return active; }
}
