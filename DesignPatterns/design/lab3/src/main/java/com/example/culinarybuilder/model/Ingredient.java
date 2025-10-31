package com.example.culinarybuilder.model;

public class Ingredient {
    private String id;
    private String name;
    private double quantity;
    private String unit;

    public Ingredient(String id, String name, double quantity, String unit) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.unit = unit;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public double getQuantity() { return quantity; }
    public String getUnit() { return unit; }

    @Override
    public String toString() {
        return name + " (" + quantity + unit + ")";
    }
}