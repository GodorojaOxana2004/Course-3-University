package com.example.culinarybuilder;

import com.example.culinarybuilder.builder.*;
import com.example.culinarybuilder.model.*;

public class Main {
    public static void main(String[] args) {
        try {
            Ingredient beet = new IngredientBuilder().setName("Свекла").setQuantity(2).setUnit("шт").build();
            Ingredient carrot = new IngredientBuilder().setName("Морковь").setQuantity(1).setUnit("шт").build();
            Ingredient potato = new IngredientBuilder().setName("Картофель").setQuantity(3).setUnit("шт").build();

            Step chop = new StepBuilder().setDescription("Нарезать овощи").build();
            Step boil = new StepBuilder().setDescription("Варить 30 минут").build();

            Recipe recipe = new RecipeBuilder()
                    .setName("Борщ")
                    .addIngredient(beet)
                    .addIngredient(carrot)
                    .addIngredient(potato)
                    .addStep(chop)
                    .addStep(boil)
                    .build();

            System.out.println(recipe);
            System.out.println("SQL для сохранения:");
            recipe.generateSQL().forEach(System.out::println);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
