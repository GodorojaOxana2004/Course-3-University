package com.example.culinarybuilder.model;

import java.util.UUID;

public class MutableIngredient {
    private String id = UUID.randomUUID().toString();
    private String name;
    private double quantity;
    private String unit;
    private int line;

    public MutableIngredient(String name, double quantity, String unit, int line) {
        this.name = name;
        this.quantity = quantity;
        this.unit = unit;
        this.line = line;
    }

    public MutableIngredient() {

    }

    public String getName() { return name; }
    public int getLine() { return line; }

    public Ingredient toImmutable() {
        return new Ingredient(id, name, quantity, unit);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public double getQuantity() {
        return quantity;
    }

    public void setQuantity(double quantity) {
        this.quantity = quantity;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

    public void setLine(int line) {
        this.line = line;
    }

    public void setName(String name) {
        this.name = name;
    }
}