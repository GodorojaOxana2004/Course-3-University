package com.example.culinarybuilder.model;

import com.example.culinarybuilder.utils.ValidationException;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class MutableRecipe {
    private String id = UUID.randomUUID().toString();
    private String name;
    private List<MutableIngredient> ingredients = new ArrayList<>();
    private List<MutableStep> steps = new ArrayList<>();
    private List<String> errors = new ArrayList<>();

    public void setName(String name) {
        if (name == null || name.isEmpty()) errors.add("Line " + id + ": Название рецепта пустое");
        this.name = name;
    }

    public void addIngredient(MutableIngredient ingredient) {
        if (ingredient.getName() == null || ingredient.getName().isEmpty())
            errors.add("Ingredient at line " + ingredient.getLine() + " has no name");
        ingredients.add(ingredient);
    }

    public void addStep(MutableStep step) {
        if (step.getDescription() == null || step.getDescription().isEmpty())
            errors.add("Step at line " + step.getLine() + " has no description");
        steps.add(step);
    }

    public Recipe toImmutable() throws ValidationException {
        if (name == null || name.isEmpty()) errors.add("Recipe has no name");
        if (ingredients.isEmpty()) errors.add("Recipe has no ingredients");
        if (steps.isEmpty()) errors.add("Recipe has no steps");
        if (!errors.isEmpty()) throw new ValidationException(errors);

        List<Ingredient> ingList = new ArrayList<>();
        for (MutableIngredient mi : ingredients) ingList.add(mi.toImmutable());
        List<Step> stList = new ArrayList<>();
        for (MutableStep ms : steps) stList.add(ms.toImmutable());

        return new Recipe(id, name, ingList, stList);
    }
}