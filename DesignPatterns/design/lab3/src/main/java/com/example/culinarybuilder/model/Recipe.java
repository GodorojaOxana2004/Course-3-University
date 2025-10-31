package com.example.culinarybuilder.model;

import java.util.List;
import java.util.stream.Collectors;

public class Recipe {
    private String id;
    private String name;
    private List<Ingredient> ingredients;
    private List<Step> steps;

    public Recipe(String id, String name, List<Ingredient> ingredients, List<Step> steps) {
        this.id = id;
        this.name = name;
        this.ingredients = ingredients;
        this.steps = steps;
    }

    public List<String> generateSQL() {
        List<String> sql = ingredients.stream()
                .map(i -> String.format("INSERT INTO ingredients(id, name, quantity, unit) VALUES ('%s','%s',%s,'%s');", i.getId(), i.getName(), i.getQuantity(), i.getUnit()))
                .collect(Collectors.toList());
        sql.addAll(steps.stream()
                .map(s -> String.format("INSERT INTO steps(id, description) VALUES ('%s','%s');", s.getId(), s.getDescription()))
                .collect(Collectors.toList()));
        sql.add(String.format("INSERT INTO recipes(id, name) VALUES ('%s','%s');", id, name));
        return sql;
    }

    @Override
    public String toString() {
        return "Recipe{id='" + id + "', name='" + name + "', ingredients=" + ingredients + ", steps=" + steps + '}';
    }
}