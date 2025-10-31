package com.example.culinarybuilder.builder;

import com.example.culinarybuilder.model.MutableIngredient;
import com.example.culinarybuilder.model.Ingredient;

public class IngredientBuilder {
    private MutableIngredient ingredient = new MutableIngredient();

    public IngredientBuilder setName(String name) {
        ingredient.setName(name);
        return this;
    }

    public IngredientBuilder setQuantity(double quantity) {
        ingredient.setQuantity(quantity);
        return this;
    }

    public IngredientBuilder setUnit(String unit) {
        ingredient.setUnit(unit);
        return this;
    }

    public Ingredient build() {
        return ingredient.toImmutable();
    }
}
