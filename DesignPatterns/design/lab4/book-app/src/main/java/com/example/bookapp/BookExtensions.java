package com.example.bookapp;

import com.example.dynamiclib.KeyRegistry;
import com.example.dynamiclib.TypedKey;

import java.util.List;

public class BookExtensions {
    public final TypedKey<Double> RATING;
    public final TypedKey<List> GENRES;
    public final TypedKey<Integer> SALES;

    public BookExtensions(KeyRegistry registry) {
        RATING = registry.register("book.rating", Double.class);
        GENRES = registry.register("book.genres", List.class);
        SALES = registry.register("book.sales", Integer.class);
    }
}
