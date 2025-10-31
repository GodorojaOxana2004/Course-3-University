package com.example.culinarybuilder.builder;

import com.example.culinarybuilder.model.*;
import com.example.culinarybuilder.utils.ValidationException;

public class RecipeBuilder {
    private MutableRecipe recipe = new MutableRecipe();

    public RecipeBuilder setName(String name) {
        recipe.setName(name);
        return this;
    }

    public RecipeBuilder addIngredient(Ingredient ingredient) {
        recipe.addIngredient(new MutableIngredient(ingredient.getName(), ingredient.getQuantity(), ingredient.getUnit(), 0));
        return this;
    }

    public RecipeBuilder addStep(Step step) {
        recipe.addStep(new MutableStep(step.getDescription(), 0));
        return this;
    }

    public Recipe build() throws ValidationException {
        return recipe.toImmutable();
    }
}
