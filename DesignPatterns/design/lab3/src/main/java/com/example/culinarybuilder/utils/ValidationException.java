package com.example.culinarybuilder.utils;

import java.util.List;

public class ValidationException extends Exception {
    public ValidationException(List<String> errors) {
        super(String.join("\n", errors));
    }
}